"""OpenAI chat models with structured output, retries and per-role token accounting."""

import sys
import threading
import time
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import LLM_TIMEOUT_S, model_for

_clients: dict[tuple[str, str], ChatOpenAI] = {}
_usage: dict[str, dict] = {}
_lock = threading.Lock()


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", file=sys.stderr, flush=True)


def _client(role: str) -> ChatOpenAI:
    key = (role, model_for(role))
    with _lock:
        if key not in _clients:
            _clients[key] = ChatOpenAI(model=key[1], max_retries=4, timeout=LLM_TIMEOUT_S)
        return _clients[key]


def _record(role: str, raw, seconds: float) -> None:
    meta = getattr(raw, "usage_metadata", None) or {}
    with _lock:
        u = _usage.setdefault(role, {"model": model_for(role), "calls": 0, "input_tokens": 0,
                                     "output_tokens": 0, "seconds": 0.0})
        u["calls"] += 1
        u["input_tokens"] += meta.get("input_tokens", 0)
        u["output_tokens"] += meta.get("output_tokens", 0)
        u["seconds"] += seconds


def call_structured(role: str, schema, system: str, user: str, attempts: int = 3):
    """Invoke the model assigned to `role` and parse its answer into `schema` (strict JSON schema)."""
    runnable = _client(role).with_structured_output(schema, method="json_schema", strict=True, include_raw=True)
    messages = [SystemMessage(content=system), HumanMessage(content=user)]
    last_error = None
    for attempt in range(1, attempts + 1):
        start = time.time()
        try:
            out = runnable.invoke(messages)
        except Exception as exc:  # API errors after the client's own retries, refusals, length limits
            last_error = exc
            log(f"  ! {role} ({model_for(role)}) attempt {attempt} failed: {exc!r}"[:400])
            time.sleep(2 * attempt)
            continue
        _record(role, out.get("raw"), time.time() - start)
        if out.get("parsed") is not None:
            return out["parsed"]
        last_error = out.get("parsing_error")
        log(f"  ! {role} attempt {attempt}: unparseable output ({last_error!r})"[:400])
    raise RuntimeError(f"{role} failed after {attempts} attempts: {last_error!r}")


def usage_report() -> dict:
    with _lock:
        return {role: dict(u) for role, u in _usage.items()}
