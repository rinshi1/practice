#this is just to check
import os
from dotenv import load_dotenv
load_dotenv(override=True)
os.environ["DEPLOYMENT_NAME"]=os.getenv("DEPLOYMENT_NAME")
os.environ["OPENAI_API_TYPE"]=os.getenv("OPENAI_API_TYPE")
os.environ["AZURE_OPENAI_ENDPOINT"]=os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"]=os.getenv("OPENAI_API_VERSION")
os.environ["AZURE_OPENAI_API_KEY"]=os.getenv("AZURE_OPENAI_API_KEY")
 
from langchain_openai import AzureChatOpenAI
 
llm = AzureChatOpenAI(
    deployment_name=os.environ["DEPLOYMENT_NAME"],
    openai_api_version=os.environ["OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    openai_api_type=os.environ["OPENAI_API_TYPE"]
)

from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from langchain.schema import HumanMessage , SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import gradio as gr
from pydantic import BaseModel



class State(BaseModel):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state.messages)]}

graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

def chat(user_input: str, history):
    user_message = HumanMessage(content=user_input)

    #Add system promote according to your task
    system_message = SystemMessage(content="You are a flight booking assistant for a travel agency. Your role is to assist with booking flights, providing timely updates, adhering to all safety protocols, and maintaining a high standard of observability for ongoing interactions. You are equipped to maintain long-term memory for the user's preferences and past interactions to ensure a personalized experience.")
    messages = [system_message, user_message]
    state = State(messages=messages)
    result = graph.invoke(state, config=config)
    return result["messages"][-1].content

gr.ChatInterface(chat, type="messages").launch()