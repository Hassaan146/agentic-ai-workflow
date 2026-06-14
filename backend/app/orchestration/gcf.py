from __future__ import annotations

from typing import Any


def to_gcf(value: Any, *, max_text_length: int = 1200) -> str:
    """Encode simple Python data into a compact GCF-style handoff format.

    GCF is used only at the LLM handoff boundary. The app still uses JSON for
    API responses and persistence because that keeps frontend/backend contracts stable.
    """
    return _encode_root(value, max_text_length=max_text_length).strip()


def build_agent_handoff_payload(*, task_id: str, agent_name: str, summary: str, data: dict[str, Any]) -> str:
    compact_data = _compact_data(data)
    return to_gcf(
        {
            "handoff": {
                "task_id": task_id,
                "agent": agent_name,
                "summary": summary,
            },
            "data": compact_data,
        }
    )


def _compact_data(data: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    for key, value in data.items():
        if key in {"gcf_payload", "toon_payload"}:
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


def _encode_root(value: Any, *, max_text_length: int) -> str:
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            section = _safe_key(str(key))
            lines.append(f"## {section}")
            lines.extend(_encode_section(item, max_text_length=max_text_length))
        return "\n".join(lines)
    if isinstance(value, list):
        return "## items\n" + "\n".join(_encode_list(value, max_text_length=max_text_length))
    return f"## value\n@0 value {_scalar(value, max_text_length=max_text_length)}"


def _encode_section(value: Any, *, max_text_length: int) -> list[str]:
    if isinstance(value, dict):
        lines: list[str] = []
        for index, (key, item) in enumerate(value.items()):
            safe_key = _safe_key(str(key))
            if _is_scalar(item):
                lines.append(f"@{index} {safe_key} {_scalar(item, max_text_length=max_text_length)}")
            elif isinstance(item, list):
                lines.append(f"@{index} {safe_key}")
                lines.extend(f"  {line}" for line in _encode_list(item, max_text_length=max_text_length))
            else:
                lines.append(f"@{index} {safe_key}")
                lines.extend(f"  {line}" for line in _encode_section(item, max_text_length=max_text_length))
        return lines
    if isinstance(value, list):
        return _encode_list(value, max_text_length=max_text_length)
    return [f"@0 value {_scalar(value, max_text_length=max_text_length)}"]


def _encode_list(values: list[Any], *, max_text_length: int) -> list[str]:
    if not values:
        return ["@0 empty []"]
    lines: list[str] = []
    for index, item in enumerate(values):
        if isinstance(item, dict):
            fields = " ".join(
                f"{_safe_key(str(key))} {_scalar(value, max_text_length=max_text_length)}"
                for key, value in item.items()
                if _is_scalar(value)
            )
            nested = {key: value for key, value in item.items() if not _is_scalar(value)}
            lines.append(f"@{index} {fields}".rstrip())
            for key, value in nested.items():
                lines.append(f"  {_safe_key(str(key))}")
                lines.extend(f"    {line}" for line in _encode_section(value, max_text_length=max_text_length))
        elif _is_scalar(item):
            lines.append(f"@{index} value {_scalar(item, max_text_length=max_text_length)}")
        else:
            lines.append(f"@{index}")
            lines.extend(f"  {line}" for line in _encode_section(item, max_text_length=max_text_length))
    return lines


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
    needs_quotes = not text or any(char in text for char in [":", "#", "[", "]", "{", "}"])
    if needs_quotes:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def _safe_key(key: str) -> str:
    cleaned = key.strip().replace(" ", "_")
    return cleaned or "field"
