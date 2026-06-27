---
name: wfs-marketing-pb-cognition-en
description: Convert an English Wallace Wang cognition/business/sales oral script into publish-ready English marketing fields, format the script for readability without changing any words, choose English business/cognition tags, and write the issue into the WWFS Marketing publish center under "Wallace认知圈". Use when the user provides an English cognition video script or text and says "英文认知圈视频写入Wallace认知圈", "English cognition video to Wallace认知圈", "写入Wallace认知圈", "publish to Wallace认知圈", "新建英文认知圈一期", or asks to create English title/cover title/tags/description for marketing.wallacewang.ca/publish.
---

# WFS Marketing PB Cognition EN

Use this skill to turn an English Wallace Wang cognition, business, entrepreneurship, or sales oral script into a `Wallace认知圈` issue in the WWFS Marketing publish center.

## Inputs

- English oral script: usually a `.txt` file path or pasted transcript.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If the user says `ai-title-analysis-rule.md`, look for the actual local file first; in this environment it has historically been named `ai-title-data-analysis-rule.md`.
- Destination phrase: when the user says `英文认知圈视频写入Wallace认知圈`, `English cognition video to Wallace认知圈`, or `写入Wallace认知圈`, create or update an issue for the `Wallace认知圈` IP.

## Core Workflow

1. Read the title rule files and the English oral script with explicit UTF-8.
2. Generate English:
   - `标题`
   - `封面标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
3. Do not generate or use a cover subtitle for English unless the user explicitly asks. Leave `封面副标题` empty.
4. Open or use `https://marketing.wallacewang.ca/publish` in an authenticated browser session.
5. Select the `Wallace认知圈` IP tab.
6. Before creating, check for an existing issue with the same source file path, script number, or title. If it exists, update missing/weak fields instead of duplicating it.
7. If no issue exists, click `+ 新建一期`, fill fields, and click `创建本期`.
8. Verify the issue appears under `Wallace认知圈` and has the Wallace认知圈 platform set: 小红书, 抖音, 视频号, TikTok, X, Instagram, FaceBook, LinkedIn, YouTube.

## YouTube Popularity Mining Before Title Generation

Before generating titles for an English cognition/business publish task, run a YouTube trend-mining step when browser access is available and the task is not urgent:

1. Extract 3-6 English search keywords from the script, including the business topic, audience, pain point, and contrarian angle. Examples: `customer says too expensive`, `sales objection price`, `business mindset`, `customer value`, `entrepreneurship lessons`, `how to sell value`.
2. Open YouTube search URLs sorted by Popularity when possible, for example: `https://www.youtube.com/results?search_query=<keyword>&sp=CAM%253D`.
3. Inspect visible results and capture useful title/thumbnail patterns plus visible signals such as views and age.
4. Keep up to 10 usable videos/posts across relevant searches.
5. Analyze repeated words, hook structures, audience labels, anxiety/benefit/risk phrases, and outdated clickbait to avoid.
6. Generate the issue title and self-contained cover title from verified patterns plus the current script's actual content.

If YouTube blocks access, returns irrelevant results, or reliable signals are unavailable, state the limitation, use the local title rules and accumulated word bank, and still complete the publish workflow.

## English Cognition Title Rules

Follow the user's title system, adapted for English cognition/business content:

- First extract theme, audience, pain point, misconception, and risk boundaries.
- If no fresh platform samples are available, rely on the local rule files, historical word bank, and script terms; do not pretend there is fresh external data.
- Prefer business cognition, sales cognition, entrepreneurship, work reflection, value perception, client psychology, and personal growth angles.
- Keep the title educational and grounded in the script. Do not turn a cognition/business script into a finance topic unless the script itself is about finance.
- Avoid overpromising, guru-style hype, and empty clickbait such as `secret formula`, `guaranteed`, `one trick`, `make millions overnight`, or `everyone is wrong`.
- Use clear, human English. Titles should feel like a smart YouTube/short-video business insight, not a product ad.

## English Cover Title Rule

Because English posts normally do not use a cover subtitle, make `封面标题` self-contained:

- Include the core business/cognition keywords from the script, such as `Price Objection`, `Customer Value`, `Sales`, `Entrepreneurship`, `Business Mindset`, `Value vs Price`, or `Client Psychology`.
- Prefer clear meaning over vague punchlines.
- Good examples:
  - `Price Is Not the Real Problem`
  - `Sell Value, Not Discounts`
  - `When Customers Say Too Expensive`
  - `Customer Value Beats Price`
  - `The Sales Lesson I Needed`
- Avoid vague standalone cover titles such as `What? Why?` unless the user explicitly wants a curiosity-only cover.

## Accumulated English Cognition Word Bank

Use these as reusable ingredients, not mandatory phrases. Keep titles truthful and grounded in the script.

### Sales, Customer Value, Price Objections

- `When Customers Say Too Expensive`
- `Price Is Not the Real Problem`
- `Sell Value, Not Discounts`
- `Customer Value Beats Price`
- `The Real Price Objection`
- `Stop Defending Your Price`
- `Make the Value Obvious`
- `They Don't See the Value Yet`
- `Value Before Price`
- `The Honda vs Lamborghini Lesson`
- `A 50-Year Business Lesson`
- `What Business Owners Miss`
- `Client Psychology`
- `Sales Mindset`

