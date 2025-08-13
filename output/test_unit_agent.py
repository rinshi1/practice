
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from agent import State, chat, graph, MemorySaver
from langchain.schema import HumanMessage, SystemMessage

# Fixtures for setup
@pytest.fixture
def valid_user_input():
    return "I want to book a flight to New York."

@pytest.fixture
def message_history():
    return []

@pytest.fixture
def state_graph():
    messages = [
        SystemMessage(content="You are a flight booking assistant."),
        HumanMessage(content="I want to book a flight.")
    ]
    return State(messages=messages)

@pytest.fixture
def mock_llm_invoke():
    with patch('agent.llm.invoke') as mock_invoke:
        mock_invoke.return_value = HumanMessage(content="Booking flight to New York is confirmed.")
        yield mock_invoke

@pytest.fixture
def mock_memory_saver():
    with patch('agent.MemorySaver') as mock_memory:
        yield mock_memory

# Test cases

def test_state_initialization(state_graph):
    """Test the State initialization with annotated messages."""
    assert isinstance(state_graph, State)
    assert len(state_graph.messages) == 2
    assert isinstance(state_graph.messages[0], SystemMessage)
    assert isinstance(state_graph.messages[1], HumanMessage)

def test_chatbot_node(mock_llm_invoke, state_graph):
    """Test if chatbot node processes state and returns correct output."""
    response = graph.invoke(state_graph, config={"configurable": {"thread_id": "1"}})
    assert "messages" in response
    assert response["messages"][-1].content == "Booking flight to New York is confirmed."
    mock_llm_invoke.assert_called_once_with(state_graph.messages)

def test_chat_function(valid_user_input, message_history, mock_llm_invoke):
    """Test the chat function for valid input and expected output."""
    result = chat(valid_user_input, message_history)
    assert result == "Booking flight to New York is confirmed."
    mock_llm_invoke.assert_called_once()

@pytest.mark.parametrize("input_text, expected_message", [
    ("Book a flight to Paris.", "Booking flight to Paris is confirmed."),
    ("Cancel my booking.", "Your booking has been cancelled.")
])
def test_chat_multiple_inputs(input_text, expected_message, mock_llm_invoke):
    """Test chat function with multiple inputs."""
    mock_llm_invoke.return_value = HumanMessage(content=expected_message)
    message_history = []
    result = chat(input_text, message_history)
    assert result == expected_message
    mock_llm_invoke.assert_called_once()

def test_error_handling_in_chat():
    """Test chat function capturing errors properly."""
    with patch('agent.graph.invoke', side_effect=Exception("Error during processing")):
        with pytest.raises(Exception, match="Error during processing"):
            chat("Trigger error", [])

# Ensure MemorySaver is functioning properly
def test_memory_saver_usage(mock_memory_saver):
    """Test to ensure MemorySaver is utilized correctly."""
    memory_instance = MemorySaver()
    assert memory_instance is not None

# To run your tests, you would typically use the command:
# pytest -v test_agent.py