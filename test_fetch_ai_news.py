import json
import sys
import tempfile
import types
import unittest
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


if __name__ == "__main__":
    unittest.main()
