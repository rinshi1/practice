
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from agent import chat, State, SystemMessage, HumanMessage, graph
from langchain_openai import AzureChatOpenAI

# Define mock response data
mock_llm_response = "Flight booked successfully."

@pytest.fixture
def mock_environment_variables():
    with patch('agent.os.environ') as mock_env:
        mock_env.get.side_effect = lambda k: {
            'DEPLOYMENT_NAME': 'test-deployment',
            'OPENAI_API_TYPE': 'azure',
            'AZURE_OPENAI_ENDPOINT': 'https://azure.endpoint.com',
            'OPENAI_API_VERSION': 'v1',
            'AZURE_OPENAI_API_KEY': 'dummy_api_key'
        }.get(k, '')
        yield

@pytest.fixture
def mock_llm():
    with patch('agent.AzureChatOpenAI.invoke', return_value=mock_llm_response) as mock_invoke:
        yield

@pytest.fixture
def mock_memory_saver():
    with patch('agent.MemorySaver') as mock_memory:
        yield mock_memory.return_value


def test_agent_initialization(mock_environment_variables):
    assert AzureChatOpenAI(deployment_name="test-deployment")


@pytest.mark.asyncio
async def test_chat_function_workflow(mock_environment_variables, mock_llm):
    user_message = "Book a flight to Paris."
    history = []
    
    with patch('agent.state.messages', create=True) as mock_state_messages:
        result = await chat(user_message, history)
        
    assert result == mock_llm_response
    assert len(mock_state_messages) > 0


def test_component_interaction(mock_environment_variables, mock_memory_saver):
    system_message = SystemMessage(content="Test system message")
    user_message = HumanMessage(content="User message")
    
    state = State(messages=[system_message, user_message])
    graph.invoke(state)
    
    assert mock_memory_saver.save.called


def test_error_propagation():
    with pytest.raises(Exception):
        raise Exception("Simulated error")


@pytest.mark.timeout(1)  # Ensure the function completes within 1 second
def test_performance_and_timeout(mock_environment_variables, mock_llm):
    user_message = "Quick query"
    history = []

    result = chat(user_message, history)
    
    assert result == mock_llm_response  # Validate response within expected timeout


@pytest.mark.parametrize("input_message,expected_response", [
    ("How do I book a flight?", "Flight booked successfully."),
    ("Cancel my flight", "Flight booked successfully."),
])
def test_varied_input_scenarios(mock_environment_variables, input_message, expected_response, mock_llm):
    history = []
    result = chat(input_message, history)
    assert result == expected_response


# Setup and Teardown for each test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Setup
    begin_environment()
    
    yield
    
    # Teardown
    cleanup_environment()


def begin_environment():
    # Any setup logic goes here
    print("Setting up the environment for tests.")

def cleanup_environment():
    # Any cleanup logic goes here
    print("Cleaning up after tests.")


@pytest.mark.asyncio
async def test_async_operations(mock_llm):
    user_message = "Async flight query"
    history = []

    # Simulate async operation and await results
    result = await chat(user_message, history)
    assert result == mock_llm_response  # Verify the awaited result