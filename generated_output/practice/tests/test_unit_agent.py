
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, Mock
from agent import chat  # Assuming import from agent.py
from langchain.schema import HumanMessage, SystemMessage

@pytest.fixture
def mock_llm():
    """Fixture to mock the AzureChatOpenAI instance."""
    with patch('agent.llm') as mock_llm:
        yield mock_llm

def test_chatbot_happy_path(mock_llm):
    """Test chatbot function with happy path input."""
    mock_llm.invoke.return_value = SystemMessage(content="Booking confirmed!")  # Mocked response

    state = State(messages=[SystemMessage(content="System"), HumanMessage(content="User")])
    result = chatbot(state)

    assert result["messages"] == [SystemMessage(content="Booking confirmed!")]

def test_chat_happy_path(mock_llm):
    """Test chat function for standard user input."""
    mock_llm.invoke.return_value = SystemMessage(content="Booking confirmed!")

    history = []  # Sample history, adjust based on what `chat` expects
    user_input = "I would like to book a flight to Paris."

    result = chat(user_input, history)

    assert result == "Booking confirmed!"

def test_chat_empty_user_input(mock_llm):
    """Test chat functionality with an empty user input string."""
    mock_llm.invoke.return_value = SystemMessage(content="Please provide your destination.")

    history = []  # Adjust based on expected structure
    user_input = ""

    result = chat(user_input, history)

    assert result == "Please provide your destination."

def test_chat_error_handling(mock_llm):
    """Test chatbot and chat function raises an error on invalid data."""
    # Simulating an error in invoke
    mock_llm.invoke.side_effect = Exception("API Error")

    user_input = "Error prompt"
    history = []

    with pytest.raises(Exception, match="API Error"):
        chat(user_input, history)

def test_environment_variables():
    """Test that environment variables are loaded correctly."""
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda k: {"DEPLOYMENT_NAME": "test_deploy", 
                                             "OPENAI_API_TYPE": "test_type",
                                             "AZURE_OPENAI_ENDPOINT": "test_endpoint",
                                             "OPENAI_API_VERSION": "test_version",
                                             "AZURE_OPENAI_API_KEY": "test_key"}.get(k, None)
        import agent  # Trigger re-import for patched values

        assert os.environ["DEPLOYMENT_NAME"] == "test_deploy"
        assert os.environ["OPENAI_API_TYPE"] == "test_type"
        assert os.environ["AZURE_OPENAI_ENDPOINT"] == "test_endpoint"
        assert os.environ["OPENAI_API_VERSION"] == "test_version"
        assert os.environ["AZURE_OPENAI_API_KEY"] == "test_key"

@pytest.mark.parametrize("input_data,expected_response", [
    ("I want to book a flight to New York.", "Booking confirmed!"),
    ("Can you find me tickets to London?", "Booking confirmed!"),
])
def test_chat_multiple_inputs(mock_llm, input_data, expected_response):
    """Parameterized test for multiple user inputs."""
    mock_llm.invoke.return_value = SystemMessage(content=expected_response)

    history = []  # Adjust based on how history should be handled
    result = chat(input_data, history)

    assert result == expected_response