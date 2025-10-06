import asyncio
import json
from pathlib import Path
from typing import Any

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from app.core.settings import get_settings
from app.db.session import build_engine_and_sessionmaker
from app.models.challenge import Challenge
from app.models.meta import Category, Size, Tag


def _get_cards_path(
    explicit_path: str | None,
) -> Path:
    base_dir = Path(__file__).resolve().parents[2]
    if explicit_path:
        return Path(explicit_path)
    return base_dir / "cards.json"


def _load_cards(
    cards_path: Path,
) -> list[dict[str, Any]]:
    data = json.loads(cards_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("cards.json must contain a list of card objects")
    return data


def _extract_unique_values(
    cards: list[dict[str, Any]],
) -> tuple[set[str], set[str], set[str]]:
    categories: set[str] = set()
    sizes: set[str] = set()
    tags: set[str] = set()
    for card in cards:
        category = str(card.get("category") or "").strip()
        if category:
            categories.add(category)
        size = str(card.get("size") or "").strip()
        if size:
            sizes.add(size)
        raw_tags = str(card.get("tags") or "").strip()
        if raw_tags:
            for tag in raw_tags.split(","):
                t = tag.strip()
                if t:
                    tags.add(t)
    return categories, sizes, tags


async def _clear_tables(
    session,
) -> None:
    await session.execute(delete(Challenge))
    await session.execute(delete(Category))
    await session.commit()


async def _upsert_meta(
    session,
    categories: set[str],
    sizes: set[str],
    tags: set[str],
) -> None:
    if categories:
        await session.execute(
            insert(Category).values(
                [{"name": name} for name in sorted(categories)]
            ).on_conflict_do_nothing(
                index_elements=["name"]
            )
        )
    if sizes:
        await session.execute(
            insert(Size).values(
                [{"name": name} for name in sorted(sizes)]
            ).on_conflict_do_nothing(
                index_elements=["name"]
            )
        )
    if tags:
        await session.execute(
            insert(Tag).values(
                [{"name": name} for name in sorted(tags)]
            ).on_conflict_do_nothing(
                index_elements=["name"]
            )
        )
    await session.commit()


def _card_to_challenge_values(
    card: dict[str, Any],
) -> dict[str, Any]:
    return {
        "title": str(card.get("title") or "").strip(),
        "short_description": (str(card.get("short_description")).strip() if card.get("short_description") else None),
        "category": (str(card.get("category")).strip() if card.get("category") else None),
        "tags": (str(card.get("tags")).strip() if card.get("tags") else None),
        "size": (str(card.get("size")).strip() if card.get("size") else "small"),
        "estimated_duration_min": (int(card.get("estimated_duration_min")) if card.get("estimated_duration_min") is not None else None),
        "is_premium_only": bool(card.get("is_premium_only", False)),
    }


async def _insert_challenges(
    session,
    cards: list[dict[str, Any]],
) -> None:
    for card in cards:
        values = _card_to_challenge_values(card=card)
        if not values["title"]:
            continue
        await session.execute(
            insert(Challenge).values(
                values
            ).on_conflict_do_nothing(
                index_elements=["title"]
            )
        )
    await session.commit()


async def seed(
    cards_json_path: str | None = None,
) -> None:
    settings = get_settings()
    _, session_maker = build_engine_and_sessionmaker(
        database_url=(
            settings.database_url
            or "postgresql+asyncpg://postgres:postgres@localhost:5433/something_new"
        ),
    )

    cards_path = _get_cards_path(explicit_path=cards_json_path)
    cards = _load_cards(cards_path=cards_path)
    categories, sizes, tags = _extract_unique_values(cards=cards)

    async with session_maker() as session:
        await _clear_tables(session=session)
        await _upsert_meta(
            session=session,
            categories=categories,
            sizes=sizes or {"small", "medium", "large"},
            tags=tags,
        )
        await _insert_challenges(
            session=session,
            cards=cards,
        )


def main() -> None:
    asyncio.run(seed(cards_json_path=None))


if __name__ == "__main__":
    main()


