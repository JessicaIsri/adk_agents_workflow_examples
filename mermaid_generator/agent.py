from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.llm_agent import Agent

from mermaid_generator.prompts import interpreter_instructions, mermaid_generator_instructions, reviwer_instructions

MODEL = 'gemini-2.5-flash'

interpreter_agent = LlmAgent(
    model=MODEL,
    name='interpreter_agent',
    description='Agente interpretador de fluxos',
    instruction=interpreter_instructions,
)

mermaid_agent = LlmAgent(
    model=MODEL,
    name='mermaid_agent',
    description='Agente de mermaid',
    instruction=mermaid_generator_instructions
)

revisor_agent = LlmAgent(
    model=MODEL,
    name='revisor_agent',
    description='Agente de revisor',
    instruction=reviwer_instructions
)

sequential_agent = SequentialAgent(
    name='MermaidGenerator',
    sub_agents=[interpreter_agent, mermaid_agent]
)

root_agent = sequential_agent
