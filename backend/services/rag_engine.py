from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai_like import OpenAILike  # Updated import
from llama_index.core.prompts import PromptTemplate
from llama_index.core.node_parser import SentenceSplitter
import os

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=100,
    paragraph_separator="\n\n"
)

def get_chat_engine(vector_store):
    # Updated LLM class
    llm = OpenAILike(
        model="openrouter/free", 
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
        is_chat_model=True,
        temperature=0.1
    )
    Settings.llm = llm

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    text_qa_template = PromptTemplate(
        "You are an expert document analyst.\n"
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, answer the query accurately. "
        "Query: {query_str}\n"
        "Answer: "
    )

    return index.as_query_engine(
        similarity_top_k=5,
        text_qa_template=text_qa_template
    )