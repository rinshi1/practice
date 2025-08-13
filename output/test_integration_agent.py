
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import patch, MagicMock
from pydantic import BaseModel, ValidationError
from langchain_openai import AzureChatOpenAI
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

@pytest.fixture(scope="module")
def environment_setup():
    with patch('os.getenv', return_value='test_value'):
        yield
    # Teardown any modifications to environment variables if needed


@pytest.fixture
def mock_openai():
    with patch('langchain_openai.AzureChatOpenAI', autospec=True) as mock_openai_class:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "Mocked response"
        mock_openai_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def state_input():
    user_message = HumanMessage(content="Test user input")
    system_message = SystemMessage(content="You are a flight booking assistant for a travel agency. Your role...")
    messages = [system_message, user_message]
    return State(messages=messages)


def test_agent_initialization(mock_openai, environment_setup):
    """Ensure the agent initializes correctly with environment variables."""
    config = {"configurable": {"thread_id": "1"}}
    state_graph = StateGraph(State)
    assert isinstance(state_graph, StateGraph)
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", lambda state: {'messages': [mock_openai.invoke(state.messages)]})
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    assert graph.start_node == START
    assert graph.end_node == END


def test_full_workflow_execution(state_input):
    """Test a complete workflow from start to finish."""
    config = {"configurable": {"thread_id": "1"}}
    memory = MemorySaver()
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile(checkpointer=memory)
    result = graph.invoke(state_input, config=config)
    assert result["messages"][-1].content == "Mocked response"


def test_component_interaction(mock_openai):
    """Ensure inter-component interactions are smoothly handled."""
    state = State(messages=[HumanMessage(content="Test input"), SystemMessage(content="System message")])
    assert state.messages[0].content == "System message"
    assert state.messages[1].content == "Test input"

    response = mock_openai.invoke(state.messages)
    assert response == "Mocked response"


def test_error_propagation():
    """Check system behavior on invalid input using Pydantic validation."""
    with pytest.raises(ValidationError):
        # Create an invalid state object
        invalid_state = State(messages=[HumanMessage(content=None)])
        invalid_state.validate()


@pytest.mark.asyncio
async def test_async_operations(mock_openai, state_input):
    """Verify that asynchronous operations are properly handled."""
    async def async_chatbot(state):
        return {"messages": [await mock_openai.invoke(state.messages)]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("async_chatbot", async_chatbot)
    graph_builder.add_edge(START, "async_chatbot")
    graph_builder.add_edge("async_chatbot", END)
    graph = graph_builder.compile(checkpointer=MemorySaver())

    result = await graph.invoke(state_input, config={"configurable": {"thread_id": "1"}})
    assert result["messages"][-1].content == "Mocked response"


def test_state_management_checks(state_input):
    """Ensure state persistence and updates are as expected."""
    config = {"configurable": {"thread_id": "1"}}
    memory = MemorySaver()
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile(checkpointer=memory)
    result = graph.invoke(state_input, config=config)
    assert result["messages"][-1].content == "Mocked response"
    assert memory.get_state("chatbot") is not None


def test_varied_input_scenarios():
    """Handle a variety of inputs and validate expected outcomes."""
    inputs = [
        "What is the best flight option?",
        "",
        "How do I book a ticket?",
        "Need help with booking"
    ]

    for user_input in inputs:
        state = State(messages=[HumanMessage(content=user_input), SystemMessage(content="System Prompt")])
        result = graph.invoke(state, config={"configurable": {"thread_id": "1"}})
        assert isinstance(result, dict)
        assert 'messages' in result


def test_performance_and_timeout_analysis(mock_openai, state_input):
    """Assess performance and verify functionality within timeout constraints."""
    import time

    start_time = time.time()
    result = chatbot(state_input)
    end_time = time.time()

    duration = end_time - start_time
    assert duration < 2  # asserting the response time is less than 2 seconds
    assert result["messages"][-1] == "Mocked response"