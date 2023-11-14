import openai
import os
from dotenv import load_dotenv
import time
load_dotenv()

# Set up OpenAI API credentials
client = openai.Client().beta

def construct_index(directory_path):
    # check if assistant_id.txt already exists
    # if it does, check the file list and see if it matches the current directory
    # if it does, return the assistant_id
    # else, upload the missing files and create a new assistant
    # if assistant_id.txt does not exist, create a new assistant
    # and store the assistant ID in assistant_id.txt

    # check if assistant_id.txt exists
    if os.path.exists("storage/" + directory_path + "/assistant_id.txt"):
        # check if the file list matches the current directory
        with open("storage/"+directory_path+"/assistant_id.txt", "r") as f:
            assistant_id = f.read()
        assistant = client.assistants.retrieve(assistant_id)
        file_ids = assistant.file_ids
        for id in file_ids:
            openai.files.delete(id)
        files = []
        for r, d, f in os.walk("docs/" + directory_path):
            for file in f:
                files.append(os.path.join(r, file))
        for file in files:
            with open(file, "rb") as f:
                response = openai.files.create(file=f, purpose="assistants")
                file_ids.append(response.id)
        assistant = client.assistants.update(
            assistant_id,
            file_ids=file_ids
        )
        return
            
    else:
        # upload files to OpenAI
        files = []
        file_ids = []
        for r, d, f in os.walk("docs/" + directory_path):
            for file in f:
                files.append(os.path.join(r, file))
        for file in files:
            with open(file, "rb") as f:
                response = openai.files.create(file=f, purpose="assistants")
                file_ids.append(response.id)

        # Create a new assistant
        assistant = client.assistants.create(
            name="my-assistant",
            model="gpt-4-1106-preview",
            instructions="You're a VTP (Virtual Training Program) Assistant. You can answer questions about the VTP contents.",
            tools=[{"type": "retrieval"}],
            file_ids=file_ids
        )

        # Store the assistant ID for future reference
        assistant_id = assistant.id
        with open("storage/" + directory_path + "/assistant_id.txt", "w") as f:
            f.write(assistant_id)

def chatbot_generator(input_text, prompt_text, directory_path):

    # Load the assistant
    with open("storage/" + directory_path + "/assistant_id.txt", "r") as f:
        assistant_id = f.read()

    # Ask the assistant a question
    thread = client.threads.create(
        messages=[
            {
            "role": "user",
            "content": input_text,
            }
        ]
    )
    if prompt_text == "":
        prompt_text = "You're a VTP (Virtual Training Program) Assistant. You can answer questions about the VTP contents."
    run = client.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions= prompt_text,
    )

    # check the status of the run every 100ms
    # if the status is completed, return the response
    # else, return the status
    response = client.threads.runs.retrieve(
        run.id,
        thread_id=thread.id,
    )
    while response.status == "in_progress":
        response = client.threads.runs.retrieve(
            run.id,
            thread_id=thread.id,
        )
        print(response.status)
        time.sleep(0.2)

    messages = client.threads.messages.list(
        thread_id=thread.id
    )
    message = messages.data[0]
    message_content = message.content[0]
    if message_content.type == "text": message_value = message_content.text.value
    else: message_value = ""
    if message_content.type == "text": annotations = message_content.text.annotations
    else: annotations = []
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_value.replace(annotation.text, f' [{index}]')

        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = openai.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = openai.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    message_value += '\n' + '\n'.join(citations)

    # Print the response
    print(messages)
    return {"answer": message_value, "sources": annotations} # type: ignore