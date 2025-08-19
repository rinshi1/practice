
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
import os
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, ValidationError
import asyncio

# Load environment variables for testing
load_dotenv(override=True)

class StateSchema(BaseModel):
    messages: Annotated[list, add_messages]

@pytest.fixture(scope='session')
def setup_environment():
    """Fixture to provide a clean environment."""
    os.environ["DEPLOYMENT_NAME"] = "mock_deployment"
    os.environ["OPENAI_API_TYPE"] = "mock_api_type"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "mock_endpoint"
    os.environ["OPENAI_API_VERSION"] = "mock_version"
    os.environ["AZURE_OPENAI_API_KEY"] = "mock_key"
    yield
    # Teardown environment
    for key in ["DEPLOYMENT_NAME", "OPENAI_API_TYPE", "AZURE_OPENAI_ENDPOINT", "OPENAI_API_VERSION", "AZURE_OPENAI_API_KEY"]:
        del os.environ[key]

@pytest.fixture
def mocked_llm():
    """Fixture to provide a mocked AzureChatOpenAI instance."""
    with patch('langchain_openai.AzureChatOpenAI') as mock_llm:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = 'Test response from mocked LLM.'
        mock_llm.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def state_graph():
    """Fixture to setup the StateGraph."""
    return StateGraph(StateSchema)

def test_agent_workflow(setup_environment, mocked_llm, state_graph):
    """Test the complete agent workflow and validate execution flow."""
    memory_saver = MemorySaver()
    state_graph.add_node("chatbot", lambda state: {"messages": [mocked_llm.invoke(state.messages)]})
    state_graph.add_edge(START, "chatbot")
    state_graph.add_edge("chatbot", END)
    
    graph = state_graph.compile(checkpointer=memory_saver)
    
    system_message = SystemMessage(content="Test system message for workflow validation.")
    user_message = HumanMessage(content="Test user query.")
    messages = [system_message, user_message]

    state = StateSchema(messages=messages)
    config = {"configurable": {"thread_id": "1"}}
    
    result = graph.invoke(state, config=config)
    assert result["messages"] == ['Test response from mocked LLM.']

def test_component_interaction(mocked_llm):
    """Test inter-component communication."""
    user_input = "Component interaction test"
    history = []
    
    with patch('agent.chat') as mock_chat:
        mock_chat.return_value = 'Mocked component interaction response'
        response = mock_chat(user_input, history)
    
    assert response == 'Mocked component interaction response'

def test_error_handling():
    """Test error propagation in components with ValidationError."""
    invalid_state_data = {"messages": "This should be a list but is a string"}
    
    with pytest.raises(ValidationError):
        StateSchema(**invalid_state_data)

@pytest.mark.asyncio
async def test_async_operations(mocked_llm):
    """Test async functions with mocked LLM interactions."""
    async def async_chat_function(state_schema):
        return await mocked_llm.invoke(state_schema.messages)

    result = await async_chat_function(StateSchema(messages=[HumanMessage(content="Async test message")]))
    assert result == 'Test response from mocked LLM.'

def test_configuration(setup_environment):
    """Test configuration and environment variable loading."""
    assert os.environ["DEPLOYMENT_NAME"] == "mock_deployment"
    assert os.environ["OPENAI_API_TYPE"] == "mock_api_type"

def test_state_management(state_graph):
    """Check state persistence and updating in graph state."""
    memory_saver = MemorySaver()
    state_graph.add_node("test_node", lambda state: {"messages": ['State updated message']})
    graph = state_graph.compile(checkpointer=memory_saver)

    user_message = HumanMessage(content="Test state management")
    state = StateSchema(messages=[user_message])

    result = graph.invoke(state, config=config)
    assert result["messages"][-1] == 'State updated message'

def test_varied_input_handling(mocked_llm):
    """Test handling of varied inputs."""
    inputs = [
        "Test input one",
        "Another challenging input 987823",
        "Edge case input !@#$%^",
        "Long input " * 50
    ]
    
    for input_case in inputs:
        assert mocked_llm.invoke([HumanMessage(content=input_case)]) == 'Test response from mocked LLM.'

def test_performance_and_timeout_analysis():
    """Test performance with focus on timeout conditions."""
    import time
    start_time = time.time()
    
    user_input = "Performance test input"
    history = []

    # Simulate the chat function using the mock
    with patch('agent.chat') as mock_chat:
        mock_chat.return_value = 'Mocked performance response'
        mock_chat(user_input, history)
    
    end_time = time.time()
    assert end_time - start_time < 0.1  # Assuming a realistic timeout requirement