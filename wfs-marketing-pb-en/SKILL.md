---
name: wfs-marketing-pb-en
description: Convert an English Wallace Wang finance oral script into publish-ready English marketing fields, format the script for readability without changing any words, choose English finance tags from the preferred tag pool, and write the issue into the WWFS Marketing publish center under "wallacewang.ca". Use when the user provides an English口播稿/script file or text and says "写入Wallacewang.ca", "写入wallacewang.ca", "publish to wallacewang.ca", "放到wallacewang.ca发布中心", "新建英文一期", or asks to create English title/cover title/tags/description and submit it to marketing.wallacewang.ca/publish.
---

# WFS Marketing PB EN

Use this skill to turn an English Wallace Wang oral script into a new `wallacewang.ca` issue in the WWFS Marketing publish center.

## Inputs

- English oral script: usually a `.txt` file path or pasted transcript.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If the user says `ai-title-analysis-rule.md`, look for the actual local file first; in this environment it has historically been named `ai-title-data-analysis-rule.md`.
- Destination phrase: when the user says `写入Wallacewang.ca`, create an issue for the `wallacewang.ca` IP.

## Core Workflow

1. Read the title rule files and the oral script with explicit UTF-8.
2. Generate English:
   - `标题`
   - `封面标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
3. Do not generate or use a cover subtitle for English unless the user explicitly asks. Leave `封面副标题` empty.
4. Open `https://marketing.wallacewang.ca/publish` in the user's desktop Google Chrome session.
5. Select the `wallacewang.ca` IP tab, click `+ 新建一期`, fill fields, and click `创建本期`.
6. Verify the created issue appears at the top of the `wallacewang.ca` list.

## English Title Rules

Follow the user's title system, adapted for English:

- First extract theme, audience, pain point, misconception, and compliance risks.
- If no fresh platform samples are provided, rely on the local rule files, historical word bank, and script terms; do not pretend there is fresh external data.
- Avoid unsafe financial claims:
  - Do not use `guaranteed`, `risk-free`, `best strategy`, `always`, `must buy`, `secret method`, `double your money`, or absolute tax/investment conclusions.
  - Prefer `may`, `can`, `could`, `common approach`, `look at whether it fits`, `not the only factor`.
- Make the title and cover title educational, not product-sales copy.
- English cover title must be clear without a cover subtitle. Do not rely on a vague slogan alone.

## English Cover Title Rule

Because English posts normally do not use a cover subtitle, make `封面标题` self-contained:

- Include core content keywords from the script, such as `TFSA`, `RRSP`, `US ETFs`, `Non-Reg`, `Insurance Policy`, `CRA`, `Tax Planning`, etc.
- Prefer clear meaning over ultra-short punchlines.
- Good examples:
  - `US ETFs: TFSA, RRSP or Non-Reg?`
  - `TFSA vs RRSP for US ETFs`
  - `Don't Cancel Your Life Insurance Yet`
  - `Compound Interest Needs Tax Planning`
- Avoid vague standalone cover titles such as `Stop Fearing 15%` unless paired with a clarifying subtitle, which English posts usually will not have.

## English Description Style

The `描述` goes into `备注(内部使用,不发到平台)`.

Write a hook, not a simple summary:

- Paragraph 1: start with the exact question/fear the audience already has.
- Paragraph 2: introduce the counterintuitive twist without giving away everything.
- Paragraph 3: explain why the viewer should watch to the end.

Example shape:

```text
Most people ask the same question when they buy US ETFs in Canada: TFSA or RRSP?

But what if that question is already aiming at the wrong target? The 15% withholding tax sounds scary, but it may not be the thing that actually decides whether your account setup works.

This video starts with the account placement debate, then turns into the bigger point: what belongs in your precious TFSA room, what may be fine outside it, and why the real lever may come after the account decision.
```

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

- ETF/account/tax-efficient investing scripts: use tags such as `#Canadainvesting`, `#CanadianInvestment`, `#TFSA`, `#RRSP`, `#nonregisteredaccount`, `#taxefficientinvesting`, `#Canadianinvestors`, `#compoundinterest`, `#taxshelteredinvesting`, `#investmentstrategy`, `#personalfinanceCanada`, `#FinancialPlanning`, `#Investing`, `#wealthbuilding`.
- Insurance scripts: use tags such as `#CanadaInsurance`, `#LifeInsurance`, `#FinancialPlanning`, `#PersonalFinance`, `#personalfinanceCanada`.
- Tax/CRA/corporation scripts: use tags such as `#CanadianTax`, `#Canadiantaxplanning`, `#CRA`, `#T4employee`, `#corporateaccount`, `#CDA`, `#Canadianbusiness`, `#Business`.

## Script Formatting Rule

For `主内容 / 口播稿`, make the English transcript readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original word, including transcription mistakes, filler phrases, repeated sentences, and awkward phrasing.
- Add punctuation and paragraph breaks.
- Merge line breaks into readable sentence groups.
- Keep the original casing unless adding punctuation requires a natural sentence boundary; do not rewrite words.

Do not:

- Correct transcription errors such as `night of tens`, `SMP`, `GAC's`, `broom`, or similar.
- Rewrite, polish, paraphrase, delete, or add words.
- Summarize the script in the main content field.

## Desktop Chrome Publishing Procedure

Prefer the user's desktop Google Chrome session.

1. Open:

```powershell
Start-Process 'chrome.exe' 'https://marketing.wallacewang.ca/publish'
```

2. Use screenshots to confirm the page is logged in. If logged out, ask the user to log in in Chrome.
3. Click the `wallacewang.ca` tab if it is not selected.
4. Click `+ 新建一期`.
5. Fill:
   - `标题(平台帖子/视频标题)` = generated English title
   - `封面标题` = generated self-contained English cover title
   - `封面副标题` = blank
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = chosen English tags
   - `主内容 / 口播稿` = formatted English script
   - `备注(内部使用,不发到平台)` = hook-style English description
6. Leave platform defaults alone unless the user asks otherwise.
7. Click `创建本期`.
8. Verify the new issue appears at the top and has `创建于 刚刚`.

## Desktop Interaction Notes

- Use screenshots to verify state before submitting.
- Use clipboard paste for long fields.
- After filling, inspect a screenshot to ensure main content and remarks were not swapped.
- If editing an existing issue, open `编辑标题/备注`, change only the requested fields, save, and verify the expanded details.

## Final Response

Keep the final response brief. Confirm creation or update and list the exact fields used:

- 标题
- 封面标题
- 标签

Mention that `封面副标题` was left blank for English, the hook description went into remarks, and the formatted script went into `主内容 / 口播稿`.
