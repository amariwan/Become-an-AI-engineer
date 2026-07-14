# ReAct Agent
# Quelle: chapters/09_ai_agenten.tex (Zeile 588)
class ReActAgent:
    def __init__(self, tools: ToolRegistry, llm_client, max_steps: int = 10):
        self.tools = tools
        self.llm = llm_client
        self.max_steps = max_steps

    def run(self, user_query: str) -> str:
        messages = [{"role": "system", "content": (
            "Loese Aufgaben durch Thought -> Action -> Observation. "
            "Thought: dein Gedankengang. "
            "Action: Tool-Name. "
            "Action Input: JSON. "
            "Wenn fertig: Answer: Endergebnis."
        )}, {"role": "user", "content": user_query}]

        for step in range(self.max_steps):
            response = self.llm.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[t.to_openai() for t in self.tools.tools.values()],
            )
            msg = response.choices[0].message

            if msg.content and "Answer:" in msg.content:
                return msg.content

            if msg.tool_calls:
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = self.tools.execute(tc.function.name, **args)
                    messages.append(msg)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": str(result),
                    })

        return "Max steps reached without completion."

