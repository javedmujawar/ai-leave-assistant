"""Leave assistant agent setup."""

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from policy_rag import search_leave_policy
from leave_tools import get_leave_balance, apply_leave


# LLM
llm = ChatOllama(model="qwen3:1.7b", temperature=0)


# Agent
agent = create_agent(
    model=llm,
    tools=[search_leave_policy, get_leave_balance, apply_leave],
    system_prompt="""
You are an AI Leave Assistant.

    Use search_leave_policy for leave policy questions.

    Use get_leave_balance for leave balance questions.

    Use apply_leave when the user wants to apply for leave.

    Do not invent information.
""",
)


if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "my user id is user_1.Apply 2 days casual leave from October 10 to October 11 because I have a personal function.",
                }
            ]
        }
    )

    print("\n--- Agent Response ---")
    print(response["messages"][-1].content)
