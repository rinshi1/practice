
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from agent import graph_builder, chat
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import asyncio

@pytest.fixture(scope="module")
def setup_environment():
    # Setup any necessary environment variables for the tests
    os.environ["DEPLOYMENT_NAME"] = "test_deployment"
    os.environ["OPENAI_API_TYPE"] = "test_api_type"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "test_endpoint"
    os.environ["OPENAI_API_VERSION"] = "test_version"
    os.environ["AZURE_OPENAI_API_KEY"] = "test_api_key"
    yield
    # Teardown any created resources or environment settings if needed

@pytest.fixture(scope="module")
def mock_azure_openai():
    # Mock the AzureChatOpenAI initialization to handle message invoking
    with patch('agent.AzureChatOpenAI') as MockAzureChatOpenAI:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = SystemMessage(content="Test Response")
        MockAzureChatOpenAI.return_value = mock_llm
        yield mock_llm

def test_chatbot_workflow(mock_azure_openai):
    state = State(messages=[HumanMessage(content="Test User Input")])
    response = graph_builder.invoke(state)
    
    # Test correct invocation flow
    assert "chatbot" in state.messages
    assert response.messages[-1].content == "Test Response"
    
def test_chat_endpoint(mock_azure_openai):
    user_input = "Book Flight"
    history = []
    
    response_message = chat(user_input, history)
    
    # Validate correct system message handling
    assert response_message == "Test Response"

@pytest.mark.asyncio
async def test_async_operations(mock_azure_openai):
    async def async_chat(*args):
        return chat(*args)
    
    user_input = "Check booking"
    history = []

    # Using asyncio to test async operations
    awaited_response = await async_chat(user_input, history)
    
    assert awaited_response == "Test Response"

def test_configuration_and_environment(setup_environment):
    expected_config = {
        "DEPLOYMENT_NAME": "test_deployment",
        "OPENAI_API_TYPE": "test_api_type",
        "AZURE_OPENAI_ENDPOINT": "test_endpoint",
        "OPENAI_API_VERSION": "test_version",
        "AZURE_OPENAI_API_KEY": "test_api_key",
    }
    
    for key, value in expected_config.items():
        assert os.environ[key] == value

def test_state_management(mock_azure_openai):
    state_before = MemorySaver()

    # Simulate persisting state across interactions
    state_messages = [HumanMessage(content="Querying State")]
    state = State(messages=state_messages)

    mock_memory_saver = MemorySaver()
    response = graph_builder.invoke(state, checkpointer=mock_memory_saver)

    # Validate state persistence and updates
    assert mock_memory_saver.messages == state_messages

def test_varied_input_scenarios(mock_azure_openai):
    inputs_and_expected = [
        ("Find flights", "Test Response"),
        ("Cancel booking", "Test Response"),
        ("Reschedule flight", "Test Response")
    ]
    
    for user_input, expected_response in inputs_and_expected:
        response = chat(user_input, [])
        assert response == expected_response

def test_performance_and_timeout_analysis():
    user_input = "Performance test"
    history = []

    # Measure time taken for function execution
    start_time = asyncio.get_event_loop().time()
    chat(user_input, history)
    end_time = asyncio.get_event_loop().time()
    
    assert end_time - start_time < 2.0  # Ensure the response within 2 seconds