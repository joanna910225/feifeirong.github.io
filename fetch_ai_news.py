import requests
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# API details (get your key from https://console.x.ai)
# Live Search (search_parameters) was deprecated by xAI -> replaced by the
# web_search server-side tool on the Responses API.
API_URL = "https://api.x.ai/v1/responses"
API_KEY = os.getenv("XAI_API_KEY")
MODEL = "grok-4.6"

# Dynamic date for 24h ago
now = datetime.now(timezone.utc)
yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

# Generate timestamp for file name (e.g., 2025-09-24_12-09-33)
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
output_folder = "news"
os.makedirs(output_folder, exist_ok=True)  # Create 'news' folder if it doesn't exist
output_file = os.path.join(output_folder, f"grok_news_summary_{timestamp}.json")

system_prompt = f"""You are an AI news curator specializing in artificial intelligence and technology. Use the web search tool to gather real-time information, then provide concise, accurate summaries of the most significant developments from the past 24 hours (from UTC {yesterday} to now). If data is sparse within this window, include notable recent developments from the past week and clearly note their dates.

Cover these areas:
- **Model Releases and Updates**: new LLMs, vision models, MoE architectures, and proprietary releases (OpenAI, Meta, Google, Anthropic, Alibaba, xAI, etc.).
- **New Research Papers**: arXiv uploads and preprints from the past day (cs.LG, cs.AI, etc.), presented in a table with titles, authors, and links.
- **Open-Source Projects and Tools**: trending GitHub repos, Hugging Face models/datasets, new developer tools.
- **General AI News**: major company actions, partnerships, funding, regulatory news, and breakthroughs.

Structure your response as:
- A brief intro with the current UTC timestamp.
- Sections: Model Releases and Updates, New Research Papers (table), Open-Source Projects and Tools, General AI News.
- Bulleted or tabulated items with key details, impact, and verifiable links.

Prioritize objectivity, avoid hype, and note if information is unverified. If data is sparse, say so and include recent alternatives with their dates. Use the provided dates exactly and do not assume dates are in the future."""

user_prompt = f"""Summarize the most significant artificial intelligence and technology developments in the past 24 hours (from {yesterday} to now), including new tools, updates, and announcements. Focus on model releases, new papers, and open-source projects, and provide relevant links."""

payload = {
    "model": MODEL,
    "input": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    "tools": [
        {"type": "web_search"},
    ],
    "temperature": 0.5,
    "max_output_tokens": 4000,
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def extract_date_from_filename(filename):
    """Extract date from filename for sorting."""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return datetime.min


def cleanup_old_news_files():
    """Remove news files older than 30 days."""
    news_dir = Path(output_folder)
    if not news_dir.exists():
        return

    cutoff_date = now - timedelta(days=30)
    removed_files = []

    for file in news_dir.glob('*.json'):
        if file.name == 'index.json':
            continue

        file_date = extract_date_from_filename(file.name)
        if file_date != datetime.min and file_date.date() < cutoff_date.date():
            file.unlink()
            removed_files.append(file.name)

    if removed_files:
        print(f"Removed {len(removed_files)} old news files (older than 30 days)")


def update_index_json():
    """Update index.json with current news files."""
    news_dir = Path(output_folder)

    if not news_dir.exists():
        return

    # Find all JSON files (excluding index.json)
    json_files = []
    for file in news_dir.glob('*.json'):
        if file.name != 'index.json':
            json_files.append(file.name)

    # Sort by date (newest first)
    json_files.sort(key=extract_date_from_filename, reverse=True)

    # Create index data with metadata
    index_data = {
        "last_updated": now.isoformat(),
        "total_files": len(json_files),
        "files": json_files
    }

    # Write to root directory
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"Updated index.json with {len(json_files)} news files")


def parse_response(result):
    """Parse Responses API output into (text, citations)."""
    text_parts = []
    citations = []

    output = result.get("output", [])
    for item in output:
        item_type = item.get("type")
        if item_type == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    text_parts.append(content.get("text", ""))
                for ann in content.get("annotations", []):
                    if ann.get("type") == "url_citation" and ann.get("url"):
                        citations.append(ann.get("url"))
        elif item_type == "web_search_call":
            # Server-side web search call; the model already used it.
            continue

    return "".join(text_parts), citations


def main():
    if not API_KEY:
        print("Error: XAI_API_KEY environment variable is not set")
        sys.exit(1)

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

    result = response.json()
    final_content, citations = parse_response(result)

    if not final_content:
        print("Error: no content in response")
        print(json.dumps(result, indent=2)[:2000])
        sys.exit(1)

    # Save the final summary to JSON file
    save_data = {
        "timestamp": timestamp,
        "summary": final_content,
        "citations": citations
    }
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)
    print(f"Summary saved to {output_file}")
    print(final_content)
    if citations:
        print("\nCitations:")
        for i, citation in enumerate(citations, 1):
            print(f"{i}. {citation}")

    # Clean up old files and update index
    # NOTE: auto-cleanup temporarily disabled to preserve the existing
    # (all >30 days old) news archive. Re-enable after archive strategy is decided.
    # cleanup_old_news_files()
    update_index_json()


if __name__ == "__main__":
    main()
