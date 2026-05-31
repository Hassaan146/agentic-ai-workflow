from __future__ import annotations

from typing import Any


def to_toon(value: Any, *, max_text_length: int = 1200) -> str:
    """Encode simple Python data into a compact TOON-like handoff format."""
    return _encode(value, 0, max_text_length=max_text_length).strip()


def build_agent_handoff_payload(*, task_id: str, agent_name: str, summary: str, data: dict[str, Any]) -> str:
    compact_data = _compact_data(data)
    return to_toon(
        {
            "task_id": task_id,
            "agent": agent_name,
            "summary": summary,
            "data": compact_data,
        }
    )


def _compact_data(data: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    for key, value in data.items():
        if key == "toon_payload":
            continue
        if key == "sources" and isinstance(value, list):
            compact[key] = [_compact_source(source) for source in value[:5]]
        else:
            compact[key] = value
    return compact


def _compact_source(source: Any) -> dict[str, Any]:
    if not isinstance(source, dict):
        return {"value": source}
    return {
        "title": source.get("title", ""),
        "url": source.get("url", ""),
        "facts": source.get("facts", [])[:3],
        "context": source.get("source_context", ""),
    }


def _encode(value: Any, indent: int, *, max_text_length: int) -> str:
    prefix = "  " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            safe_key = _safe_key(str(key))
            if _is_scalar(item):
                lines.append(f"{prefix}{safe_key}: {_scalar(item, max_text_length=max_text_length)}")
            else:
                lines.append(f"{prefix}{safe_key}:")
                lines.append(_encode(item, indent + 1, max_text_length=max_text_length))
        return "\n".join(line for line in lines if line != "")
    if isinstance(value, list):
        return _encode_list(value, indent, max_text_length=max_text_length)
    return f"{prefix}{_scalar(value, max_text_length=max_text_length)}"


def _encode_list(values: list[Any], indent: int, *, max_text_length: int) -> str:
    prefix = "  " * indent
    if not values:
        return f"{prefix}[]"
    if all(isinstance(item, dict) for item in values):
        keys = _shared_keys(values)
        if keys:
            lines = [f"{prefix}[{len(values)}]{{{','.join(_safe_key(key) for key in keys)}}}:"]
            for item in values:
                row = ",".join(_scalar(item.get(key, ""), max_text_length=max_text_length) for key in keys)
                lines.append(f"{prefix}  {row}")
            return "\n".join(lines)
    lines = []
    for item in values:
        if _is_scalar(item):
            lines.append(f"{prefix}- {_scalar(item, max_text_length=max_text_length)}")
        else:
            lines.append(f"{prefix}-")
            lines.append(_encode(item, indent + 1, max_text_length=max_text_length))
    return "\n".join(lines)


def _shared_keys(values: list[Any]) -> list[str]:
    dicts = [item for item in values if isinstance(item, dict)]
    if not dicts:
        return []
    keys = list(dicts[0].keys())
    if len(keys) > 5:
        return []
    if all(list(item.keys()) == keys for item in dicts):
        return [str(key) for key in keys]
    return []


def _is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _scalar(value: Any, *, max_text_length: int) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).replace("\r", " ").replace("\n", " ")
    text = " ".join(text.split())
    if len(text) > max_text_length:
        text = text[: max_text_length - 3].rstrip() + "..."
    needs_quotes = not text or any(char in text for char in [":", ",", "#", "[", "]", "{", "}"])
    if needs_quotes:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def _safe_key(key: str) -> str:
    cleaned = key.strip().replace(" ", "_")
    return cleaned or "field"
