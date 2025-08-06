
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.schema import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from pydantic import ValidationError
from agent import chat, State

@pytest.fixture(scope='module')
def setup_environment():
    load_dotenv(override=True)
    assert "DEPLOYMENT_NAME" in os.environ
    assert "OPENAI_API_VERSION" in os.environ
    assert "AZURE_OPENAI_ENDPOINT" in os.environ
    assert "OPENAI_API_KEY" in os.environ

@pytest.fixture
def mock_openai():
    with patch('langchain_openai.AzureChatOpenAI.invoke') as mock_invoke:
        mock_invoke.return_value = SystemMessage(content="Mocked response")
        yield mock_invoke

@pytest.fixture
def initialized_graph():
    messages = [SystemMessage(content="System message"), HumanMessage(content="User input")]
    state = State(messages=messages)
    graph_builder = StateGraph(State)
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return state, graph

def test_agent_initialization(setup_environment, mock_openai):
    llm = AzureChatOpenAI(
        deployment_name=os.environ["DEPLOYMENT_NAME"],
        openai_api_version=os.environ["OPENAI_API_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        openai_api_type=os.environ["OPENAI_API_TYPE"]
    )
    
    assert llm.deployment_name == os.environ["DEPLOYMENT_NAME"]
    assert llm.openai_api_version == os.environ["OPENAI_API_VERSION"]

def test_interaction_workflow(initialized_graph, mock_openai):
    state, graph = initialized_graph
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke(state, config=config)
    assert result["messages"][-1].content == "Mocked response"

def test_chat_function(mock_openai):
    response = chat(user_input="What's the weather?", history=[])
    assert response == "Mocked response"

def test_error_handling(mock_openai):
    mock_openai.side_effect = Exception("Network Error")
    with pytest.raises(Exception, match="Network Error"):
        chat(user_input="Test", history=[])

def test_state_management(initialized_graph):
    state, graph = initialized_graph
    assert isinstance(state.messages, list)

def test_performance():
    import time
    start_time = time.time()
    response = chat(user_input="What's the weather?" * 1000, history=[])
    end_time = time.time()
    assert end_time - start_time < 2  # assuming response must complete within 2 seconds

def test_async_operations():
    # Assuming we have some async function, to test use pytest-asyncio or similar
    pass  # expanding this requires explicit async methods in the workflow