### Entrepreneurship, Work, Cognition

- `Business Mindset`
- `Entrepreneurship Lesson`
- `The Lesson I Needed`
- `What Experience Teaches You`
- `Human Nature Hasn't Changed`
- `The Real Problem Wasn't What I Thought`
- `A Simple Lesson That Changed How I Think`
- `Before You Lower Your Price`
- `Don't Lose Before You Sell`
- `This Is Where Owners Get Stuck`

Use with caution:

- Avoid `get rich`, `secret`, `guaranteed`, `unstoppable`, `crush sales`, or aggressive guru-style copy unless the user explicitly asks for a hard-sell style.
- Prefer `lesson`, `mindset`, `value`, `before`, `what customers really mean`, and `why price is not the whole story`.

## English Description Style

The `描述` goes into `备注(内部使用,不发到平台)`.

Write a hook, not a simple summary:

- Paragraph 1: start with the exact question/fear the audience already has.
- Paragraph 2: introduce the counterintuitive twist without giving away everything.
- Paragraph 3: explain why the viewer should watch to the end.
- Final line: include `Source: <original path>` when a source file path is provided.

Example shape:

```text
When a customer says, "you are too expensive," do you immediately start defending your fee or trying to make the price sound smaller?

This video starts with a wedding conversation, but the real lesson came from a businessman who has sold bolts and nuts for more than 50 years. His reaction to one simple pricing objection was not a technique. It was belief.

Watch to the end, because the Honda versus Lamborghini example flips the whole question: maybe the problem is not price at all. Maybe the customer simply has not seen the value yet.

Source: E:\00Wallace\07 视频日记\...
```

## Preferred English Tag Pool

Choose a relevant subset from this pool based on script content. Do not include all tags blindly.

```text
#Business
#Entrepreneurship
#Sales
#SalesMindset
#CustomerValue
#ClientPsychology
#BusinessMindset
#ValueCreation
#PricingStrategy
#SmallBusiness
#FounderMindset
#Leadership
#WorkMindset
#PersonalGrowth
#CommunicationSkills
#BusinessLessons
#CanadaBusiness
#CanadianBusiness
#ServiceBusiness
#FinancialPlanningBusiness
```

Selection guidance:

- Sales/price objection/customer value scripts: use tags such as `#Sales`, `#SalesMindset`, `#CustomerValue`, `#ClientPsychology`, `#PricingStrategy`, `#BusinessLessons`.
- Entrepreneurship/business-owner scripts: use tags such as `#Business`, `#Entrepreneurship`, `#SmallBusiness`, `#FounderMindset`, `#CanadaBusiness`, `#CanadianBusiness`.
- Work reflection/personal cognition scripts: use tags such as `#BusinessMindset`, `#WorkMindset`, `#PersonalGrowth`, `#CommunicationSkills`, `#Leadership`.
- Financial-planning-business scripts can include `#FinancialPlanningBusiness`, but avoid personal-finance tags unless the script is actually about finance.

## Script Formatting Rule

For `主内容 / 口播稿`, make the English transcript readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original word, including transcription mistakes, filler phrases, repeated sentences, awkward phrasing, and mixed-language fragments.
- Add punctuation and paragraph breaks.
- Merge line breaks into readable sentence groups.
- Keep original casing unless punctuation creates a natural sentence boundary.

Do not:

- Correct transcription errors.
- Rewrite, polish, paraphrase, delete, or add words.
- Summarize the script in the main content field.
- Convert the topic into finance, tax, or investment content unless the original script says so.

## Publishing Procedure

Use an authenticated browser session for `https://marketing.wallacewang.ca/publish`.

1. Open the publish page if it is not already open.
2. If logged out, ask the user to log in.
3. Click the `Wallace认知圈` tab.
4. Check existing issues for duplicate source path, same script number, or same title.
5. If an issue exists, click `编辑标题/备注` and update fields that are missing or below this skill's standard.
6. If no issue exists, click `+ 新建一期` and fill:
   - `IP` = `Wallace认知圈`
   - `标题(平台帖子/视频标题)` = generated English title
   - `封面标题` = generated self-contained English cover title
   - `封面副标题` = blank unless explicitly requested
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = chosen English business/cognition tags
   - `主内容 / 口播稿` = formatted English script
   - `备注(内部使用,不发到平台)` = hook-style English description and source path
7. Leave platform defaults alone unless the user asks otherwise.
8. Save/create and verify the issue appears under `Wallace认知圈` with 9 platforms.

## Browser and API Notes

- Prefer the current authenticated browser page when available, because the publish API is protected by login cookies.
- Do not use server SSH or database edits unless the user explicitly asks for direct server maintenance.
- Use screenshots or DOM state to verify the selected tab, field placement, and final platform list.
- If a click or paste misses, do not submit; correct the field first.

## Final Response

Keep the final response brief. Confirm creation or update and list the exact fields used:

- 标题
- 封面标题
- 标签

Mention that `封面副标题` was left blank for English, the hook description went into remarks, and the formatted script went into `主内容 / 口播稿`.
