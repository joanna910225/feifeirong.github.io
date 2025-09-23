import requests
import json
import os
import re
from datetime import datetime
from pathlib import Path

def extract_date_from_filename(filename):
    """Extract date from filename for sorting."""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return datetime.min

def format_content_to_html(content):
    """Convert markdown-like content to HTML."""
    # Replace markdown formatting
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Handle line breaks
    content = content.replace('\n\n', '<br><br>')
    content = content.replace('\n', '<br>')
    
    return content

def create_news_block_html(news_data, filename, is_first=False):
    """Create HTML for a single news block."""
    date = extract_date_from_filename(filename)
    formatted_date = date.strftime('%Y-%m-%d')
    
    formatted_content = format_content_to_html(news_data['summary'])
    
    expanded_class = 'expanded' if is_first else ''
    toggle_symbol = '−' if is_first else '+'
    
    return f'''
    <div class="news-block">
        <div class="news-header" onclick="toggleNews(this)">
            <span class="news-title">AI & Tech News Summary</span>
            <span class="news-date">{formatted_date}</span>
            <span class="news-toggle">{toggle_symbol}</span>
        </div>
        <div class="news-content {expanded_class}">
            <p>{formatted_content}</p>
        </div>
    </div>'''

def generate_news_html():
    """Generate HTML file with all news articles."""
    news_dir = Path('news')
    
    # Find all JSON files (excluding index.json)
    json_files = []
    for file in news_dir.glob('*.json'):
        if file.name != 'index.json':
            json_files.append(file.name)
    
    if not json_files:
        print("No news JSON files found!")
        return
    
    # Sort by date (newest first)
    json_files.sort(key=extract_date_from_filename, reverse=True)
    
    # Generate HTML blocks
    html_blocks = []
    for i, filename in enumerate(json_files):
        try:
            with open(news_dir / filename, 'r', encoding='utf-8') as f:
                news_data = json.load(f)
            
            html_block = create_news_block_html(news_data, filename, i == 0)
            html_blocks.append(html_block)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    # Write complete HTML file
    html_content = '\n'.join(html_blocks)
    
    with open('news_content.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated news_content.html with {len(html_blocks)} articles")

def build_news_index():
    """Build index.json file in root directory with all news files."""
    news_dir = Path('news')
    
    if not news_dir.exists():
        print("Warning: news/ directory not found!")
        return
    
    # Find all JSON files (excluding index.json)
    json_files = []
    for file in news_dir.glob('*.json'):
        if file.name != 'index.json':
            json_files.append(file.name)
    
    if not json_files:
        print("No news JSON files found!")
        return
    
    # Sort by date (newest first)
    json_files.sort(key=extract_date_from_filename, reverse=True)
    
    # Create index data with metadata
    index_data = {
        "last_updated": datetime.now().isoformat(),
        "total_files": len(json_files),
        "files": json_files
    }
    
    # Write to root directory
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"Built index.json with {len(json_files)} news files:")
    for file in json_files:
        print(f"  - {file}")

# Define the prompt
# Enhanced System Prompt (encourages tables/markdown)
system_prompt = """You are a professional AI News Reporter. Deliver objective, insightful summaries with journalistic integrity. Structure reports using markdown: bold key terms, bullet points for lists, and tables for comparisons (e.g., model features, paper impacts). Always cite sources with hyperlinks. Focus on high-impact stories from the past 24 hours."""

# Enhanced User Prompt (explicitly requests tables)
prompt = """As a professional AI News Reporter, compile a daily briefing on AI/technology developments of last 24 hrs. Categorize into sections: Model Releases, Research Papers, Open-Source Projects. For each, use a markdown table with columns: Item, Summary (1-2 sentences), Key Impacts, Source Link. Limit to 4-6 items total. End with a forward-looking analysis paragraph."""
# API endpoint and configuration
url = "https://api.x.ai/v1/chat/completions"
api_key = os.getenv("XAI_API_KEY")  # Load from environment variable

if not api_key:
    raise ValueError("XAI_API_KEY environment variable is not set. Please set it in your environment or GitHub Actions secrets.")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    "model": "grok-3",  # UI default; switch to "grok-4-0709" if needed
    "stream": False,
    "temperature": 0.7,  # Balanced creativity
    "max_tokens": 3000,  # For detailed responses
    # Fixed search_parameters: Use tagged enum objects for sources
    "search_parameters": {
        "mode": "auto",  # "auto", "on", or "off"
        "sources": [
            {"type": "web"},  # Correct field for web search
            {"type": "x"}     # Correct field for X posts
        ]
        # Optional: Add date filters, e.g., "from_date": "2025-09-22" (ISO format)
    }
}

# Make the API call
response = requests.post(url, headers=headers, json=data)

if response.status_code != 200:
    raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

result = response.json()["choices"][0]["message"]["content"]

# Prepare data with timestamp
timestamp = datetime.now().isoformat()
news_data = {
    "timestamp": timestamp,
    "summary": result
}

# Ensure news/ directory exists
os.makedirs("news", exist_ok=True)

# Save to JSON file (using timestamp in filename for uniqueness)
filename = f"news/grok_news_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(news_data, f, indent=4, ensure_ascii=False)

print(f"Summary saved to {filename}")

# Generate HTML for all news files
generate_news_html()

# Build index.json in root directory
build_news_index()

print("News HTML file and index updated")