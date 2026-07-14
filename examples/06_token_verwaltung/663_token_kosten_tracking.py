# Token-Kosten-Tracking
# Quelle: chapters/06_token_verwaltung.tex (Zeile 663)
from dataclasses import dataclass
from datetime import datetime
import sqlite3

@dataclass
class TokenUsage:
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    cost: float
    user_id: str
    endpoint: str
    timestamp: datetime

class CostTracker:
    def __init__(self, db_path: str = "costs.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS token_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT, model TEXT,
                input_tokens INTEGER, output_tokens INTEGER,
                cached_tokens INTEGER DEFAULT 0,
                cost REAL, user_id TEXT, endpoint TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def log(self, usage: TokenUsage):
        self.conn.execute(
            "INSERT INTO token_usage "
            "(provider, model, input_tokens, output_tokens, "
            " cached_tokens, cost, user_id, endpoint, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (usage.provider, usage.model,
             usage.input_tokens, usage.output_tokens,
             usage.cached_tokens, usage.cost,
             usage.user_id, usage.endpoint,
             usage.timestamp.isoformat())
        )
        self.conn.commit()

    def daily_cost(self, date: str) -> float:
        row = self.conn.execute(
            "SELECT SUM(cost) FROM token_usage WHERE date(timestamp) = ?",
            (date,)
        ).fetchone()
        return row[0] or 0.0

    def top_users(self, limit: int = 10) -> list[tuple]:
        return self.conn.execute(
            "SELECT user_id, SUM(cost) as total "
            "FROM token_usage "
            "GROUP BY user_id ORDER BY total DESC LIMIT ?",
            (limit,)
        ).fetchall()

