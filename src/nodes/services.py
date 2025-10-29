import dotenv
import os
dotenv.load_dotenv("../.env")

from langchain_groq import ChatGroq
from langchain.messages import AIMessage, HumanMessage, SystemMessage

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

from .models import Chat, Node, NodeType

from typing import List, Tuple

class LLMService:
    def __init__(self, model="deepseek-r1-distill-llama-70b", tools=None):
        self.llm = ChatGroq(
            model=model,
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
        )
        if self.tools:
            # Integrate tools with the LLM if provided
            self.llm = self.llm.bind_tools(self.tools)

        self.graph = self.build_graph()

    def build_graph(self):

        def llm_node(messages: MessagesState):
            return {"messages": self.llm.invoke(messages)}
        
        def call_tools(state: MessagesState):
            messages = state.messages
            last_message = messages.messages[-1]
            if not last_message.tool_calls:
                return "end"
            else:
                return "call_tools"

        graph = StateGraph(MessagesState)
        graph.add_node("llm", llm_node)
        graph.add_edge(START, "llm")
        if self.tools:
            graph.add_conditional_edges("llm", call_tools, {
                "call_tools": ToolNode(tools=self.tools),
                "end": END
            })
            graph.add_edge("call_tools", "llm")
        else:
            graph.add_edge("llm", END)
        graph = graph.compile()
        return graph

    async def get_response(self, state: MessagesState):
        result = self.graph.invoke(state)
        return result
    
    def generate_history(self, lineage: List[dict]) -> MessagesState:
        messages: List = []
        for item in lineage:
            node_type = item.get("node_type")
            content = item.get("content")
            if node_type == NodeType.SYSTEM:
                messages.append(SystemMessage(content=content))
            elif node_type == NodeType.USER:
                messages.append(HumanMessage(content=content))
            elif node_type == NodeType.LLM:
                messages.append(AIMessage(content=content))
        return MessagesState(messages=messages)
    
class ChatGraphService:
    @classmethod
    def get_chat_graph(cls, chat_id):
        nodes: List = []
        edges: List[Tuple] = []

        parent_node = chat_id.parent_node

        def traverse_node(node: Node):
            nodes.append({
                "id": node.id,
                "name": node.name,
                "content": node.content,
                "node_type": node.node_type,
            })
            for child in node.get_children():
                edges.append((node.id, child.id))
                traverse_node(child)

        traverse_node(parent_node)
        return {"nodes": nodes, "edges": edges}

    @classmethod
    def get_lineage(cls, node=None, node_id=None):
        if not node and not node_id:
            raise ValueError("Either node or node_id must be provided.")

        lineage: List = []

        if not node:
            node = Node.objects.get(id=node_id)

        def traverse_up(node: Node):
            if node is None:
                return
            lineage.append({
                "id": node.id,
                "name": node.name,
                "content": node.content,
                "node_type": node.node_type,
            })
            traverse_up(node.get_parent())

        traverse_up(node)
        lineage.reverse()
        return lineage
