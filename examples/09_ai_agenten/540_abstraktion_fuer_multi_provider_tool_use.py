# Abstraktion fuer Multi-Provider Tool Use
# Quelle: chapters/09_ai_agenten.tex (Zeile 540)
from dataclasses import dataclass, field

@dataclass
class AgentTool:
    name: str
    description: str
    fn: callable
    parameters: dict = field(default_factory=dict)

    def to_openai(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def to_anthropic(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters,
        }

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, AgentTool] = {}

    def register(self, tool: AgentTool):
        self.tools[tool.name] = tool

    def execute(self, name: str, **kwargs):
        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")
        return tool.fn(**kwargs)

