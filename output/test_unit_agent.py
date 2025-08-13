
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from agent import chat, State, graph_builder, llm, chatbot, config
from langchain.schema import HumanMessage, SystemMessage


@pytest.fixture
def mock_llm_invoke():
    """Fixture to mock the AzureChatOpenAI invoke method."""
    with patch.object(llm, 'invoke', return_value=SystemMessage(content="Mock response")) as mock_invoke:
        yield mock_invoke

@pytest.fixture
def basic_state():
    """Fixture to provide a basic State object with mocked messages."""
    return State(messages=[
        SystemMessage(content="Mock system message"),
        HumanMessage(content="Mock user message")
    ])

def test_chat_typical_input(mock_llm_invoke):
    """Test chat function with typical user input."""
    user_input = "I want to book a flight to New York"
    expected_response = "Mock response"
    
    response = chat(user_input, history=[])
    
    assert response == expected_response
    mock_llm_invoke.assert_called_once()

def test_chat_handles_empty_input(mock_llm_invoke):
    """Test chat function with empty user input."""
    user_input = ""
    expected_response = "Mock response"
    
    response = chat(user_input, history=[])
    
    assert response == expected_response
    mock_llm_invoke.assert_called_once()

def test_chat_handles_special_characters(mock_llm_invoke):
    """Test chat function with special characters in user input."""
    user_input = "@#$%^&*"
    expected_response = "Mock response"
    
    response = chat(user_input, history=[])
    
    assert response == expected_response
    mock_llm_invoke.assert_called_once()

def test_state_initialization_with_messages(basic_state):
    """Test State object initialization with expected messages."""
    assert isinstance(basic_state.messages, list)
    assert len(basic_state.messages) == 2
    assert isinstance(basic_state.messages[0], SystemMessage)
    assert isinstance(basic_state.messages[1], HumanMessage)

def test_chatbot_function(mock_llm_invoke, basic_state):
    """Test chatbot function processing a basic state."""
    result = chatbot(basic_state)
    
    assert 'messages' in result
    assert isinstance(result['messages'], list)
    assert isinstance(result['messages'][-1], SystemMessage)
    mock_llm_invoke.assert_called_once()

def test_graph_builder_edges():
    """Test graph builder edge connections."""
    assert graph_builder.has_edge(graph_builder.start_node, "chatbot")
    assert graph_builder.has_edge("chatbot", graph_builder.end_node)

@pytest.mark.parametrize("input_message, expected_call_count", [
    ("I need your help", 1),
    ("Tell me more about your services", 1),
    ("Goodbye", 1)
])
def test_chat_varied_inputs(mock_llm_invoke, input_message, expected_call_count):
    """Test chat function with parameterized user inputs."""
    response = chat(input_message, history=[])
    
    assert response == "Mock response"
    assert mock_llm_invoke.call_count == expected_call_count


# Additional tests can be added to further exercise the edge cases and errors