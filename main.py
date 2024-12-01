from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import deepl

load_dotenv()

auth_key = "" # deepl auth key for translation. not use in .env file
translator = deepl.Translator(auth_key)

model = ChatOpenAI(model="gpt-3.5-turbo")
memory = SqliteSaver.from_conn_string(":memory:")

search = TavilySearchResults(max_results=2)
tools = [search]

model_with_tools = model.bind_tools(tools)

agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

if __name__ == '__main__':
    while True:
        user_input = input(">")
        for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
        ):
            if 'agent' in chunk and 'messages' in chunk['agent']:
                for message in chunk['agent']['messages']:
                    if isinstance(message, AIMessage):
                        print(message.content)
                        print("----")



#    full_text = ""
#   for chunk in rag_chain.stream("what's in the ram bank"):
#        full_text += chunk
#        print(chunk, end="", flush=True, )
#
#    result = translator.translate_text(full_text, target_lang="TR") # use the deepl translator to translate the text to any language
#    print("\n" + str(result))