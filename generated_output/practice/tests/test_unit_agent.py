
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
# test_agent.py
import pytest
from unittest.mock import patch, Mock
from pydantic import ValidationError
from agent import State, chat


@pytest.fixture
def valid_state_messages():
    """Fixture representing a sample valid state messages list."""
    return [
        {"type": "system", "content": "You are a flight booking assistant."},
        {"type": "user", "content": "I would like to book a flight to Paris."}
    ]


@pytest.fixture
def invalid_state_messages():
    """Fixture representing an invalid state messages list."""
    return [
        {"type": "undefined", "content": "This is not a valid message type."}
    ]


def test_state_initialization_happy_path(valid_state_messages):
    """Test State initialization with valid messages should succeed."""
    state = State(messages=valid_state_messages)
    assert len(state.messages) == 2
    assert state.messages[0].type == "system"
    assert state.messages[1].type == "user"


def test_state_initialization_invalid_input(invalid_state_messages):
    """Test State initialization with invalid messages should raise ValidationError."""
    with pytest.raises(ValidationError):
        State(messages=invalid_state_messages)


def test_chatbot_function_happy_path(valid_state_messages):
    """Test chatbot function behaves correctly with typical input using mock."""
    with patch('agent.llm.invoke', return_value=Mock(content="Flight booked to Paris")) as mock_invoke:
        state = State(messages=valid_state_messages)
        result = chat("I would like to book a flight to Paris", [])
        mock_invoke.assert_called_once_with(state.messages)
        assert result == "Flight booked to Paris"


def test_chatbot_function_edge_case_empty_message():
    """Test chatbot function with empty message scenarios for graceful handling."""
    with patch('agent.llm.invoke', return_value=Mock(content="Please provide more details")) as mock_invoke:
        result = chat("", [])
        mock_invoke.assert_called_once()
        assert result == "Please provide more details"


def test_chatbot_function_edge_case_long_message():
    """Test chatbot with very long user message input for robustness."""
    long_message = "a" * 1000
    with patch('agent.llm.invoke', return_value=Mock(content="Message too long to process")) as mock_invoke:
        result = chat(long_message, [])
        mock_invoke.assert_called_once()
        assert result == "Message too long to process"


def test_chatbot_function_with_memory():
    """Test chatbot function ensuring it handles history appropriately."""
    history = [
        {"type": "user", "content": "Previous booking: Flight to London"}
    ]
    with patch('agent.llm.invoke', return_value=Mock(content="Continuing from previous booking history")) as mock_invoke:
        result = chat("What's my last booking?", history)
        mock_invoke.assert_called_once()
        assert result == "Continuing from previous booking history"


def test_chatbot_function_error_handling():
    """Test chatbot handles errors from the underlying service gracefully."""
    with patch('agent.llm.invoke', side_effect=Exception("API error")) as mock_invoke:
        try:
            result = chat("I would like to book a flight", [])
        except Exception as e:
            assert str(e) == "API error"
        mock_invoke.assert_called_once()
    

# Add more parameterized tests if needed to cover various input scenarios
@pytest.mark.parametrize("user_input,expected_output", [
    ("Find flights to Berlin", "Flights found to Berlin"),
    ("Check my flight status", "Your flight status is on time"),
])
def test_chat_parameterized(user_input, expected_output):
    """Parameterized test for chat functionality with different inputs."""
    with patch('agent.llm.invoke', return_value=Mock(content=expected_output)) as mock_invoke:
        result = chat(user_input, [])
        mock_invoke.assert_called_once()
        assert result == expected_output


# Run the tests using pytest.
# Ensure you have pytest and pytest-mock available in your environment.
# Use `pytest test_agent.py` to run the tests.