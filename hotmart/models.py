from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Page:
    name: str
    hash: str
    type: str
    locked: bool
    completed: bool
    has_player_media: bool
    liberation_start: int
    minimum_score_required: bool
    thumbnail_url: str | None = None
    first_media_code: str | None = None
    first_media_type: str | None = None
    media_duration_in_seconds: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Page:
        return cls(
            name=data["name"],
            hash=data["hash"],
            type=data["type"],
            locked=data["locked"],
            completed=data["completed"],
            has_player_media=data["hasPlayerMedia"],
            liberation_start=data["liberationStart"],
            minimum_score_required=data["minimumScoreRequired"],
            thumbnail_url=data.get("thumbnailUrl"),
            first_media_code=data.get("firstMediaCode"),
            first_media_type=data.get("firstMediaType"),
            media_duration_in_seconds=data.get("mediaDurationInSeconds"),
        )


@dataclass
class Module:
    id: str
    code: str
    name: str
    type: str
    thumbnail_url: str
    locked: bool
    extra: bool
    pages: list[Page] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Module:
        return cls(
            id=data["id"],
            code=data["code"],
            name=data["name"],
            type=data["type"],
            thumbnail_url=data["thumbnailUrl"],
            locked=data["locked"],
            extra=data["extra"],
            pages=[Page.from_dict(page) for page in data.get("pages", [])],
        )
