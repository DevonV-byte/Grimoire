# --- Imports ---
import os
from langchain_community.document_loaders import (
    TextLoader, Docx2txtLoader, NotebookLoader, PythonLoader
)
from .text_splitter import split_documents

# --- Globals ---
COURSE_DIR = "IBM RAG and Agentic AI"
ALLOWED_EXTENSIONS = {".txt", ".docx", ".ipynb", ".py"}

# --- Helpers ---
def get_loader(file_path):
    """
    Returns the appropriate loader for a given file extension.
    """
    _, ext = os.path.splitext(file_path)
    if ext == ".txt":
        return TextLoader(file_path)
    elif ext == ".docx":
        return Docx2txtLoader(file_path)
    elif ext == ".ipynb":
        return NotebookLoader(file_path)
    elif ext == ".py":
        return PythonLoader(file_path)
    else:
        return None

def load_course_documents(course_dir):
    """
    Loops through the course folder, identifies file types, applies the correct loader,
    and extracts the raw text from the documents.
    """
    loaded_documents = []
    for root, _, files in os.walk(course_dir):
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                file_path = os.path.join(root, file)
                loader = get_loader(file_path)
                if loader:
                    loaded_documents.extend(loader.load())
    return loaded_documents

def main():
    """Loads documents, splits them into chunks, and prints the total number of chunks."""
    documents = load_course_documents(COURSE_DIR)
    chunks = split_documents(documents)
    print(f"Loaded {len(documents)} documents and split them into {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
