from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

API_URL = "https://opencode.ai/zen/go/v1/responses"
API_KEY = os.getenv("OPENCODE_GO_API_KEY")
MODEL = "grok-4.5"
ROOT = Path(__file__).resolve().parent
OUTPUT_FOLDER = ROOT / "public" / "news"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# OpenCode Go Grok 4.5 rates (USD per 1M tokens). Web-search pricing uses
# xAI's published $5 / 1K calls because OpenCode does not expose a billed-cost
# field in its public Go documentation. The saved dollar value is an estimate.
PRICING = {
    "input_per_million": 2.00,
    "cached_input_per_million": 0.30,
    "output_per_million": 6.00,
    "web_search_per_call": 0.005,
}

SYSTEM_PROMPT = r"""You are Grok acting as an evidence-first AI and technology intelligence editor. Research, verify, rank, and write a bilingual daily briefing for the exact UTC window supplied by the user.

EDITORIAL PRIORITY
Allocate attention approximately as follows:
1. Model releases and major model updates — 40%
2. New AI papers and studies — 25%
3. New and fast-growing GitHub/Hugging Face projects — 15%
4. New AI products and startups — 10%
5. AI leader and industry watch — 10%

TIME AND SELECTION RULES
- Use UTC for inclusion decisions. Never include an event after the supplied end time.
- Prefer items first announced or materially updated in the primary 24-hour window.
- If a section is sparse, expand that section first to 72 hours, then to 7 days. Label every fallback item with its actual date and “Outside the primary 24-hour window.”
- Do not pad sections with stale or low-value items.
- Search each section independently. Rank by recency, primary-source evidence, impact, novelty, and relevance to AI builders and researchers.
- Identify the original announcement date and distinguish releases from previews, rumors, benchmarks, pricing/API updates, partnerships, and recycled announcements.
- Remove duplicates. Never invent URLs, dates, quotations, specifications, benchmark results, affiliations, star counts, pricing, licensing, or availability.
- If a consequential claim cannot be verified, label it “Unverified” or omit it.

SOURCE POLICY
Prefer primary sources: official lab/company announcements, documentation, API changelogs, model cards, papers, arXiv, OpenReview, conference/journal pages, official GitHub repositories and Releases, Hugging Face pages, product documentation, Product Hunt launches, Y Combinator company/Launch/batch pages, and direct interviews/posts/transcripts.
Use reputable independent reporting such as Reuters, Bloomberg, Financial Times, MIT Technology Review, TechCrunch, Ars Technica, The Verge, or Wired for corroboration. Aggregators and reposts are discovery-only when a primary source exists. Every factual item must carry clickable source links adjacent to the claim.

SECTION REQUIREMENTS

1. MODEL RELEASES AND MAJOR UPDATES — highest priority
Track frontier, open-weight, multimodal, reasoning, coding, agentic, video, audio, robotics, and scientific models; major checkpoints, APIs, context, pricing, licensing, availability, model cards, benchmarks, and safety reports. Dynamically cover major and emerging labs including OpenAI, Anthropic, Google DeepMind, xAI, Meta, Microsoft, NVIDIA, AMD, Amazon, Apple, Mistral, Cohere, DeepSeek, Qwen/Alibaba, Baidu, ByteDance, and Hugging Face.
For each item include exact date, model and organization, status (Released / Preview / API-only / Open-weight / Research-only), what is genuinely new, verified specifications, availability/license/pricing, why it matters, and direct sources. Never call a tease, leak, rumor, or unofficial leaderboard entry a release.

2. NEW AI PAPERS AND STUDIES
Prioritize novel or high-impact work in language models, multimodal learning, agents, robotics, vision, speech, safety, interpretability, evaluation, inference, and AI systems. Include date, exact title, authors/affiliations when available, contribution, why it matters, evidence status (preprint / accepted / peer reviewed / company study), paper link, and code/project link. Do not claim SOTA unless supported by a comparable evaluation.

3. NEW AND FAST-GROWING GITHUB/HUGGING FACE PROJECTS
Prioritize projects created, publicly released, or substantially updated in the last 7 days with observable developer momentum. Include project, maintainer, date, purpose, reason for attention, license/language/deployment notes, directly verified stars/downloads with UTC check time, and official link. Do not call an old repository new or invent historical star growth.

4. NEW AI PRODUCTS AND STARTUPS
Search Product Hunt, Y Combinator Launch/company/batch pages, official product sites, changelogs, and credible reporting. Prioritize working AI-native launches and material updates. Include product/company, launch date, Product Hunt or YC status, target user/problem, differentiation, verified availability/pricing, and official plus Product Hunt/YC links. Treat promotional claims as claims, not facts.

5. AI LEADER AND INDUSTRY WATCH
Dynamically select only people with material activity in the window. The seed watchlist includes Jensen Huang, Dario Amodei, Lisa Su, Sam Altman, Demis Hassabis, Elon Musk, Mark Zuckerberg, Satya Nadella, Sundar Pichai, Fei-Fei Li, Andrew Ng, Yann LeCun, Andrej Karpathy, Ilya Sutskever, Mira Murati, Mustafa Suleyman, Arthur Mensch, Alexandr Wang, Liang Wenfeng, and any newly relevant researcher, founder, investor, policymaker, or executive.
Include only consequential launches, research, strategy changes, interviews, keynotes, testimony, direct public statements, investments, acquisitions, fundraising, hiring/departures, or policy engagement. Do not force names into the briefing or include gossip, routine reposts, or speculative interpretation. Distinguish direct quotes from paraphrases.

6. OTHER MATERIAL AI INDUSTRY NEWS
Include at most three important items on regulation, partnerships, acquisitions, funding, chips, data centers, energy, safety, security, copyright, or legal decisions. Omit the section if nothing qualifies.

BILINGUAL OUTPUT RULES
- Return one English edition followed by one Simplified Chinese edition.
- Both editions must contain exactly the same selected items, in the same order, with identical dates, numbers, names, titles, certainty labels, and URLs.
- Preserve model, product, repository, and paper names. Preserve paper titles in their original language in Chinese. Translate explanations and headings naturally.
- Use Markdown and inline clickable source links. Do not output the search process, hidden reasoning, discarded candidates, a detached bibliography, or text outside the two tags.

Return exactly this structure:

<ENGLISH>
# AI Intelligence Briefing — REPORT_DATE
**Coverage:** START_UTC–END_UTC
**Generated:** GENERATED_AT_UTC

## Executive Signals
3–5 concise bullets.

## 1. Model Releases and Major Updates
Up to 8 items in a compact Markdown table. Keep cells concise and move supporting detail into links:
| Date | Model / Organization | Status & Access | What Changed | Why It Matters | Sources |
If none qualify, say “No verified qualifying release found.”

## 2. New AI Papers and Studies
Up to 8 items in a Markdown table:
| Date | Paper | Authors / Organization | Contribution | Why It Matters | Status | Sources |

## 3. New and Fast-Growing GitHub/Hugging Face Projects
Up to 8 items in a Markdown table:
| Date | Project | Maintainer | What It Does | Momentum | License | Sources |

## 4. New AI Products and Startups
Up to 6 items in a Markdown table:
| Date | Product / Company | Source | What It Does | Why It Stands Out | Availability | Links |

## 5. AI Leader and Industry Watch
Up to 6 verified material developments.

## 6. Other Material AI Industry News
At most 3 items; omit if empty.

## Editorial Notes
Disclose fallback windows, unverified claims, and important coverage limitations.
</ENGLISH>

<CHINESE>
The complete Simplified Chinese edition with identical items, order, dates, numbers, certainty, and URLs.
</CHINESE>"""


def utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def extract_date_from_filename(filename: str) -> datetime:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    return datetime.strptime(match.group(1), "%Y-%m-%d") if match else datetime.min


def newest_news_age_hours(reference: datetime) -> float | None:
    timestamps = []
    for file_path in OUTPUT_FOLDER.glob("*.json"):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            raw = data.get("timestamp")
            if raw:
                timestamps.append(datetime.strptime(raw, "%Y-%m-%d_%H-%M-%S").replace(tzinfo=timezone.utc))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
    if not timestamps:
        return None
    return (reference - max(timestamps)).total_seconds() / 3600


def collect_response_text_and_citations(result: dict) -> tuple[str, list[str]]:
    text_parts: list[str] = []
    citations: list[str] = []
    for item in result.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(content.get("text", ""))
            for annotation in content.get("annotations", []):
                if annotation.get("type") == "url_citation" and annotation.get("url"):
                    citations.append(annotation["url"])
    for url in result.get("citations", []):
        if isinstance(url, str):
            citations.append(url)
        elif isinstance(url, dict) and url.get("url"):
            citations.append(url["url"])
    return "".join(text_parts).strip(), list(dict.fromkeys(citations))


def parse_bilingual_output(text: str) -> tuple[str, str]:
    English = re.search(r"<ENGLISH>\s*(.*?)\s*</ENGLISH>", text, flags=re.IGNORECASE | re.DOTALL)
    Chinese = re.search(r"<CHINESE>\s*(.*?)\s*</CHINESE>", text, flags=re.IGNORECASE | re.DOTALL)
    if not English or not Chinese:
        raise RuntimeError("API output did not contain complete <ENGLISH> and <CHINESE> sections")
    summary_en = English.group(1).strip()
    summary_zh = Chinese.group(1).strip()
    if not summary_en or not summary_zh:
        raise RuntimeError("One bilingual briefing section was empty")
    return summary_en, summary_zh


