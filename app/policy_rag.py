from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
def search_leave_policy(question: str) -> str:
    """Search the company leave policy and answer questions about leave rules."""
    return ask_policy(question)

# 1. Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Load Chroma database
vector_store = Chroma(
    collection_name="leave_policy",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)


# 3. Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 4. LLM
llm = ChatOllama(
    model="qwen3:1.7b",
    tools=[search_leave_policy],
    temperature=0
)


# 5. Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a leave policy assistant.

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


# 6. Chain
chain = prompt | llm


def ask_policy(question: str) -> str:
    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content


if __name__ == "__main__":
    question = input("Ask Leave Policy Question: ")

    answer = ask_policy(question)

    print("\n--- Answer ---")
    print(answer)