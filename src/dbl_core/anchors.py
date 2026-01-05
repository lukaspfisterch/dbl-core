from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Literal, Mapping

from .events.errors import InvalidEventError

AnchorType = Literal["axiom", "maxim", "invariant", "primitive"]


@dataclass(frozen=True)
class AnchorRef:
    anchor_id: str
    anchor_type: AnchorType

    def __post_init__(self) -> None:
        if not isinstance(self.anchor_id, str) or not self.anchor_id.strip():
            raise InvalidEventError("anchor_id must be a non-empty string")
        if self.anchor_type not in ("axiom", "maxim", "invariant", "primitive"):
            raise InvalidEventError(
                "anchor_type must be one of: axiom, maxim, invariant, primitive"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "anchor_type": self.anchor_type,
        }


def normalize_anchor_refs(refs: Any) -> list[dict[str, Any]]:
    if not isinstance(refs, list):
        raise InvalidEventError("anchors_used must be a list")
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for item in refs:
        anchor = _coerce_anchor(item)
        key = (anchor["anchor_type"], anchor["anchor_id"])
        if key in seen:
            raise InvalidEventError("anchors_used contains duplicates")
        seen.add(key)
        normalized.append(anchor)

    normalized.sort(key=lambda x: (x["anchor_type"], x["anchor_id"]))
    return normalized


def _coerce_anchor(item: Any) -> dict[str, Any]:
    if isinstance(item, AnchorRef):
        return item.to_dict()
    if not isinstance(item, Mapping):
        raise InvalidEventError("anchors_used entries must be Mapping or AnchorRef")
    anchor_id = item.get("anchor_id")
    anchor_type = item.get("anchor_type")
    if not isinstance(anchor_id, str) or not anchor_id.strip():
        raise InvalidEventError("anchor_id must be a non-empty string")
    if anchor_type not in ("axiom", "maxim", "invariant", "primitive"):
        raise InvalidEventError("anchor_type must be one of: axiom, maxim, invariant, primitive")
    _assert_only_allowed_keys(item, {"anchor_id", "anchor_type"})
    return {
        "anchor_id": anchor_id,
        "anchor_type": anchor_type,
    }


def _assert_only_allowed_keys(item: Mapping[str, Any], allowed: set[str]) -> None:
    extra = set(item.keys()) - allowed
    if extra:
        raise InvalidEventError("anchors_used contains unsupported keys")
