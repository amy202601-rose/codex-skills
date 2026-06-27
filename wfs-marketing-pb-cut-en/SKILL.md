---
name: wfs-marketing-pb-cut-en
description: Convert an English Wallace Wang finance knowledge-slice oral script into publish-ready English marketing fields, format the script for readability without changing any words, choose English finance tags from the existing preferred tag pool, and write the issue into the WWFS Marketing publish center under "知识切片". Use when the user provides an English knowledge-slice script or text and says "英文知识切片视频写入知识切片", "English knowledge slice to 知识切片", "英文知识切片写入知识切片", "写入知识切片", "publish to 知识切片", "新建英文知识切片一期", or asks to create English title/cover title/tags/description for marketing.wallacewang.ca/publish.
---

# WFS Marketing PB Cut EN

Use this skill to turn an English Wallace Wang finance knowledge-slice script into a new `知识切片` issue in the WWFS Marketing publish center.

## Inputs

- English knowledge-slice oral script: usually a `.txt` file path or pasted transcript.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If the user says `ai-title-analysis-rule.md`, look for the actual local file first; in this environment it has historically been named `ai-title-data-analysis-rule.md`.
- Destination phrase: when the user says `英文知识切片视频写入知识切片`, `English knowledge slice to 知识切片`, or `写入知识切片`, create or update an issue for the `知识切片` IP.

## Core Workflow

1. Read the title rule files and the oral script with explicit UTF-8.
2. Generate English:
   - `标题`
   - `封面标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
3. Do not generate or use a cover subtitle for English unless the user explicitly asks. Leave `封面副标题` empty.
4. Open or use `https://marketing.wallacewang.ca/publish` in an authenticated browser session.
5. Select the `知识切片` IP tab.
6. Before creating, check for an existing issue with the same source file path, script number, or title. If it exists, update missing/weak fields instead of duplicating it.
7. If no issue exists, click `+ 新建一期`, fill fields, and click `创建本期`.
8. Verify the issue appears under `知识切片` and has the 知识切片 platform set: 小红书, 抖音, 视频号, TikTok, X, Instagram, FaceBook, LinkedIn, YouTube.

## YouTube Popularity Mining Before Title Generation

Keep the same title/cover/tag direction as `wfs-marketing-pb-en`. Before generating titles, run a YouTube trend-mining step when browser access is available and the task is not urgent:

1. Extract 3-6 English search keywords from the script, including the financial topic, audience, pain point, and contrarian angle.
2. Open YouTube search URLs sorted by Popularity when possible, for example: `https://www.youtube.com/results?search_query=<keyword>&sp=CAM%253D`.
3. Inspect visible results and capture useful title/thumbnail patterns plus visible signals such as views and age.
4. Keep up to 10 usable videos/posts across relevant searches.
5. Analyze repeated words, hook structures, audience labels, anxiety/benefit/risk phrases, and outdated or compliance-risk phrases to avoid.
6. Generate the issue title and self-contained cover title from verified patterns plus the current script's actual content.

If YouTube blocks access, returns irrelevant results, or reliable signals are unavailable, state the limitation, use the local title rules and accumulated word bank, and still complete the publish workflow.

## English Title Rules

Follow the user's title system, adapted for English finance content:

- First extract theme, audience, pain point, misconception, and compliance risks.
- If no fresh platform samples are provided, rely on the local rule files, historical word bank, and script terms; do not pretend there is fresh external data.
- Avoid unsafe financial claims:
  - Do not use `guaranteed`, `risk-free`, `best strategy`, `always`, `must buy`, `secret method`, `double your money`, or absolute tax/investment conclusions.
  - Prefer `may`, `can`, `could`, `common approach`, `look at whether it fits`, `not the only factor`.
- Make the title and cover title educational, not product-sales copy.
- English cover title must be clear without a cover subtitle. Do not rely on a vague slogan alone.

## English Cover Title Rule

Because English posts normally do not use a cover subtitle, make `封面标题` self-contained:

- Include core content keywords from the script, such as `TFSA`, `RRSP`, `US ETFs`, `Non-Reg`, `Insurance Policy`, `CRA`, `Tax Planning`, `Borrow to Invest`, or `Retirement`.
- Prefer clear meaning over ultra-short punchlines.
- Good examples:
  - `US ETFs: TFSA, RRSP or Non-Reg?`
  - `TFSA vs RRSP for US ETFs`
  - `Don't Cancel Your Life Insurance Yet`
  - `Compound Interest Needs Tax Planning`
  - `Borrowing to Invest: Know the Risk`
- Avoid vague standalone cover titles unless the user explicitly asks for a curiosity-only cover.

## Accumulated English Viral Word Bank

Use the same finance-oriented ingredients as `wfs-marketing-pb-en`. Keep titles truthful, educational, and compliance-safe.

### Leverage, Borrowing to Invest, Wealth Building