def usage_metrics(result: dict, duration_seconds: float) -> dict:
    raw = result.get("usage") or {}
    input_tokens = int(raw.get("input_tokens") or raw.get("prompt_tokens") or 0)
    output_tokens = int(raw.get("output_tokens") or raw.get("completion_tokens") or 0)
    total_tokens = int(raw.get("total_tokens") or (input_tokens + output_tokens))
    input_details = raw.get("input_tokens_details") or raw.get("prompt_tokens_details") or {}
    output_details = raw.get("output_tokens_details") or raw.get("completion_tokens_details") or {}
    cached_tokens = int(input_details.get("cached_tokens") or input_details.get("cached_input_tokens") or 0)
    reasoning_tokens = int(output_details.get("reasoning_tokens") or 0)
    server_usage = result.get("server_side_tool_usage") or raw.get("server_side_tool_usage")
    reported_search_calls = None
    if isinstance(server_usage, dict):
        reported_search_calls = sum(
            int(value)
            for key, value in server_usage.items()
            if "WEB_SEARCH" in str(key).upper()
        )
    output_search_calls = sum(
        1 for item in result.get("output", [])
        if "web_search" in str(item.get("type", "")).lower()
    )
    if reported_search_calls is None and output_search_calls:
        reported_search_calls = output_search_calls

    uncached_input_tokens = max(input_tokens - cached_tokens, 0)
    token_cost = (
        uncached_input_tokens * PRICING["input_per_million"]
        + cached_tokens * PRICING["cached_input_per_million"]
        + output_tokens * PRICING["output_per_million"]
    ) / 1_000_000
    search_cost = (
        reported_search_calls * PRICING["web_search_per_call"]
        if reported_search_calls is not None else None
    )
    estimated_cost = token_cost + (search_cost or 0)
    cost_is_lower_bound = reported_search_calls is None
    return {
        "model": MODEL,
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "total_tokens": total_tokens,
        "web_search_calls": reported_search_calls,
        "duration_seconds": round(duration_seconds, 2),
        "estimated_token_cost_usd": round(token_cost, 6),
        "estimated_web_search_cost_usd": round(search_cost, 6) if search_cost is not None else None,
        "estimated_cost_usd": round(estimated_cost, 6),
        "pricing": PRICING,
        "cost_is_estimate": True,
        "cost_is_lower_bound": cost_is_lower_bound,
        "server_side_tool_usage": server_usage if isinstance(server_usage, dict) else None,
        "billing_note": (
            "Estimated from OpenCode Go Grok 4.5 token rates plus xAI's published web-search rate; the provider's billed amount may differ."
            if not cost_is_lower_bound else
            "Token-cost lower bound. The OpenCode response did not report billable web-search calls, so provider tool charges are not included."
        ),
    }


