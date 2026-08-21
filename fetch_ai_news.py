import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

API_URL = "https://opencode.ai/zen/go/v1/responses"
API_KEY = os.getenv("OPENCODE_GO_API_KEY")
MODEL = "grok-4.5"
ROOT = Path(__file__).resolve().parent
now = datetime.now(timezone.utc)
yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
output_folder = ROOT / "public" / "news"
output_folder.mkdir(parents=True, exist_ok=True)
output_file = output_folder / f"grok_news_summary_{timestamp}.json"

base_prompt = f"""You are an AI news curator specializing in artificial intelligence and technology. Use the web search tool to gather real-time information, then provide concise, accurate summaries of the most significant developments from the past 24 hours (from UTC {yesterday} to now). If data is sparse within this window, include notable recent developments from the past week and clearly note their dates.

Cover these areas:
- **Model Releases and Updates**: new LLMs, vision models, MoE architectures, and proprietary releases.
- **New Research Papers**: arXiv uploads and preprints from the past day (cs.LG, cs.AI, etc.), presented in a table with titles, authors, and links.
- **Open-Source Projects and Tools**: trending GitHub repos, Hugging Face models/datasets, and developer tools.
- **General AI News**: major company actions, partnerships, funding, regulatory news, and breakthroughs.

Structure your response as a brief intro followed by sections: Model Releases and Updates, New Research Papers (table), Open-Source Projects and Tools, and General AI News. Use bullets or tables with key details, impact, and verifiable links. Prioritize objectivity, avoid hype, and note if information is unverified. Use dates exactly and do not assume dates are in the future."""


def request_summary(language: str):
    language_instruction = "Write the briefing in English." if language == "en" else "Write the briefing in Simplified Chinese. Preserve product names, paper titles, and URLs; translate explanations and headings."
    payload = {
        "model": MODEL,
        "input": [
            {"role": "system", "content": base_prompt + "\n\n" + language_instruction},
            {"role": "user", "content": f"Summarize the most significant artificial intelligence and technology developments in the past 24 hours (from {yesterday} to now), including new tools, updates, and announcements. Focus on model releases, new papers, and open-source projects, and provide relevant links."},
        ],
        "tools": [{"type": "web_search"}],
        "temperature": 0.5,
        "max_output_tokens": 4000,
    }
    response = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, json=payload, timeout=180)
    if response.status_code != 200:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")
    result = response.json()
    text_parts, citations = [], []
    for item in result.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(content.get("text", ""))
            for annotation in content.get("annotations", []):
                if annotation.get("type") == "url_citation" and annotation.get("url"):
                    citations.append(annotation["url"])
    text = "".join(text_parts).strip()
    if not text:
        raise RuntimeError("API returned no text")
    return text, citations


def extract_date_from_filename(filename):
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    return datetime.strptime(match.group(1), "%Y-%m-%d") if match else datetime.min


def update_index_json():
    files = sorted((f.name for f in output_folder.glob("*.json")), key=extract_date_from_filename, reverse=True)
    data = {"last_updated": now.isoformat(), "total_files": len(files), "files": files}
    (ROOT / "public" / "index.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated public/index.json with {len(files)} news files")


def main():
    if not API_KEY:
        print("Error: OPENCODE_GO_API_KEY environment variable is not set")
        sys.exit(1)
    try:
        summary_en, citations_en = request_summary("en")
        summary_zh, citations_zh = request_summary("zh")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    citations = list(dict.fromkeys(citations_en + citations_zh))
    output_file.write_text(json.dumps({"timestamp": timestamp, "summary": summary_en, "summary_en": summary_en, "summary_zh": summary_zh, "citations": citations}, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"Summary saved to {output_file.relative_to(ROOT)}")
    print(summary_en)
    update_index_json()


if __name__ == "__main__":
    main()
