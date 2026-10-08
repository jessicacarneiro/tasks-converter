from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Asset:
    id: int
    asset_type: str
    title: str
    status: int
    is_external: bool
    filename: str
    time_estimation: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Asset:
        return cls(
            id=data["id"],
            asset_type=data["asset_type"],
            title=data["title"],
            status=data["status"],
            is_external=data["is_external"],
            filename=data["filename"],
            time_estimation=data["time_estimation"],
        )


@dataclass
class Chapter:
    id: int
    title: str
    sort_order: int
    object_index: int
    is_published: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Chapter:
        return cls(
            id=data["id"],
            title=data["title"],
            sort_order=data["sort_order"],
            object_index=data["object_index"],
            is_published=data["is_published"],
        )


@dataclass
class Lecture:
    id: int
    title: str
    created: str
    sort_order: int
    object_index: int
    is_published: bool
    is_free: bool
    asset: Asset | None = None
    supplementary_assets: list[Asset] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Lecture:
        asset = data.get("asset")
        return cls(
            id=data["id"],
            title=data["title"],
            created=data["created"],
            sort_order=data["sort_order"],
            object_index=data["object_index"],
            is_published=data["is_published"],
            is_free=data["is_free"],
            asset=Asset.from_dict(asset) if asset else None,
            supplementary_assets=[
                Asset.from_dict(item) for item in data.get("supplementary_assets", [])
            ],
        )


@dataclass
class Quiz:
    id: int
    title: str
    type: str
    sort_order: int
    object_index: int
    is_published: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Quiz:
        return cls(
            id=data["id"],
            title=data["title"],
            type=data["type"],
            sort_order=data["sort_order"],
            object_index=data["object_index"],
            is_published=data["is_published"],
        )


@dataclass
class Practice:
    id: int
    title: str
    sort_order: int
    object_index: int
    is_published: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Practice:
        return cls(
            id=data["id"],
            title=data["title"],
            sort_order=data["sort_order"],
            object_index=data["object_index"],
            is_published=data["is_published"],
        )


CurriculumItem = Chapter | Lecture | Quiz | Practice

ITEM_CLASSES: dict[str, type[Chapter] | type[Lecture] | type[Quiz] | type[Practice]] = {
    "chapter": Chapter,
    "lecture": Lecture,
    "quiz": Quiz,
    "practice": Practice,
}


def parse_item(data: dict[str, Any]) -> CurriculumItem:
    item_class = data["_class"]
    if item_class not in ITEM_CLASSES:
        raise ValueError(f"Unsupported curriculum item type: {item_class!r}")
    return ITEM_CLASSES[item_class].from_dict(data)


@dataclass
class CurriculumPage:
    count: int
    next: str | None
    previous: str | None
    results: list[CurriculumItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CurriculumPage:
        return cls(
            count=data["count"],
            next=data.get("next"),
            previous=data.get("previous"),
            results=[parse_item(item) for item in data.get("results", [])],
        )
