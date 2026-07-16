"""STARs RAG Agent - Google ADK Entry Point
This file defines the agents available in the ADK UI
"""

from agents.root_agent import root_agent

# Export the root agent so ADK can discover it
__all__ = ['root_agent']

# ADK will automatically discover and display this agent in the UI