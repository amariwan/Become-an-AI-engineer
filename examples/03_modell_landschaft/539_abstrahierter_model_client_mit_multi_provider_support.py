# Abstrahierter Model-Client mit Multi-Provider-Support
# Quelle: chapters/03_modell_landschaft.tex (Zeile 539)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import openai
import anthropic


class Provider(Enum):
    OPENAI = openai
    ANTHROPIC = anthropic
    GOOGLE = "google"
    LOCAL = "local"

@dataclass
class QueryResult:
    response_text: str
    model_used: str
    tokens_input: int
    tokens_output: int
    cost_eur: float


class BaseModelClient(ABC):
    @abstractmethod
    def query(self, messages: list[dict]) -> QueryResult:
        pass

class OpenAIClient(BaseModelClient):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.pricing = {"input": 0.0015, "output": 0.006}

    def query(self, messages: list[dict]) -> QueryResult:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
        )
        return QueryResult(
            response_text=response.choices[0].message.content,
            model_used=self.model,
            tokens_input=response.usage.prompt_tokens,
            tokens_output=response.usage.completion_tokens,
            cost_eur=(response.usage.prompt_tokens * self.pricing["input"] +
                      response.usage.completion_tokens * self.pricing["output"]) / 1000,
        )

class AnthropicClient(BaseModelClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.pricing = {"input": 0.003, "output": 0.015}

    def query(self, messages: list[dict]) -> QueryResult:
        response = self.client.messages.create(
            model=self.model, max_tokens=4096,
            messages=messages,
            system="Du bist ein hilfreicher Assistent."
        )
        return QueryResult(
            response_text=response.content[0].text,
            model_used=self.model,
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            cost_eur=(response.usage.input_tokens * self.pricing["input"] +
                      response.usage.output_tokens * self.pricing["output"]) / 1000,
        )


def ask(messages: list[dict], provider: Provider = Provider.OPENAI):
    if provider == Provider.OPENAI:
        client = OpenAIClient(api_key="sk-...")
    elif provider == Provider.ANTHROPIC:
        client = AnthropicClient(api_key="sk-ant-...")
    result = client.query(messages)
    print(f"{result.model_used}: {result.response_text[:100]}... "
          f"(EUR{result.cost_eur:.4f})")

msgs = [{"role": "user",
         "content": "Was ist der Unterschied zwischen RAG und Fine-Tuning?"}]
ask(msgs, Provider.OPENAI)
ask(msgs, Provider.ANTHROPIC)

