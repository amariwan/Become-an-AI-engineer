# Retry mit Exponential Backoff
# Quelle: chapters/05_openai_plattform.tex (Zeile 554)
import time
from openai import RateLimitError, APIError

def query_with_retry(client, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(**kwargs)
        except (RateLimitError, APIError) as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt + time.time() % 1
            time.sleep(wait)

