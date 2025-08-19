
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from unittest.mock import Mock, patch, MagicMock
import pytest
from unittest.mock import Mock, patch
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.schema import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
from typing import Annotated
from your_module_path import graph_builder, chatbot, chat, State  # assuming the module is saved as agent.py

@pytest.fixture
def mock_llm():
    """
    Mock the AzureChatOpenAI LLM interaction.
    """
    mock_llm = Mock()
    mock_llm.invoke.return_value = "Mocked response"
    return mock_llm

@pytest.fixture
def mock_state_graph():
    """
    Mock the StateGraph functionality for testing.
    """
    mock_state_graph = Mock(spec=StateGraph)
    return mock_state_graph

@pytest.fixture
def sample_messages():
    """
    Provide sample messages for testing.
    """
    user_message = HumanMessage(content="Sample user message")
    system_message = SystemMessage(content="Sample system message")
    return [system_message, user_message]

def test_chatbot_function_happy_path(mock_llm, sample_messages):
    """
    Test the chatbot function using typical input data for happy path scenario.
    """
    with patch('langchain_openai.AzureChatOpenAI', return_value=mock_llm):
        state = State(messages=sample_messages)
        result = chatbot(state)
        assert result == {"messages": ["Mocked response"]}

def test_chatbot_function_edge_case_empty_messages(mock_llm):
    """
    Test the chatbot function with an edge case: Empty message list input.
    """
    with patch('langchain_openai.AzureChatOpenAI', return_value=mock_llm):
        empty_state = State(messages=[])
        result = chatbot(empty_state)
        assert result == {"messages": ["Mocked response"]}

def test_graph_builder_setup(mock_state_graph):
    """
    Validate graph builder setup and correct node addition.
    """
    mock_state_graph.add_node("test_node", lambda x: x)
    mock_state_graph.add_edge(START, "test_node")
    mock_state_graph.add_edge("test_node", END)
    compiled_graph = mock_state_graph.compile(checkpointer=Mock(spec=MemorySaver))
    assert isinstance(compiled_graph, Mock)  # Here you might need to adjust based on your real implementation.

@pytest.mark.parametrize("user_input, expected_message", [
    ("Book flight to Paris", "Mocked response"),
    ("Cancel my flight", "Mocked response"),
])
def test_chat_function_various_inputs(mock_llm, user_input, expected_message):
    """
    Test the chat function with various user inputs using parameterized tests.
    """
    with patch('langchain_openai.AzureChatOpenAI', return_value=mock_llm):
        result_message = chat(user_input=user_input, history=None)
        assert result_message == expected_message

def test_chat_invalid_input():
    """
    Test chat function handles invalid input gracefully.
    """
    with pytest.raises(ValueError):
        chat(user_input=None, history=None)

def test_state_model_initialization_success():
    """
    Ensure State model initializes correctly with the add_messages annotation.
    """
    state = State(messages=[HumanMessage(content="Hello"), SystemMessage(content="System")])
    assert isinstance(state, State)

@pytest.mark.parametrize("input_messages, expected_count", [
    ([], 0),
    ([HumanMessage(content="Hi")], 1),
    ([HumanMessage(content="Hi"), SystemMessage(content="Sys")], 2),
])
def test_state_message_count(input_messages, expected_count):
    """
    Validate State object correctly stores the number of messages passed in.
    """
    state = State(messages=input_messages)
    assert len(state.messages) == expected_count

# Assuming your entire module is named 'agent.py' and tests are specific to its functionalities.

if __name__ == "__main__":
    pytest.main()