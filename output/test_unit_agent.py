
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from agent import chat, State, graph_builder
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from pydantic import ValidationError

@pytest.fixture
def mock_llm():
    """Fixture to mock the AzureChatOpenAI instance."""
    with patch('agent.AzureChatOpenAI') as MockLLM:
        instance = MockLLM.return_value
        instance.invoke.return_value = MagicMock()
        yield instance

@pytest.fixture
def mock_graph_builder():
    """Fixture to mock the 'graph_builder' instance."""
    with patch('agent.graph_builder') as MockGraphBuilder:
        mock_graph = MagicMock()
        MockGraphBuilder.compile.return_value = mock_graph
        yield mock_graph

def test_chat_happy_path(mock_llm, mock_graph_builder):
    """Test chat function with typical user input and history."""
    mock_message = MagicMock()
    mock_message.content = "Hello! I'm here to help you with flight booking."
    mock_llm.invoke.return_value = mock_message

    user_input = "I want to book a flight to Paris"
    history = []

    expected_response = "Hello! I'm here to help you with flight booking."

    response = chat(user_input, history)
    assert response == expected_response

def test_chat_with_empty_input(mock_llm, mock_graph_builder):
    """Test chat function with empty user input."""
    mock_message = MagicMock()
    mock_message.content = "You entered empty input."
    mock_llm.invoke.return_value = mock_message

    user_input = ""
    history = []

    expected_response = "You entered empty input."

    response = chat(user_input, history)
    assert response == expected_response

def test_chat_edge_case_long_input(mock_llm, mock_graph_builder):
    """Test chat function with long user input text."""
    mock_message = MagicMock()
    mock_message.content = "Your input is too long to process."
    mock_llm.invoke.return_value = mock_message

    user_input = "a" * 10000
    history = []

    expected_response = "Your input is too long to process."

    response = chat(user_input, history)
    assert response == expected_response

def test_chat_invalid_state(mock_graph_builder):
    """Test chat function handling of invalid State."""
    user_input = "I want to book a flight"
    history = []
    
    with patch('agent.State') as MockState:
        MockState.side_effect = ValidationError([], State)
        
        with pytest.raises(ValidationError):
            chat(user_input, history)

def test_state_initialization():
    """Test initialization of State with valid messages."""
    messages = [SystemMessage(content="System content"), HumanMessage(content="Human content")]
    
    state = State(messages=messages)
    assert state.messages == messages

def test_state_initialization_invalid():
    """Test State initialization with invalid messages raising a ValidationError."""
    messages = [None, "Invalid Message"]
    
    with pytest.raises(ValidationError):
        State(messages=messages)

def test_graph_builder_add_node():
    """Test graph_builder's capability to add nodes."""
    graph_builder.add_node("new_node", lambda x: x)
    assert "new_node" in graph_builder.nodes

def test_graph_builder_add_edge():
    """Test graph_builder's capability to add edges."""
    graph_builder.add_edge("test_start", "test_end")
    assert ("test_start", "test_end") in graph_builder.edges

@pytest.mark.parametrize("user_input,expected_response", [
    ("Help me book a flight to New York", "Assistant response for booking flight to New York"),
    ("Get me a flight", "Assistant response for flight booking"),
])
def test_chat_parameterized(mock_llm, user_input, expected_response):
    """Parameterized test for chat function with various user inputs."""
    mock_message = MagicMock()
    mock_message.content = expected_response
    mock_llm.invoke.return_value = mock_message

    history = []
    
    response = chat(user_input, history)
    assert response == expected_response