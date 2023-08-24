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

    service_context = ServiceContext.from_defaults()
    index = VectorStoreIndex(nodes, service_context=service_context)
    index.storage_context.persist(persist_dir="storage/"+directory_path)

    return index


def chatbot_generator(input_text, prompt_text, directory_path):
    storage_context = StorageContext.from_defaults(persist_dir="storage/"+directory_path)
    index = load_index_from_storage(storage_context)
    if prompt_text != "":
        replacement_prompt = Prompt(prompt_text)
        query_engine = index.as_query_engine(similarity_top_k=5, text_qa_template=replacement_prompt)
    else:
        query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(input_text)
    return {"answer": response.response, "sources": response.get_formatted_sources(length=400)}
