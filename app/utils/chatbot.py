from langchain import OpenAI
import gradio as gr

from dotenv import load_dotenv
load_dotenv()

from llama_index import (
    SimpleDirectoryReader,
    node_parser,
    VectorStoreIndex,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.prompts import Prompt

def construct_index(directory_path):

    docs = SimpleDirectoryReader("docs/"+directory_path).load_data()
    parser = node_parser.SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(docs)

    # llm = OpenAI(model="gpt-4", temperature=70, max_tokens=1024)
    # max_input_size = 4096
    # num_output = 1024
    # chunk_overlap_ratio = 0.40
    # chunk_size_limit = 1200

    # prompt_helper = PromptHelper(max_input_size, num_output, chunk_overlap_ratio, chunk_size_limit=chunk_size_limit)

    service_context = ServiceContext.from_defaults( chunk_size = 1024 )
    index = VectorStoreIndex(nodes, service_context=service_context)
    index.storage_context.persist(persist_dir="storage/"+directory_path)

    return index


def chatbot_generator(input_text, prompt_text):
    storage_context = StorageContext.from_defaults(persist_dir="storage/"+"singlecell")
    index = load_index_from_storage(storage_context)
    if prompt_text != "":
        replacement_prompt = Prompt(prompt_text)
        query_engine = index.as_query_engine(similarity_top_k=5, text_qa_template=replacement_prompt)
    else:
        replacement_prompt = None
        query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(input_text)
    return {"answer": response.response, "sources": response.get_formatted_sources(length=400)}
