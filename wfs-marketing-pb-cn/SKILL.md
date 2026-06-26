---
name: wfs-marketing-pb-cn
description: Convert a Chinese Wallace Wang finance oral script into publish-ready Chinese marketing fields, format the script for readability without changing any words, and write the issue into the WWFS Marketing publish center under "加拿大Wallace". Use when the user provides a口播稿/script file or text and says "写入加拿大Wallace", "发布到加拿大Wallace", "放到发布中心", "新建一期", or asks to create title/cover/subtitle/tags/description and submit it to marketing.wallacewang.ca/publish.
---

# WFS Marketing PB CN

Use this skill to turn a Chinese Wallace Wang oral script into a new `加拿大Wallace` issue in the WWFS Marketing publish center.

## Inputs

- Oral script: usually a `.txt` file path or pasted Chinese口播稿.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If either file is missing, state it briefly and use the latest available title-system rules from context.
- Destination phrase: when the user says `写入加拿大Wallace`, create an issue for the `加拿大Wallace` IP.

## Core Workflow

1. Read the two title rule files and the口播稿 with explicit UTF-8.
2. Generate:
   - `标题`
   - `封面标题`
   - `封面副标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
3. Open `https://marketing.wallacewang.ca/publish` in the user's desktop Google Chrome session when the user requests it.
4. Select the `加拿大Wallace` IP tab, click `+ 新建一期`, fill fields, and click `创建本期`.
5. Verify the created issue appears at the top of the `加拿大Wallace` list.

## Title Generation Rules

Always follow the user's title system:

- First extract the script's theme, audience, pain point, misconception, and compliance risks.
- If no fresh platform爆款 samples are provided, state internally/briefly that the run lacks new platform samples and relies on the local rule files, historical word bank, and the script's own terms.
- Avoid unsafe financial claims:
  - Do not use `稳赚`, `保证省税`, `闭眼买`, `必买`, `内部方法`, `快上车`, `最佳方案`, or absolute tax/investment conclusions.
  - Prefer `可能`, `先看是否适合自己`, `常见思路`, `看懂逻辑`, `不一定是重点`.
- Prefer educational, risk-reminder, misconception-correction language.
- Keep cover title short, generally 6-12 Chinese characters.
- Make the description a hook, not a summary. It should create curiosity and encourage watching the full video.

## Description Style

The `描述` goes into the form's `备注(内部使用,不发到平台)` field.

Write 2-4 short paragraphs:

- Paragraph 1: open with the audience's concrete question or fear.
- Paragraph 2: tease the counterintuitive point without giving away the whole answer.
- Paragraph 3: explain why watching the whole口播 matters.

Example shape:

```text
很多人在加拿大买美股ETF，第一反应就是问：放TFSA还是RRSP？更怕那15%的预扣税。

但这条视频真正要讲的，不是一个简单的账户答案，而是你一开始可能就把重点看偏了：15%扣的到底是哪一部分？TFSA最宝贵的位置该留给什么资产？

如果你自己管理投资账户，这条先看完，再决定ETF怎么摆。
```

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

- 投资/账户/复利/税务主题：优先考虑 `#加拿大投资`, `#加拿大理财`, `#复利`, `#避税复利`, `#加拿大避税`, `#加拿大合理避税`.
- TFSA/RRSP/FHSA/RESP/教育金主题：根据稿件具体账户选择 `#FHSA`, `#RESP`, `#加拿大教育基金`, `#加拿大理财`.
- 养老金/退休主题：优先考虑 `#加拿大养老金`, `#加拿大理财`, `#复利`.
- 开公司/创业/公司理财主题：优先考虑 `#加拿大开公司`, `#创业`, `#加拿大创业`, `#加拿大公司理财`.
- 保险/资产传承/信托主题：优先考虑 `#加拿大保险`, `#加拿大资产传承`, `#加拿大信托`, `#加拿大理财顾问`.
- 移民身份或新移民场景明显时，加入 `#移民`.

## Script Formatting Rule

For `主内容 / 口播稿`, make the script readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original Chinese word and filler word, including `啊`, `呃`, `哈`, `呢`.
- Add Chinese punctuation and paragraph breaks.
- Merge line breaks into natural sentences.
- Use only the Chinese口播 portion unless the user explicitly asks to include the English machine translation.

Do not:

- Rewrite, polish, paraphrase, delete, or add words.
- Convert `RSP` to `RRSP` unless the original line already says `RRSP`.
- Remove filler words.
- Summarize the script in the main content field.

## Desktop Chrome Publishing Procedure

Prefer desktop Google Chrome when the user says to use it.

1. Open the publish URL in Chrome:

```powershell
Start-Process 'chrome.exe' 'https://marketing.wallacewang.ca/publish'
```

2. Use a screenshot to inspect the page. If logged out, ask the user to log in in Chrome.
3. Click the `加拿大Wallace` tab if it is not selected.
4. Click `+ 新建一期`.
5. Fill:
   - `标题(平台帖子/视频标题)` = generated title
   - `封面标题` = generated cover title
   - `封面副标题` = generated cover subtitle
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = generated tags
   - `主内容 / 口播稿` = formatted script
   - `备注(内部使用,不发到平台)` = hook-style description
6. Leave platform defaults alone unless the user asks otherwise. If all platforms are selected by default, keep them.
7. Click `创建本期`.
8. Verify the new issue appears at the top and has `创建于 刚刚`.

## Desktop Interaction Notes

When using desktop Chrome instead of the in-app browser:

- Use screenshots to verify state before submitting.
- Use clipboard paste for long fields to avoid typing errors.
- After filling, inspect a screenshot to ensure main content and remarks were not swapped.
- If a click or paste misses, do not submit; correct the field first.

## Final Response

Keep the final response brief. Confirm creation and list the exact fields used:

- 标题
- 封面标题
- 封面副标题
- 标签

Mention that the description went into remarks and the formatted script went into `主内容 / 口播稿`.
