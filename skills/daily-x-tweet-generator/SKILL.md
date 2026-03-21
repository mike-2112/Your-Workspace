---
name: daily-x-tweet-generator
description: Generates 5 fresh, witty X posts (one per topic) using only <24h old content. Runs daily at noon ET via cron.
version: 1.0
---

# Daily X Tweet Generator Skill

## Core Rules (NEVER break these)
- This skill runs daily at 12:00 noon ET.
- Topics (fixed): Astrophysics, muscle cars, scifi and fantasy entertainment, artificial intelligence, heavy metal music.
- For EACH topic you MUST:
  1. First use web_search or x_keyword_search with strict time filter ("past 24 hours" or since:YYYY-MM-DD).
  2. Pick ONE genuinely cool/recent article, news story, or viral X post.
  3. Use browse_page on the link to confirm it is live and relevant.
  4. Write one fun, witty, postable X tweet (<280 chars, emoji OK, engaging tone).
- Never use old content. If nothing good in last 24h, say "No strong story today for [topic]" and skip.
- Never include broken/dead links.
- Output format: Numbered 1–5 with the tweet text + source link + one-sentence why it's cool.
- Style: Witty, bold, liberty-minded, slightly irreverent, justice-focused, emoji-friendly, in the spirit of @TknIt3Z (freedom, no-nonsense takes, ⚖️🗽 vibe).

## Model Usage
Switch to Grok 4.20 Reasoning first (`/model openai/grok-4.20-0309-reasoning` or `openai/grok-4.20-reasoning-latest`). Use it for all search synthesis and tweet writing — it is vastly better at wit and freshness than the fast model.

## How to Trigger Manually (for testing)
Just say: "Run daily-x-tweet-generator skill"

## Cron Integration
This skill is designed to be called by cron. When triggered by cron it will generate the 5 posts and send them directly to the main session (or your preferred channel).

Update this skill if patterns improve.
