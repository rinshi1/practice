
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, Mock
from agent import chat, State, graph, llm, graph_builder  # Assuming the module is named agent.py
from langchain.schema import HumanMessage, SystemMessage

# Fixtures for consistent test setup
@pytest.fixture
def mock_llm_invoke():
    """Mock the AzureChatOpenAI invoke method."""
    return patch.object(llm, 'invoke', return_value=Mock(content="Sample response from mock LLM"))

@pytest.fixture
def sample_state():
    """Provide a sample State instance for testing."""
    user_message = HumanMessage(content="Sample user input")
    system_message = SystemMessage(
        content="You are a flight booking assistant for a travel agency. Your role is to assist with booking flights, providing timely updates, adhering to all safety protocols, and maintaining a high standard of observability for ongoing interactions. You are equipped to maintain long-term memory for the user's preferences and past interactions to ensure a personalized experience."
    )
    messages = [system_message, user_message]
    return State(messages=messages)

@pytest.fixture
def sample_config():
    """Provide a sample configuration."""
    return {"configurable": {"thread_id": "1"}}

# Test the chatbot function within the graph
def test_chatbot_function_happy_path(sample_state, mock_llm_invoke):
    """Test the happy path of the chatbot function ensuring it returns a result as expected."""
    with mock_llm_invoke as mock_invoke:
        result = graph.invoke(sample_state, config={"configurable": {"thread_id": "1"}})
        assert result is not None
        assert isinstance(result["messages"], list)
        assert result["messages"][-1].content == "Sample response from mock LLM"
        mock_invoke.assert_called_once_with(sample_state.messages)

# Test the chat function with typical input
def test_chat_typical_input(mock_llm_invoke):
    """Test the chat function with a typical user input scenario."""
    user_input = "I want to book a flight to New York."
    history = []  # Assuming history is an empty list for simplicity
    with mock_llm_invoke as mock_invoke:
        response = chat(user_input, history)
        assert response == "Sample response from mock LLM"
        mock_invoke.assert_called_once()

# Test the chat function with empty input (edge case)
def test_chat_empty_input(mock_llm_invoke):
    """Test the chat function with empty user input to ensure it handles it robustly."""
    user_input = ""
    history = [] 
    with mock_llm_invoke as mock_invoke:
        response = chat(user_input, history)
        assert response == "Sample response from mock LLM"
        mock_invoke.assert_called_once()

# Test for exception handling when LLM invocation fails
def test_llm_invoke_failure():
    """Test if the system gracefully handles errors during LLM invocation."""
    user_input = "How can I get to the airport?"
    history = []
    with patch.object(llm, 'invoke', side_effect=Exception("LLM invoke failure")):
        try:
            response = chat(user_input, history)
        except Exception as e:
            assert str(e) == "LLM invoke failure"

# Test the State model creation and message assignment
def test_state_message_assignment():
    """Test that the State model correctly assigns messages."""
    user_message = HumanMessage(content="Test message")
    sys_message = SystemMessage(content="Test system message")
    state = State(messages=[sys_message, user_message])
    assert state.messages[0].content == "Test system message"
    assert state.messages[1].content == "Test message"