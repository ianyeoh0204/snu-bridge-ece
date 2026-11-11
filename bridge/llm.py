"""The only place that talks to a model. Swap this file to change provider."""
from __future__ import annotations

import base64
import json
import os

import anthropic

MODEL = os.environ.get("BRIDGE_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("BRIDGE_EFFORT", "high")
usage = {"calls": 0, "input_tokens": 0, "cached_tokens": 0, "output_tokens": 0}


def image(png: bytes) -> dict:
    data = base64.standard_b64encode(png).decode("ascii")
    return {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}}


def text(value: str) -> dict:
    return {"type": "text", "text": value}


def ask(system: str, content: list[dict], schema: dict, max_tokens: int = 32000, effort: str = "") -> dict:
    """One request, one JSON answer that matches `schema`."""
    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",  # if a safety filter declines, the API retries on a fallback model
        system=system,
        output_config={"effort": effort or EFFORT, "format": {"type": "json_schema", "schema": schema}},
        messages=[{"role": "user", "content": content}],
    ) as stream:
        message = stream.get_final_message()
    usage["calls"] += 1
    usage["input_tokens"] += message.usage.input_tokens + (message.usage.cache_creation_input_tokens or 0)
    usage["cached_tokens"] += message.usage.cache_read_input_tokens or 0
    usage["output_tokens"] += message.usage.output_tokens
    if message.stop_reason != "end_turn":
        raise RuntimeError(f"Model stopped early: {message.stop_reason}")
    return json.loads(next(block.text for block in message.content if block.type == "text"))
