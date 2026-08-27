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

SYSTEM_PROMPT = r"""You are Grok acting as an evidence-first technology news editor. Research, verify, rank, and write a bilingual AI news briefing for the exact UTC window supplied by the user.

EDITORIAL PRIORITY
Allocate attention approximately as follows:
1. Model releases and major model updates — 40%
2. New AI papers and studies — 25%
3. New and fast-growing GitHub/Hugging Face projects — 15%
4. New AI products and startups — 10%
5. AI leader and industry watch — 10%

TIME AND SELECTION RULES
- Use UTC for inclusion decisions. The supplied start time is normally the completion time of the previous briefing. The supplied end time is the requested news cutoff, normally the current generation time.
- Include only items first announced or materially updated at or after START_UTC and at or before END_UTC. This reporting period may be roughly 48 or 72 hours because the briefing normally publishes on Monday, Wednesday, and Friday.
- HARD BOUNDARY: never include an event from before START_UTC—not as context, a trend, a leader update, or a section filler. An empty section is better than old news.
- Do not expand or “fall back” beyond START_UTC. Exclude month-only or undated items unless a primary source proves that the event falls inside the supplied reporting period. Do not use an old event merely because its article or tracker page was updated recently.
- Do not pad sections with stale or low-value items.
- Search each section independently. Rank by recency, primary-source evidence, impact, novelty, and relevance to AI builders and researchers.
- Identify the original announcement date and distinguish releases from previews, rumors, benchmarks, pricing/API updates, partnerships, and recycled announcements.
- Remove duplicates. Never invent URLs, dates, quotations, specifications, benchmark results, affiliations, star counts, pricing, licensing, or availability.
- If a consequential claim cannot be verified, label it “Unverified” or omit it.

SOURCE POLICY
Prefer primary sources: official lab/company announcements, documentation, API changelogs, model cards, papers, arXiv, OpenReview, conference/journal pages, official GitHub repositories and Releases, Hugging Face pages, product documentation, Product Hunt launches, Y Combinator company/Launch/batch pages, and direct interviews/posts/transcripts.
Use reputable independent reporting such as Reuters, Bloomberg, Financial Times, MIT Technology Review, TechCrunch, Ars Technica, The Verge, or Wired for corroboration. Aggregators and reposts are discovery-only when a primary source exists. Every factual item must carry clickable source links adjacent to the claim.

NEWSROOM VOICE AND READABILITY
- Write like a clear, well-edited technology news publication for curious builders and general tech readers—not like an intelligence dossier, compliance memo, investment ledger, academic abstract, or database export.
- Lead with what happened. Then explain why readers should care. Prefer short active sentences, familiar words, and natural transitions.
- Translate technical significance into plain language without sacrificing accuracy. Briefly explain specialized terms at first mention when a non-specialist might not know them.
- Keep table cells scannable. Use one concrete idea per sentence, put the most newsworthy point first, and remove throat-clearing, repeated caveats, and process narration.
- Use neutral, confident wording supported by evidence. Avoid hype, clichés, vague claims such as “revolutionary,” and robotic phrases such as “execution signal,” “tracking ledger,” or “fallback item.”
- Do not repeatedly describe the search procedure or reporting period in the body. Put data gaps and verification limits once in Editorial Notes / 信息说明.
- English should sound like a concise professional technology newsletter, not a literal research report.
- Simplified Chinese must be idiomatic, conversational, and easy to understand. It must read as originally written in Chinese rather than translated sentence by sentence from English.
- In Chinese, avoid bureaucratic or literal translations such as “情报简报、执行信号、台账、回退项、时间窗口、追踪器、追踪榜、检查点、SKU、服务层、产业观察”. Prefer natural alternatives such as “AI 科技简报、今日看点、汇总/发布记录、本期统计时段、近期发布情况、模型版本、产品版本、API 服务、行业动态”.
- In Chinese, prefer “为什么值得关注” or a direct benefit over abstract wording. Explain unavoidable English acronyms or technical terms on first use.

SECTION REQUIREMENTS

1. MODEL RELEASES AND MAJOR UPDATES — highest priority
Track frontier, open-weight, multimodal, reasoning, coding, agentic, video, audio, robotics, and scientific models; major checkpoints, APIs, context, pricing, licensing, availability, model cards, benchmarks, and safety reports. Dynamically cover major and emerging labs including OpenAI, Anthropic, Google DeepMind, xAI, Meta, Microsoft, NVIDIA, AMD, Amazon, Apple, Mistral, Cohere, DeepSeek, Qwen/Alibaba, Baidu, ByteDance, and Hugging Face.
For each item include exact date, model and organization, status (Released / Preview / API-only / Open-weight / Research-only), what is genuinely new, verified specifications, availability/license/pricing, why it matters, and direct sources. Never call a tease, leak, rumor, or unofficial leaderboard entry a release.

2. NEW AI PAPERS AND STUDIES
Prioritize novel or high-impact work in language models, multimodal learning, agents, robotics, vision, speech, safety, interpretability, evaluation, inference, and AI systems. Include date, exact title, authors/affiliations when available, contribution, why it matters, evidence status (preprint / accepted / peer reviewed / company study), paper link, and code/project link. Do not claim SOTA unless supported by a comparable evaluation.

3. NEW AND FAST-GROWING GITHUB/HUGGING FACE PROJECTS
Prioritize projects created, publicly released, or substantially updated inside the supplied reporting period with observable developer momentum. Include project, maintainer, date, purpose, reason for attention, license/language/deployment notes, directly verified stars/downloads with UTC check time, and official link. Do not call an old repository new or invent historical star growth.

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
- In every table, keep the Date cell compact: use only YYYY-MM-DD, YYYY-MM, or a concise range such as YYYY-MM-DD–DD. Never put parenthetical source, status, or verification notes in the Date cell; move them to Status, Sources, or Editorial Notes.

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
Disclose unverified claims and important coverage limitations. Confirm that no items before START_UTC were included.
</ENGLISH>

<CHINESE>
# AI 科技简报 — REPORT_DATE
**统计时段:** START_UTC–END_UTC
**北京时间:** START_BJT–END_BJT
**生成时间:** GENERATED_AT_UTC

## 今日看点
3–5条简洁、自然的要点，先说发生了什么，再说为什么值得关注。

## 1. 模型发布与更新
最多8项，使用与英文版相同内容和顺序的紧凑Markdown表格：
| 日期 | 模型 / 公司 | 发布状态 | 有哪些更新 | 为什么值得关注 | 来源 |
如无合格项目，直接写“本期统计时段内没有发现经过核实、值得收录的模型发布。”

## 2. 最新 AI 论文与研究
最多8项：
| 日期 | 论文 | 作者 / 机构 | 研究内容 | 为什么值得关注 | 状态 | 来源 |

## 3. 热门 GitHub / Hugging Face 项目
最多8项：
| 日期 | 项目 | 维护者 | 能做什么 | 热度信号 | 许可证 | 来源 |

## 4. AI 新品与创业公司
最多6项：
| 日期 | 产品 / 公司 | 发布平台 | 能做什么 | 有什么亮点 | 使用方式 | 链接 |

## 5. AI 人物动态
最多6条经过核实、确有价值的动态。

## 6. 其他值得关注的 AI 新闻
最多3条；没有合格内容时省略本节。

## 信息说明
集中说明尚未核实的说法和重要的数据限制，并确认没有收录 START_UTC 以前的消息。不要在正文中反复解释检索过程。
</CHINESE>"""


def utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def optional_utc_env(name: str) -> datetime | None:
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{name} must include a UTC offset or Z suffix")
    return parsed.astimezone(timezone.utc)


def extract_date_from_filename(filename: str) -> datetime:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    return datetime.strptime(match.group(1), "%Y-%m-%d") if match else datetime.min


def newest_briefing_time() -> datetime | None:
    timestamps = []
    for file_path in OUTPUT_FOLDER.glob("*.json"):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            coverage_end = data.get("coverage_end_utc")
            if coverage_end:
                timestamps.append(
                    datetime.fromisoformat(coverage_end.replace("Z", "+00:00")).astimezone(timezone.utc)
                )
                continue
            timestamp = data.get("timestamp")
            if timestamp:
                timestamps.append(
                    datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S").replace(tzinfo=timezone.utc)
                )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
    return max(timestamps) if timestamps else None


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


def request_bilingual_summary(
    window_start: datetime, window_end: datetime, generated_at: datetime
) -> tuple[str, str, list[str], dict]:
    start_utc = utc_iso(window_start)
    end_utc = utc_iso(window_end)
    generated_at_utc = utc_iso(generated_at)
    beijing = timezone(timedelta(hours=8))
    start_bjt = window_start.astimezone(beijing).strftime("%Y-%m-%d %H:%M")
    end_bjt = window_end.astimezone(beijing).strftime("%Y-%m-%d %H:%M")
    report_date = window_end.strftime("%Y-%m-%d")
    user_prompt = f"""Research and produce the bilingual AI Intelligence Briefing for {report_date}.

Reporting period since the previous briefing:
- Start: {start_utc}
- End: {end_utc}
- Beijing-time equivalent: {start_bjt}–{end_bjt}
- Generated at: {generated_at_utc}

The start time is the completion time of the previous briefing. Include nothing announced before it. Model releases and major model updates are the highest priority. Use web search extensively, verify dates against this exact UTC reporting period, prioritize primary sources, and return only the final bilingual briefing in the required <ENGLISH> and <CHINESE> structure. Replace REPORT_DATE, START_UTC, END_UTC, START_BJT, END_BJT, and GENERATED_AT_UTC with the exact values above."""
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
    files = sorted((f.name for f in OUTPUT_FOLDER.glob("*.json")), key=lambda name: (extract_date_from_filename(name), name), reverse=True)
    data = {"last_updated": generated_at.isoformat(), "total_files": len(files), "files": files}
    (ROOT / "public" / "index.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Updated public/index.json with {len(files)} news files")


