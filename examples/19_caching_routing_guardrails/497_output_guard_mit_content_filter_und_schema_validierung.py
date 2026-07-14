# Output Guard mit Content-Filter und Schema-Validierung
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 497)
from typing import Optional


class OutputGuard:
    def __init__(self):
        self.blocked_categories = [
            "gewaltverherrlichend", "beleidigend",
            "diskriminierend", "illegal",
        ]
        self.max_length = 4096  # Zeichen

    def check_content_safety(self, text: str) -> Optional[str]:
        """LLM-basierter Content-Safety-Check."""
        prompt = (
            f"Pruefe den folgenden Text auf verbotene Inhalte. "
            f"Kategorien: {', '.join(self.blocked_categories)}.\n"
            f"Antworte NUR mit 'OK' oder 'BLOCKED: <Kategorie>'.\n\n"
            f"{text[:2000]}"
        )
        response = call_llm("gpt-4o-mini", prompt, temperature=0.0)
        if response.startswith("BLOCKED"):
            return response
        return None

    def validate_schema(self, text: str,
                        schema: dict) -> tuple[bool, str]:
        """Prueft, ob der Output einem JSON-Schema entspricht."""
        try:
            import json
            data = json.loads(text)
            for key, expected_type in schema.items():
                if key not in data:
                    return False, f"Missing key: {key}"
                if not isinstance(data[key], expected_type):
                    return False, (f"Wrong type for {key}: "
                                   f"{type(data[key])} != {expected_type}")
            return True, "OK"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"

    def validate(self, llm_output: str,
                 schema: dict = None) -> dict:
        result = {
            "original_length": len(llm_output),
            "truncated": False,
            "blocked": False,
            "block_reason": None,
        }

        # Laengenbegrenzung
        if len(llm_output) > self.max_length:
            llm_output = llm_output[:self.max_length]
            result["truncated"] = True

        # Inhaltspruefung
        safety_issue = self.check_content_safety(llm_output)
        if safety_issue:
            result["blocked"] = True
            result["block_reason"] = safety_issue
            result["output"] = "[Output blocked by safety guard]"
            return result

        # Schema-Validierung
        if schema:
            valid, msg = self.validate_schema(llm_output, schema)
            result["schema_valid"] = valid
            result["schema_message"] = msg

        result["output"] = llm_output
        return result