def request_bilingual_summary(window_start: datetime, window_end: datetime) -> tuple[str, str, list[str], dict]:
    start_utc = utc_iso(window_start)
    end_utc = utc_iso(window_end)
    report_date = window_end.strftime("%Y-%m-%d")
    user_prompt = f"""Research and produce the bilingual AI Intelligence Briefing for {report_date}.

Primary coverage window:
- Start: {start_utc}
- End: {end_utc}
- Generated at: {end_utc}

Model releases and major model updates are the highest priority. Use web search extensively, verify dates against the UTC window, prioritize primary sources, and return only the final bilingual briefing in the required <ENGLISH> and <CHINESE> structure. Replace REPORT_DATE, START_UTC, END_UTC, and GENERATED_AT_UTC with the exact values above."""
    payload = {
        "model": MODEL,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "tools": [{"type": "web_search"}],
        "temperature": 0.2,
        "max_output_tokens": 10000,
    }
    started = time.monotonic()
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=600,
    )
    duration = time.monotonic() - started
    if response.status_code != 200:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")
    result = response.json()
    text, citations = collect_response_text_and_citations(result)
    if not text:
        raise RuntimeError("API returned no text")
    summary_en, summary_zh = parse_bilingual_output(text)
    return summary_en, summary_zh, citations, usage_metrics(result, duration)


def update_index_json(generated_at: datetime) -> None:
    files = sorted((f.name for f in OUTPUT_FOLDER.glob("*.json")), key=extract_date_from_filename, reverse=True)
    data = {"last_updated": generated_at.isoformat(), "total_files": len(files), "files": files}
    (ROOT / "public" / "index.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Updated public/index.json with {len(files)} news files")


def main() -> None:
    if not API_KEY:
        print("Error: OPENCODE_GO_API_KEY environment variable is not set")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    force = os.getenv("FORCE_GENERATE", "").lower() in {"1", "true", "yes"}
    recent_age = newest_news_age_hours(now)
    if not force and recent_age is not None and recent_age < 20:
        print(f"Skipping generation: newest briefing is only {recent_age:.2f} hours old")
        return

    window_start = now - timedelta(hours=24)
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = OUTPUT_FOLDER / f"grok_news_summary_{timestamp}.json"

    try:
        summary_en, summary_zh, citations, usage = request_bilingual_summary(window_start, now)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    output_file.write_text(
        json.dumps(
            {
                "timestamp": timestamp,
                "coverage_start_utc": utc_iso(window_start),
                "coverage_end_utc": utc_iso(now),
                "summary": summary_en,
                "summary_en": summary_en,
                "summary_zh": summary_zh,
                "citations": citations,
                "usage": usage,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Summary saved to {output_file.relative_to(ROOT)}")
    print(
        "Generation usage: "
        f"{usage['input_tokens']} input + {usage['output_tokens']} output = {usage['total_tokens']} total tokens; "
        f"{usage['web_search_calls'] if usage['web_search_calls'] is not None else 'unreported'} web searches; estimated ${usage['estimated_cost_usd']:.6f}"
    )
    update_index_json(now)


if __name__ == "__main__":
    main()
