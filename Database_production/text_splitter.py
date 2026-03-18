# --- Imports ---
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Functions ---
def split_documents(documents):
    """
    Splits the loaded documents into smaller chunks for processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(documents)

def main():
    """
    Main function to demonstrate the text splitting functionality.
    """
    # This is a placeholder for the actual documents
    # In a real scenario, you would load the documents first
    class Document:
        def __init__(self, page_content):
            self.page_content = page_content
            self.metadata = {}

    sample_documents = [
        Document("This is a long document that needs to be split. " * 100),
        Document("Another long document for splitting. " * 100)
    ]
    
    chunks = split_documents(sample_documents)
    print(f"Split {len(sample_documents)} documents into {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
