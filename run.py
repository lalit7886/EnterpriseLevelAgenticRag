from app.rag.vectorstore import get_embdeddings
from app.services.ingestion import load_file,chunk_documents
from pathlib import Path
from app.rag.vectorstore import add_documents

data_dir = Path("data/sample_kb")
for files_ in data_dir.iterdir():
    docs = load_file(files_)
    chunks = chunk_documents(docs)
    add_documents(chunks)
    
    
# embedding_model=get_embdeddings()


