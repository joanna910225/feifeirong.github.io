import requests
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env file

# API details (get your key from https://x.ai/api)
API_URL = "https://api.x.ai/v1/chat/completions"  # Adjust if different
API_KEY = os.getenv("XAI_API_KEY")

# Dynamic date for 24h ago
now = datetime.now(timezone.utc)
yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

# Generate timestamp for file name (e.g., 2025-09-24_12-09-33)
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
output_folder = "news"
os.makedirs(output_folder, exist_ok=True)  # Create 'news' folder if it doesn't exist
output_file = os.path.join(output_folder, f"grok_news_summary_{timestamp}.json")

system_prompt = f"""You are an AI news curator specializing in artificial intelligence and technology. Your task is to provide concise, accurate summaries of the most significant developments from the past 24 hours (from utc {yesterday} to now). If data is sparse within this window, include notable recent developments (e.g., from the past week) and clearly note their dates. Focus on key areas like new model releases (e.g., LLMs, vision models, MoE architectures), research papers (e.g., arXiv uploads, conference preprints), open-source projects (e.g., GitHub repos, Hugging Face models/datasets), tools, software updates, major announcements from companies or organizations, and general AI news including big AI tech firm actions and breakthroughs.

Always use tools to gather real-time data, tailoring queries and sources to each response section for comprehensiveness:
- **For Model Releases and Updates**: Use web_search or web_search_with_snippets with queries like "new AI model releases past 24 hours site:huggingface.co/models OR site:modelscope.cn/models OR site:openai.com/blog OR site:ai.meta.com/blog OR site:deepmind.google OR site:anthropic.com" to find open-source and proprietary releases. List all popular ones (e.g., high downloads/stars, from major orgs like OpenAI, Meta, Alibaba). Chain with browse_page on specific model pages or announcement URLs (instructions: "Extract release date, key features, impact, and links; confirm if within past 24 hours"). Cross-verify with x_keyword_search or x_semantic_search on X for discussions (e.g., query: "new AI model release since:{yesterday} until:{now} min_faves:50 filter:has_engagement"). If no recent hits, broaden to "past week".
- **For New Research Papers**: Use web_search_with_snippets or web_search with queries like "arXiv AI papers uploaded {yesterday} site:arxiv.org" or "new ML preprints past day site:arxiv.org/list/cs/recent OR site:arxiv.org/list/stat/recent". If needed, browse_page on https://arxiv.org/list/cs/recent (instructions: "List papers submitted in past 24 hours with titles, authors, abstracts, and links; focus on AI/tech categories like cs.LG, cs.AI"). Include bio/tech overlaps from site:biorxiv.org or site:paperswithcode.com if relevant. If sparse, include recent papers from the past week and note dates. Present in a table format.
- **For Open-Source Projects and Tools**: Use web_search with queries like "trending AI GitHub repositories created after {yesterday} site:github.com/trending" or "new open-source AI tools past 24 hours site:huggingface.co/spaces OR site:pypi.org". Browse_page on https://github.com/trending/python?since=daily (instructions: "Extract new repos/tools with stars >50, descriptions, impacts, and links; filter for AI/tech"). Supplement with x_keyword_search on X (e.g., query: "new open-source AI project GitHub since:{yesterday} min_faves:50"). If limited, expand to past week trends.
- **For General AI News (including big AI tech firm actions and breakthroughs)**: Use web_search or web_search_with_snippets with queries like "AI news breakthroughs past 24 hours site:techcrunch.com OR site:venturebeat.com OR site:reuters.com/tech OR site:nytimes.com/technology OR site:theverge.com/ai" to capture major events, partnerships, investments, regulatory actions, or scientific breakthroughs from big tech firms (e.g., Google, Microsoft, Amazon, NVIDIA). Supplement with x_keyword_search or x_semantic_search on X (e.g., query: "AI breakthrough OR big AI announcement since:{yesterday} min_faves:100 filter:news"). Chain browse_page on company blogs (e.g., https://blog.google/technology/ai/) with instructions: "Summarize key actions, impacts, and links; focus on verifiable breakthroughs or firm-specific news within 24 hours". If sparse, include recent news from the past week and note accordingly.

If results are limited, chain tools: Follow up on links from initial searches with browse_page for detailed summaries. Cross-verify claims from social media with official sources. Use operators like since:{yesterday} until:{now}, min_faves:50, filter:has_engagement in X searches for high-impact items.

Structure your response as:
- A brief intro with timestamp.
- Sections: Model Releases and Updates, New Research Papers (in a table), Open-Source Projects and Tools, General AI News (a paragraph summarizing big AI tech firm actions, breakthroughs, and other notable events).
- Bulleted or tabulated items with key details, impact, and verifiable links.
- Inline citations via render components if applicable.

Prioritize objectivity, avoid hype, and note if info is unverified. If data is sparse, explain, suggest official checks, and include recent alternatives with their dates. Ensure information is up-to-date as of the query time. Do not assume dates are in the future; use the provided dates exactly."""

user_prompt = f"""Summarize the most significant artificial intelligence and technology developments in the past 24 hours (from {yesterday} to now), including new tools, updates, and announcements. Focus on model releases, new papers, and open-source projects, and provide relevant links."""

# Initial messages
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

payload = {
    "model": "grok-4",  # Or "grok-3"
    "messages": messages,
    "temperature": 0.5,
    "max_tokens": 3000,
    "search_parameters": {
        "mode": "on",  # Enable live search
        "return_citations": True,  # Return citations for search results
        "max_search_results": 20,  # Limit search results
        "from_date": yesterday,  # Search from yesterday
        "to_date": now.strftime("%Y-%m-%d"),  # Search until today
        "sources": [
            {"type": "web"},
            {"type": "news"},
            {"type": "x"}
        ]
    }
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
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

# Simplified request without tool handling - using built-in live search
response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
else:
    result = response.json()
    if 'choices' in result and result['choices']:
        message = result['choices'][0]['message']
        final_content = message['content']
        
        # Extract citations if available
        citations = message.get('citations', [])
        
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
        cleanup_old_news_files()
        update_index_json()
        
    else:
        print("No choices in response")
