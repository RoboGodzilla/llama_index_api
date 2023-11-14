import os
from dotenv import load_dotenv
load_dotenv()

from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    SummaryIndex,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    load_graph_from_storage,
)
from llama_index.prompts import Prompt
from llama_index.composability import ComposableGraph
from llama_index.llms import OpenAI

def construct_index(directory_path):
    # for every file in the directory_path, create a vectorstore index
    # and store it in the storage directory
    files = []
    for r, d, f in os.walk("docs/" + directory_path):
        for file in f:
            files.append(os.path.join(r, file))
    service_context = ServiceContext.from_defaults()
    indexes = []
    for file in files:
        doc = SimpleDirectoryReader(input_files=[file]).load_data()
        index = VectorStoreIndex.from_documents(doc, service_context=service_context, show_progress=True)
        indexes.append(index)

        index.storage_context.persist(persist_dir=os.path.join("storage", directory_path, os.path.splitext(os.path.basename(file))[0]))

    return


def chatbot_generator(input_text, prompt_text, chapter_content, directory_path):
    dirs = []
    indexes = []
    # index_summaries = [os.path.splitext(os.path.basename())[0] + "_summary" for file in files]
    for r, d, f in os.walk("storage/" + directory_path):
        for dir in d:
            dirs.append(dir)
            storage_context = StorageContext.from_defaults(persist_dir=os.path.join("storage", directory_path, dir))
            index = load_index_from_storage(storage_context=storage_context)
            indexes.append(index)
    graph = ComposableGraph.from_indices(SummaryIndex, indexes, index_summaries=[dir + "_summary" for dir in dirs])
    if prompt_text != "":
        replacement_prompt = Prompt(prompt_text)
        llm = OpenAI(model="gpt-4", max_tokens=4096)
        query_engine = graph.as_query_engine(similarity_top_k=3, text_qa_template=replacement_prompt, llm=llm)
    else:
        query_engine = graph.as_query_engine()
    response = query_engine.query(input_text)
    return {"answer": response.response, "sources": response.get_formatted_sources(length=400)} # type: ignore
