from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 1. load document
loader = TextLoader("./app/data/leave_policy.txt")
documents = loader.load()

print(f"Loaded {len(documents)} documents")

# 2. Split documnet into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")

# 3. create embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4. Store embeddings in Chroma

vectore_store = Chroma(
    collection_name="leave_policy",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

vectore_store.add_documents(chunks)

print("Embeddings stored in Chroma database")

# 5. Create a retriever
retriver = vectore_store.as_retriever(search_kwargs={"k": 3})

# 6. Search Policy

question = "Can casual leave be carried forward?"

results = retriver.invoke(question)


print("\n--- Retrieved Documents ---")

for i, document in enumerate(results, start=1):
    print(f"\nDocument {i}:")
    print(document.page_content)
