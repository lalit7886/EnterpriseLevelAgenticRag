import time
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import get_settings
from app.core.logging import logging

settings = get_settings()
_embeddings = None
_vectorstore = None

def get_embdeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
    model_name = settings.embedding_model,
    model_kwargs= {"device":"cpu"},
    encode_kwargs={"normalize_embeddings": True}
    
        
        )
    return _embeddings


def ensure_index():
    if not settings.pinecone_api_key:
        raise RuntimeError("Pinecone api key is missing")
    
    pc = Pinecone(api_key= settings.pinecone_api_key)
    names = [x["name"] for x in pc.list_indexes()]
    
    if settings.pinecone_index_name in names:
        index_info = pc.describe_index(settings.pinecone_index_name)
        
    if settings.pinecone_index_name not in [x["name"] for x in pc.list_indexes()]:
        pc.create_index(
            name = settings.pinecone_index_name,
            dimension=1024,
            metric="cosine",
            spec = ServerlessSpec(cloud = "aws", region = "us-east-1")

        )
        
        while not pc.describe_index(settings.pinecone_index_name).status["ready"]:
            time.sleep(1)
    return pc.Index(settings.pinecone_index_name)

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        logging.info("initating get_vectorstore")
        index = ensure_index()
        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=get_embdeddings(),
            namespace=settings.pinecone_namespace
        )
        logging.info("Sucssfully created _vectorestore")
    return _vectorstore
    
def get_retriever():
    return get_vectorstore().as_retriever(search_kwargs={"k":settings.top_k})

def add_documents(chunks):
    store = get_vectorstore()
    if store is None:
        raise RuntimeError("vector store initailzationn failed")
    return store.add_documents(chunks)