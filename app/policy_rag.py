from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# 1. create embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Load Chroma database
vectore_store = Chroma(
    collection_name="leave_policy",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
# 3. Create a retriever
retriever = vectore_store.as_retriever(search_kwargs={"k": 3})

# 4. LLM
llm = ChatOllama(model="qwen3:1.7b", temperature=0)

# 5. Create a prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an leave policy assistant.

Answer the user's question using ONLY the provided company policy.

If the policy does not contain the answer, say:
"I could not find this information in the available policy."

Do not invent or assume company policies.

Policy:
{context}""",
        ),
        ("human", "{question}"),
    ]
)

# 6. Create a chain
chain = prompt | llm


def ask_policy(question):
    # Retrieve relevant documents
    documents = retriever.invoke(question)

    # Combine retrieved content
    context = "\n\n".join(document.page_content for document in documents)

    # Create prompt
    messages = prompt.invoke({"context": context, "question": question})

    # Ask LLM
    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":
    question = input("Ask Leave Policy Question: ")
    answer = ask_policy(question)
    print("\n--- Answer ---")
    print(answer)