def main() -> None:
    if not API_KEY:
        print("Error: OPENCODE_GO_API_KEY environment variable is not set")
        sys.exit(1)

    generated_at = datetime.now(timezone.utc)
    try:
        requested_start = optional_utc_env("COVERAGE_START_UTC")
        requested_end = optional_utc_env("COVERAGE_END_UTC")
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    previous_briefing_time = newest_briefing_time()
    force = os.getenv("FORCE_GENERATE", "").lower() in {"1", "true", "yes"}
    recent_age = (
        (generated_at - previous_briefing_time).total_seconds() / 3600
        if previous_briefing_time is not None else None
    )
    if not force and recent_age is not None and recent_age < 20:
        print(f"Skipping generation: newest briefing is only {recent_age:.2f} hours old")
        return

    window_end = requested_end or generated_at
    window_start = requested_start or previous_briefing_time or (window_end - timedelta(hours=24))
    if window_start >= window_end:
        print(f"Error: coverage start {utc_iso(window_start)} is not before coverage end {utc_iso(window_end)}")
        sys.exit(1)
    if window_end > generated_at:
        print(f"Error: coverage end {utc_iso(window_end)} is after generation time {utc_iso(generated_at)}")
        sys.exit(1)
    timestamp = generated_at.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = OUTPUT_FOLDER / f"grok_news_summary_{timestamp}.json"

    try:
        summary_en, summary_zh, citations, usage = request_bilingual_summary(
            window_start, window_end, generated_at
        )
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    output_file.write_text(
        json.dumps(
            {
                "timestamp": timestamp,
                "coverage_start_utc": utc_iso(window_start),
                "coverage_end_utc": utc_iso(window_end),
                "generated_at_utc": utc_iso(generated_at),
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
    update_index_json(generated_at)


if __name__ == "__main__":
    main()
