from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://jsonplaceholder.typicode.com/posts"


@dataclass
class PostSummary:
    post_id: int
    user_id: int
    title: str
    word_count: int


def fetch_json(url: str, timeout: int = 10) -> list[dict]:
    """Fetch JSON data from a public HTTP API using only the Python standard library."""
    request = Request(
        url,
        headers={"User-Agent": "Stephen-Burks-Python-Portfolio/1.0"},
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected HTTP status: {response.status}")

            payload = json.loads(response.read().decode("utf-8"))

    except HTTPError as exc:
        raise RuntimeError(f"HTTP error: {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("API returned invalid JSON.") from exc

    if not isinstance(payload, list):
        raise RuntimeError("Expected the API response to contain a JSON list.")

    return payload


def normalize_title(value: object) -> str:
    """Normalize title text into a clean single-line string."""
    return " ".join(str(value or "").split())


def summarize_posts(posts: Iterable[dict]) -> list[PostSummary]:
    """Convert raw API records into a smaller, structured report."""
    summaries: list[PostSummary] = []

    for post in posts:
        try:
            post_id = int(post["id"])
            user_id = int(post["userId"])
        except (KeyError, TypeError, ValueError):
            continue

        title = normalize_title(post.get("title"))
        body = str(post.get("body", ""))
        word_count = len(body.split())

        summaries.append(
            PostSummary(
                post_id=post_id,
                user_id=user_id,
                title=title,
                word_count=word_count,
            )
        )

    return summaries


def build_statistics(summaries: list[PostSummary]) -> dict:
    """Build simple aggregate statistics for the processed dataset."""
    if not summaries:
        return {
            "processed_posts": 0,
            "unique_users": 0,
            "average_body_word_count": 0.0,
        }

    return {
        "processed_posts": len(summaries),
        "unique_users": len({item.user_id for item in summaries}),
        "average_body_word_count": round(
            sum(item.word_count for item in summaries) / len(summaries),
            2,
        ),
    }


def save_report(
    summaries: list[PostSummary],
    statistics: dict,
    output_path: Path,
) -> None:
    payload = {
        "source_api": API_URL,
        "statistics": statistics,
        "posts": [asdict(item) for item in summaries],
    }

    output_path.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    output_path = Path(__file__).resolve().parent / "api_report.json"

    print("Fetching JSON data from public API...")
    posts = fetch_json(API_URL)

    summaries = summarize_posts(posts)
    statistics = build_statistics(summaries)
    save_report(summaries, statistics, output_path)

    print("API JSON DATA PROCESSOR")
    print("=" * 40)
    print(f"Processed posts: {statistics['processed_posts']}")
    print(f"Unique users: {statistics['unique_users']}")
    print(
        "Average body word count: "
        f"{statistics['average_body_word_count']}"
    )
    print(f"Report saved to: {output_path.name}")


if __name__ == "__main__":
    main()
