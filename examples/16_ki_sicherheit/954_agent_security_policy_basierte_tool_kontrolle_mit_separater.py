# Agent-Security: Policy-basierte Tool-Kontrolle mit separater Policy-Engine
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 954)
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class Action(Enum):
    READ_FILE = auto()
    WRITE_FILE = auto()
    QUERY_DB = auto()
    SEND_EMAIL = auto()
    EXEC_CODE = auto()

@dataclass
class ToolPolicy:
    action: Action
    allowed: bool
    requires_human: bool
    max_rate_per_minute: int

class PolicyEngine:
    def __init__(self):
        self.policies = {
            Action.READ_FILE: ToolPolicy(
                Action.READ_FILE, True, False, 100),
            Action.WRITE_FILE: ToolPolicy(
                Action.WRITE_FILE, False, True, 0),
            Action.SEND_EMAIL: ToolPolicy(
                Action.SEND_EMAIL, True, True, 10),
            Action.EXEC_CODE: ToolPolicy(
                Action.EXEC_CODE, False, True, 0),
        }

    def authorize(self, action: Action,
                  context: dict) -> tuple[bool, Optional[str]]:
        policy = self.policies.get(action)
        if not policy:
            return False, "Unbekannte Aktion"

        if not policy.allowed:
            return False, "Aktion nicht erlaubt"

        if policy.requires_human:
            return (False,
                    "Menschliche Freigabe erforderlich")

        return True, None

    def execute_safe(self, action: Action,
                     context: dict) -> str:
        allowed, reason = self.authorize(action, context)
        if not allowed:
            return f"BLOCKIERT: {reason}"
        return f"AUSGEFUEHRT: {action.name}"

engine = PolicyEngine()
print(engine.execute_safe(Action.READ_FILE, {}))
print(engine.execute_safe(Action.WRITE_FILE, {}))
print(engine.execute_safe(Action.SEND_EMAIL, {}))

