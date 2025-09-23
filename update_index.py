#!/usr/bin/env python3
"""
Script to build/update index.json in root directory with all news files.
Run this whenever you add new news JSON files manually.
"""

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

def build_news_index():
    """Build index.json file in root directory with all news files."""
    news_dir = Path('news')
    
    if not news_dir.exists():
        print("Error: news/ directory not found!")
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
    
    print(f"✓ Built index.json with {len(json_files)} news files:")
    for file in json_files:
        print(f"  - {file}")
    
    return len(json_files)

if __name__ == '__main__':
    count = build_news_index()
    if count:
        print(f"\n✓ Index updated! Open index.html to see {count} news articles.")
    else:
        print("\n✗ No news files found to index.")