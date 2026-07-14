# Message-Bus-fuer-Agenten
# Quelle: chapters/09_ai_agenten.tex (Zeile 850)
class AgentMessageBus:
    """Asynchrone Kommunikation zwischen Agenten."""

    def __init__(self):
        self.queues: dict[str, asyncio.Queue] = {}
        self.results: dict[str, list[dict]] = {}

    def register(self, agent_id: str):
        self.queues[agent_id] = asyncio.Queue()
        self.results[agent_id] = []

    async def send(self, sender: str, recipient: str, msg: dict):
        await self.queues[recipient].put({
            "from": sender, **msg,
        })

    async def receive(self, agent_id: str,
                      timeout: float = 30.0) -> dict:
        return await asyncio.wait_for(
            self.queues[agent_id].get(), timeout=timeout
        )

    def publish(self, sender: str, topic: str, data: dict):
        for agent_id in self.queues:
            if agent_id != sender:
                self.queues[agent_id].put_nowait({
                    "from": sender, "topic": topic, **data,
                })

