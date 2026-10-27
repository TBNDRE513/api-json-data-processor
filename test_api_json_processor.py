import unittest

from api_json_processor import (
    build_statistics,
    normalize_title,
    summarize_posts,
)


class ApiJsonProcessorTests(unittest.TestCase):
    def test_normalize_title(self):
        self.assertEqual(
            normalize_title("  hello\n   world  "),
            "hello world",
        )

    def test_summarize_posts_skips_invalid_records(self):
        posts = [
            {
                "id": 1,
                "userId": 2,
                "title": "Example title",
                "body": "one two three",
            },
            {
                "id": "bad",
                "userId": 2,
                "title": "Invalid",
                "body": "ignored",
            },
        ]

        results = summarize_posts(posts)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].post_id, 1)
        self.assertEqual(results[0].user_id, 2)
        self.assertEqual(results[0].word_count, 3)

    def test_build_statistics(self):
        posts = [
            {
                "id": 1,
                "userId": 1,
                "title": "A",
                "body": "one two",
            },
            {
                "id": 2,
                "userId": 2,
                "title": "B",
                "body": "one two three four",
            },
        ]

        summaries = summarize_posts(posts)
        stats = build_statistics(summaries)

        self.assertEqual(stats["processed_posts"], 2)
        self.assertEqual(stats["unique_users"], 2)
        self.assertEqual(stats["average_body_word_count"], 3.0)


if __name__ == "__main__":
    unittest.main()