- `Borrow to Invest`
- `Leverage Investing`
- `Investment Loan`
- `Good Debt vs Bad Debt`
- `How the Wealthy Use Debt`
- `Build Wealth Faster`
- `Compound on a Bigger Base`
- `Tax-Deductible Interest`
- `Inflation Quietly Eats Cash`
- `Cash Feels Safe`
- `The Safe Choice May Not Be Safe`
- `Don't YOLO Leverage`
- `Leverage Cuts Both Ways`
- `Borrowing to Invest in Canada`
- `Wealth Gap Over 20 Years`
- `Saving vs Investing`
- `The Math Behind Leverage`

### RRSP, Tax Residency, Leaving Canada

- `Retiring Outside Canada`
- `Leaving Canada?`
- `How the CRA Knows if You Left Canada`
- `Tax Residency Status`
- `Non-Resident Withholding Tax`
- `183-Day Rule`
- `Residential Ties`
- `Not Your Passport`
- `RRSP Is Tax Deferred, Not Tax Free`

Use with caution:

- Avoid implying leverage, tax planning, or investing is guaranteed, risk-free, or suitable for everyone.
- Prefer `may`, `could`, `the math`, `before you borrow`, `not for everyone`, `risk matters`, `what CRA checks`, and `tax residency matters`.
- Avoid `guaranteed wealth`, `free money`, `always borrow`, `secret rich strategy`, `double your money`, `never pay tax`, and `zero taxes`.

## English Description Style

The `描述` goes into `备注(内部使用,不发到平台)`.

Write a hook, not a simple summary:

- Paragraph 1: start with the exact question/fear the audience already has.
- Paragraph 2: introduce the counterintuitive twist without giving away everything.
- Paragraph 3: explain why the viewer should watch to the end.
- Final line: include `Source: <original path>` when a source file path is provided.

## Preferred English Tag Pool

Choose a relevant subset from this pool based on script content. Do not include all tags blindly.

```text
#FinancialPlanning
#CanadaInsurance
#LifeInsurance
#CanadianTax
#InvestinCanada
#PersonalFinance
#CanadianInvestment
#Canadianbusiness
#investment
#Investing
#Business
#Canadainvesting
#Canadiantaxplanning
#TFSA
#RRSP
#FHSA
#CRA
#compoundinterest
#taxshelteredinvesting
#financialplanningCanada
#retirementplanningCanada
#nonregisteredaccount
#Canadianinvestors
#wealthbuilding
#taxefficientinvesting
#T4employee
#corporateaccount
#CDA
#investmentstrategy
#personalfinanceCanada
```

Selection guidance:

- ETF/account/tax-efficient investing scripts: use `#Canadainvesting`, `#CanadianInvestment`, `#TFSA`, `#RRSP`, `#nonregisteredaccount`, `#taxefficientinvesting`, `#Canadianinvestors`, `#compoundinterest`, `#taxshelteredinvesting`, `#investmentstrategy`, `#personalfinanceCanada`, `#FinancialPlanning`, `#Investing`, `#wealthbuilding`.
- Insurance scripts: use `#CanadaInsurance`, `#LifeInsurance`, `#FinancialPlanning`, `#PersonalFinance`, `#personalfinanceCanada`.
- Tax/CRA/corporation scripts: use `#CanadianTax`, `#Canadiantaxplanning`, `#CRA`, `#T4employee`, `#corporateaccount`, `#CDA`, `#Canadianbusiness`, `#Business`.

## Script Formatting Rule

For `主内容 / 口播稿`, make the English transcript readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original word, including transcription mistakes, filler phrases, repeated sentences, and awkward phrasing.
- Add punctuation and paragraph breaks.
- Merge line breaks into readable sentence groups.
- Keep the original casing unless adding punctuation requires a natural sentence boundary; do not rewrite words.

Do not:

- Correct transcription errors.
- Rewrite, polish, paraphrase, delete, or add words.
- Summarize the script in the main content field.

## Publishing Procedure

Use an authenticated browser session for `https://marketing.wallacewang.ca/publish`.

1. Open the publish page if it is not already open.
2. If logged out, ask the user to log in.
3. Click the `知识切片` tab.
4. Check existing issues for duplicate source path, same script number, or same title.
5. If an issue exists, click `编辑标题/备注` and update fields that are missing or below this skill's standard.
6. If no issue exists, click `+ 新建一期` and fill:
   - `IP` = `知识切片`
   - `标题(平台帖子/视频标题)` = generated English title
   - `封面标题` = generated self-contained English cover title
   - `封面副标题` = blank unless explicitly requested
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = chosen English finance tags
   - `主内容 / 口播稿` = formatted English script
   - `备注(内部使用,不发到平台)` = hook-style English description and source path
7. Leave platform defaults alone unless the user asks otherwise.
8. Save/create and verify the issue appears under `知识切片` with 9 platforms.

## Browser and API Notes

- Prefer the current authenticated browser page when available, because the publish API is protected by login cookies.
- Do not use server SSH or database edits unless the user explicitly asks for direct server maintenance.
- Use screenshots or DOM state to verify the selected tab, field placement, and final platform list.

## Final Response

Keep the final response brief. Confirm creation or update and list:

- 标题
- 封面标题
- 标签

Mention that `封面副标题` was left blank for English, the hook description went into remarks, and the formatted script went into `主内容 / 口播稿`.
