---
name: wfs-marketing-pb-youtube-cn
description: Convert a Chinese Wallace Wang finance YouTube long-video oral script into publish-ready Chinese marketing fields, format the script for readability without changing any words, choose Chinese finance tags from the existing preferred tag pool, and write the issue into the WWFS Marketing publish center under "YouTube长视频". Use when the user provides a 中文YouTube长视频口播稿/script file or text and says "中文YouTube长视频写入YouTube长视频", "中文长视频写入YouTube长视频", "写入YouTube长视频", "发布到YouTube长视频", "新建中文长视频一期", or asks to create Chinese title/cover/subtitle/tags/description for marketing.wallacewang.ca/publish.
---

# WFS Marketing PB YouTube CN

Use this skill to turn a Chinese Wallace Wang finance YouTube long-video script into a new `YouTube长视频` issue in the WWFS Marketing publish center.

## Inputs

- Chinese YouTube long-video oral script: usually a `.txt` file path or pasted Chinese口播稿.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If either file is missing, state it briefly and use the latest available title-system rules from context.
- Destination phrase: when the user says `中文YouTube长视频写入YouTube长视频`, `中文长视频写入YouTube长视频`, or `写入YouTube长视频`, create or update an issue for the `YouTube长视频` IP.

## Core Workflow

1. Read the title rule files and the口播稿 with explicit UTF-8.
2. Use only the Chinese口播 portion unless the user explicitly asks to include another language section.
3. Generate:
   - `标题`
   - `封面标题`
   - `封面副标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
4. Open or use `https://marketing.wallacewang.ca/publish` in an authenticated browser session.
5. Select the `YouTube长视频` IP tab.
6. Before creating, check for an existing issue with the same source file path, same script number, or same title. If it exists, update missing/weak fields instead of duplicating it.
7. If no issue exists, click `+ 新建一期`, fill fields, and click `创建本期`.
8. Verify the issue appears under `YouTube长视频` and has the YouTube长视频 platform set: 小红书, 抖音, 视频号, TikTok, X, Instagram, FaceBook, LinkedIn, YouTube.

## Title Generation Rules

Keep the same title/cover/tag direction as `wfs-marketing-pb-cn`:

- Follow the user's title system.
- First extract the script's theme, audience, pain point, misconception, and compliance risks.
- If no fresh platform爆款 samples are provided or accessible, state briefly that this run lacks fresh platform evidence and relies on the local rule files, historical word bank, and the script's own terms.
- Avoid unsafe financial claims:
  - Do not use `稳赚`, `保证省税`, `闭眼买`, `必买`, `内部方法`, `快上车`, `最佳方案`, or absolute tax/investment conclusions.
  - Prefer `可能`, `先看是否适合自己`, `常见思路`, `看懂逻辑`, `不一定是重点`.
- Prefer educational, risk-reminder, misconception-correction language.
- Keep cover title short, generally 6-12 Chinese characters.
- Make the description a hook, not a summary. It should create curiosity and encourage watching the full long video.

## Xiaohongshu Trend Mining Before Title Generation

Before generating titles, run a Xiaohongshu trend-mining step when network/browser access is available and the task is not urgent:

1. Extract 3-6 search keywords from the script, including the financial/account term, audience term, pain point, and surprising angle.
2. Search Xiaohongshu with these keywords. Prefer current posts in the same topic or adjacent finance topics.
3. Rank visible candidate posts by likes and comments.
4. Keep up to 10 usable posts, record cover title, post title, visible likes/comments, and relevance.
5. Analyze high-frequency words, hook structures, audience labels, anxiety/benefit/risk phrases, and outdated or over-clickbait phrases to avoid.
6. Generate title, cover title, and cover subtitle using verified patterns plus the current script's actual content.

If Xiaohongshu is blocked, logged out, rate-limited, or interaction counts are unavailable, state the limitation and still complete the publish workflow.

## Accumulated Chinese Viral Word Bank

Use the same finance-oriented ingredients as `wfs-marketing-pb-cn`. Keep titles truthful, educational, and compliance-safe.

### Retirement, RRSP/RSP, Tax Residency

- `退休后才发现`
- `别只看退税`
- `RSP太多`
- `RRSP取钱`
- `税务居民身份`
- `非税务居民`
- `25%预扣税`
- `离境税`
- `退休税率`
- `这笔税差很多`
- `不是搬走就行`
- `先算清楚身份`
- `高收入退休`
- `加拿大退休规划`
- `账户太大也有烦恼`
- `真正关键不是账户`
- `别等退休才懂`

