# Circuit-Breaker für LLM-API-Ausfälle
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 349)
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"       # Normalbetrieb
    OPEN = "open"           # API down, keine Versuche
    HALF_OPEN = "half_open" # Test-Request erlaubt

class LLMCircuitBreaker:
    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: float = 60.0):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0.0

    def call(self, llm_func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                return self.fallback_response()

        try:
            result = llm_func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            return self.fallback_response()

    def fallback_response(self):
        return {"response": "Service voruebergehend nicht "
                            "verfuegbar. Bitte spaeter erneut versuchen.",
                "cached": False, "fallback": True}

breaker = LLMCircuitBreaker(failure_threshold=3, recovery_timeout=30)
result = breaker.call(robust_chat, [{"role": "user", "content": "Hallo"}])

