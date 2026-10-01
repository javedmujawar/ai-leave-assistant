from langchain_ollama import ChatOllama

model  = ChatOllama(model="qwen3:1.7b", temperature=0)

response =  model.invoke("What is caulse Leave?")
print(response.content)