Compliance notes:

- Avoid implying that tax residency, investing, insurance, or borrowing strategies are simple, guaranteed, or suitable for everyone.
- Prefer `可能`, `先算清楚`, `不一定适合所有人`, `身份和账都要算清楚`, `看懂逻辑`.
- Avoid `保证省税`, `移民避税秘籍`, `一招省税`, `税局查不到`, `无脑搬走`, `稳赚`.

## Preferred Chinese Tag Pool

Choose a relevant subset from this pool based on the Chinese oral script content. Do not include all tags blindly.

```text
#复利
#避税复利
#FHSA
#加拿大避税
#加拿大合理避税
#加拿大投资
#加拿大养老金
#加拿大开公司
#创业
#移民
#RESP
#加拿大教育基金
#加拿大理财
#加拿大创业
#加拿大公司理财
#加拿大资产传承
#加拿大信托
#加拿大保险
#加拿大理财顾问
```

Selection guidance:

- 投资/账户/复利/税务主题：优先 `#加拿大投资`, `#加拿大理财`, `#复利`, `#避税复利`, `#加拿大避税`, `#加拿大合理避税`.
- TFSA/RRSP/FHSA/RESP/教育金主题：根据稿件具体账户选择 `#FHSA`, `#RESP`, `#加拿大教育基金`, `#加拿大理财`.
- 养老金/退休主题：优先 `#加拿大养老金`, `#加拿大理财`, `#复利`.
- 开公司/创业/公司理财主题：优先 `#加拿大开公司`, `#创业`, `#加拿大创业`, `#加拿大公司理财`.
- 保险/资产传承/信托主题：优先 `#加拿大保险`, `#加拿大资产传承`, `#加拿大信托`, `#加拿大理财顾问`.
- 移民身份或新移民场景明显时，加入 `#移民`.

## Description Style

The `描述` goes into `备注(内部使用,不发到平台)`.

Write 2-4 short paragraphs:

- Paragraph 1: open with the audience's concrete question or fear.
- Paragraph 2: tease the counterintuitive point without giving away the whole answer.
- Paragraph 3: explain why watching the whole long video matters.
- Final line: include `来源：<original path>` when a source file path is provided.

## Script Formatting Rule

For `主内容 / 口播稿`, make the script readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original Chinese word and filler word, including `啊`, `呃`, `哈`, `呢`.
- Add Chinese punctuation and paragraph breaks.
- Merge line breaks into natural sentences.
- Use only the Chinese口播 portion unless the user explicitly asks to include another language section.

Do not:

- Rewrite, polish, paraphrase, delete, or add words.
- Convert `RSP` to `RRSP` unless the original line already says `RRSP`.
- Remove filler words.
- Summarize the script in the main content field.

## Publishing Procedure

Use an authenticated browser session for `https://marketing.wallacewang.ca/publish`.

1. Open the publish page if it is not already open.
2. If logged out, ask the user to log in.
3. Click the `YouTube长视频` tab.
4. Check existing issues for duplicate source path, same script number, or same title.
5. If an issue exists, click `编辑标题/备注` and update fields that are missing or below this skill's standard.
6. If no issue exists, click `+ 新建一期` and fill:
   - `IP` = `YouTube长视频`
   - `标题(平台帖子/视频标题)` = generated title
   - `封面标题` = generated cover title
   - `封面副标题` = generated cover subtitle
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = generated tags
   - `主内容 / 口播稿` = formatted Chinese script
   - `备注(内部使用,不发到平台)` = hook-style description and source path
7. Leave platform defaults alone unless the user asks otherwise.
8. Save/create and verify the issue appears under `YouTube长视频` with 9 platforms.

## Browser and API Notes

- Prefer the current authenticated browser page when available, because the publish API is protected by login cookies.
- Do not use server SSH or database edits unless the user explicitly asks for direct server maintenance.
- Use screenshots or DOM state to verify the selected tab, field placement, and final platform list.

## Final Response

Keep the final response brief. Confirm creation or update and list:

- 标题
- 封面标题
- 封面副标题
- 标签

Mention that the description went into remarks and the formatted script went into `主内容 / 口播稿`.
