# --- Imports ---
import os
from langchain_community.document_loaders import (
    TextLoader, Docx2txtLoader, NotebookLoader, PythonLoader
)

# --- Globals ---
COURSE_DIR = "../IBM RAG and Agentic AI"
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

# --- Main loop ---
def main():
    """
    Loads all allowed documents from the course directory.
    """
    loaded_documents = []
    for root, _, files in os.walk(COURSE_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                file_path = os.path.join(root, file)
                loader = get_loader(file_path)
                if loader:
                    loaded_documents.extend(loader.load())

    # TODO: Process the loaded_documents further (e.g., chunking, embedding, storing in a vector DB)
    print(f"Loaded {len(loaded_documents)} documents.")

if __name__ == "__main__":
    main()
