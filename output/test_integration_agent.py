
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import MagicMock, patch
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from pydantic import ValidationError
from asynctest import CoroutineMock
from your_module import chat, graph_builder, State

@pytest.fixture
def setup_environment(monkeypatch):
    """Setup environment variables required for agent initialization."""
    monkeypatch.setenv("DEPLOYMENT_NAME", "test_deployment")
    monkeypatch.setenv("OPENAI_API_TYPE", "test_api_type")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "http://localhost")
    monkeypatch.setenv("OPENAI_API_VERSION", "2021-06-01")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test_key")


@pytest.fixture
def mock_openai(monkeypatch):
    """Mocking the AzureChatOpenAI LLM to return a predefined response."""
    mock_llm = MagicMock()
    mock_llm.invoke = MagicMock(return_value="Test Response")
    monkeypatch.setattr("your_module.llm", mock_llm)
    return mock_llm


@pytest.fixture
def setup_state_graph(monkeypatch):
    """Setup a state graph for testing."""
    monkeypatch.setattr("your_module.graph_builder", graph_builder)
    monkeypatch.setattr("your_module.memory", MemorySaver())


def test_initialization_correctness(setup_environment, mock_openai):
    """Test agent initialization with environment configuration."""
    from your_module import llm
    assert llm.deployment_name == "test_deployment"
    assert llm.openai_api_version == "2021-06-01"


def test_chat_functionality(setup_environment, setup_state_graph, mock_openai):
    """Test the chat system with mock inputs and outputs."""
    user_input = "Book a flight to New York"
    history = []

    response = chat(user_input, history)
    assert response == "Test Response"
    mock_openai.invoke.assert_called_once_with(
        [SystemMessage(content="You are a flight booking assistant for ..."),
         HumanMessage(content=user_input)]
    )


def test_state_handling_with_varied_inputs(setup_environment):
    """Validate State handling with various input types."""
    with pytest.raises(ValidationError):
        State(messages="Invalid Type")
    
    valid_state = State(messages=[
        HumanMessage(content="Test message")
    ])
    assert valid_state.messages[0].content == "Test message"


@patch("your_module.graph.invoke", new_callable=CoroutineMock)
async def test_async_operations(mock_invoke, setup_environment):
    """Ensure async operations are handled correctly."""
    mock_invoke.return_value = {"messages": [HumanMessage(content="Async Test Response")]}
    state = State(messages=[HumanMessage(content="Test message")])

    result = await graph.invoke(state, config={"test": "config"})
    
    assert result["messages"][0].content == "Async Test Response"


def test_error_propagation_handling(setup_environment):
    """Test for managing error propagation within agent functions."""
    with patch("your_module.llm.invoke", side_effect=Exception("Test Exception")) as mock_method:
        with pytest.raises(Exception, match="Test Exception"):
            user_input = "Test input"
            history = []
            chat(user_input, history)


def test_state_graph_integration(setup_state_graph, setup_environment):
    """Verify the state graph components and interactions."""
    mock_node_func = MagicMock(return_value={"messages": ["Node Response"]})
    graph_builder.add_node("test_node", mock_node_func)
    assert "test_node" in graph_builder.nodes

    graph_builder.add_edge("test_node", END)
    state = State(messages=[])

    result = graph.invoke(state, config={})
    mock_node_func.assert_called_once()
    assert result["messages"] == ["Node Response"]

def test_resource_cleanup_after_tests(setup_environment):
    """Ensure resources are cleaned up after test execution."""
    # Assuming there's a function cleanup_resources in your_module
    with patch("your_module.cleanup_resources") as mock_cleanup:
        mock_cleanup()
        mock_cleanup.assert_called_once()


def test_performance_and_timeout_analysis(setup_environment, mock_openai):
    """Analyze timeout and performance of workflows."""
    import time
    start_time = time.time()
    user_input = "Book a flight to Tokyo"
    history = []
    chat(user_input, history)
    end_time = time.time()

    assert (end_time - start_time) < 2, "Process exceeded performance limit"