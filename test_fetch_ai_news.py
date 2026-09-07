import json
import os
import sys
import tempfile
import types
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.modules.setdefault("requests", types.SimpleNamespace())

import fetch_ai_news


class RecentBriefingContextTest(unittest.TestCase):
    def test_returns_only_the_latest_briefings(self):
        with tempfile.TemporaryDirectory() as folder:
            news = Path(folder)
            for day in range(1, 4):
                (news / f"brief-{day}.json").write_text(
                    json.dumps({
                        "coverage_end_utc": f"2026-08-0{day}T00:00:00Z",
                        "summary_en": f"story {day}",
                    }),
                    encoding="utf-8",
                )
            with patch.object(fetch_ai_news, "OUTPUT_FOLDER", news):
                context = fetch_ai_news.recent_briefing_context(limit=2)

        self.assertIn("story 3", context)
        self.assertIn("story 2", context)
        self.assertNotIn("story 1", context)

    def test_sends_opencode_session_headers(self):
        response = types.SimpleNamespace(
            status_code=200,
            json=lambda: {
                "output": [{
                    "type": "message",
                    "content": [{
                        "type": "output_text",
                        "text": "<ENGLISH>English</ENGLISH><CHINESE>Chinese</CHINESE>",
                    }],
                }],
            },
        )
        now = datetime(2026, 9, 7, tzinfo=timezone.utc)

        with patch.dict(os.environ, {"GITHUB_RUN_ID": "34089558332"}), patch.object(
            fetch_ai_news.requests, "post", return_value=response, create=True
        ) as post:
            fetch_ai_news.request_bilingual_summary(now, now, now)

        headers = post.call_args.kwargs["headers"]
        self.assertEqual(headers["x-opencode-session"], "34089558332")
        self.assertEqual(headers["User-Agent"], "feifeirong-news/1.0")


if __name__ == "__main__":
    unittest.main()
