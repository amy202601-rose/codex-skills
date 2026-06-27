---
name: wfs-marketing-pb-cognition-cn
description: Convert a Chinese Wallace Wang cognition/business oral script into publish-ready Chinese marketing fields, format the script for readability without changing any words, and write the issue into the WWFS Marketing publish center under "Wallace认知圈". Use when the user provides a 中文认知圈口播稿/script file or text and says "中文认知圈视频写入Wallace认知圈", "写入Wallace认知圈", "发布到Wallace认知圈", "放到发布中心", "新建一期", or asks to create title/cover/subtitle/tags/description for marketing.wallacewang.ca/publish.
---

# WFS Marketing PB Cognition CN

Use this skill to turn a Chinese Wallace Wang cognition/business oral script into a new `Wallace认知圈` issue in the WWFS Marketing publish center.

## Inputs

- Oral script: usually a `.txt` file path or pasted Chinese口播稿. Common source folder: `E:\00Wallace\07 视频日记\01中文认知圈\...`.
- Title rules:
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-data-analysis-rule.md`.
  - Prefer `C:\Users\admin\Documents\New project 2\ai-title-system-v1.md`.
  - If either file is missing, state it briefly and use the latest available title-system rules from context.
- Destination phrase: when the user says `中文认知圈视频写入Wallace认知圈` or `写入Wallace认知圈`, create or update an issue for the `Wallace认知圈` IP.

## Core Workflow

1. Read the two title rule files and the口播稿 with explicit UTF-8.
2. Use only the Chinese口播 portion unless the user explicitly asks to include English. If the file has machine English after the Chinese script, split before the English translation.
3. Generate:
   - `标题`
   - `封面标题`
   - `封面副标题`
   - `标签`
   - `描述`
   - formatted `主内容 / 口播稿`
4. Open or use `https://marketing.wallacewang.ca/publish` in an authenticated browser session.
5. Select the `Wallace认知圈` IP tab.
6. Before creating, check for an existing issue with the same source file path, same script number, or same title. If it exists, update missing/weak fields instead of duplicating it.
7. If no issue exists, click `+ 新建一期`, fill fields, and click `创建本期`.
8. Verify the issue appears under `Wallace认知圈` and has the Wallace认知圈 platform set: 小红书, 抖音, 视频号, TikTok, X, Instagram, FaceBook, LinkedIn, YouTube.

## Title Generation Rules

Always follow the user's title system:

- First extract the script's theme, audience, pain point, misconception, and risk boundaries.
- If no fresh platform爆款 samples are provided or accessible, state briefly that this run lacks fresh sample evidence and relies on the local title rules, historical word bank, and the script's own terms.
- For `Wallace认知圈`, prefer business cognition, sales cognition, entrepreneurship, work reflection, value perception, client psychology, and personal growth angles.
- Keep the title truthful, human, and educational. Do not overpromise, exaggerate, or turn the script into financial advice if the script is not about finance.
- Keep cover title short, generally 6-12 Chinese characters.
- Make the description a hook, not a summary. It should create curiosity and encourage watching the full video.

## Xiaohongshu Trend Mining Before Title Generation

Before generating titles, run a Xiaohongshu trend-mining step when network/browser access is available and the task is not urgent:

1. Extract 3-6 search keywords from the script, including the cognition theme, audience, pain point, and surprising angle. Examples: `客户嫌贵`, `销售认知`, `创业认知`, `客户价值`, `价格异议`, `做生意逻辑`.
2. Search Xiaohongshu with these keywords. Prefer current posts in the same topic or adjacent business/cognition topics.
3. Rank visible candidate posts by public likes and comments.
4. Keep up to 10 usable posts and record cover title, post title, visible likes/comments, and relevance.
5. Extract high-frequency words, hook structures, audience labels, anxiety/benefit/risk phrases, and outdated phrases to avoid.
6. Use the verified patterns plus the current script's actual content to generate title, cover title, and cover subtitle.

If Xiaohongshu is blocked, logged out, rate-limited, or interaction counts are unavailable, say trend-mining evidence is unavailable for this run and still complete the publish workflow.

## Accumulated Cognition Word Bank

Use these as reusable ingredients, not mandatory words. Keep titles truthful and grounded in the script.

### Business, Sales, Client Value

- `客户嫌贵`
- `不是价格问题`
- `真正问题不是价格`
- `客户没看见价值`
- `别急着降价`
- `销售卡点`
- `价值感`
- `做生意的人`
- `创业认知`
- `生意逻辑`
- `人性没变`
- `先别解释价格`
- `客户为什么不买`
- `价格异议`
- `开公司的人要懂`
- `做服务的人要懂`

### Personal Cognition, Work, Growth

- `真正卡住你的`
- `很多人想反了`
- `这件事很现实`
- `别只看表面`
- `底层逻辑`
- `认知差距`
- `普通人容易忽略`
- `以前我也想错了`
- `看懂就不慌`
- `一句话点醒`

Avoid empty clickbait such as `震惊`, `90%的人都错了`, `不看后悔`, `财富密码`, `一招搞定`, unless the user explicitly asks for a harder marketing style.

## Preferred Chinese Tag Pool

Choose a relevant subset. Do not include all tags blindly.

```text
#销售
#创业
#客户价值
#价格
#认知
#商业认知
#创业认知
#做生意
#客户心理
#个人成长
#工作思考
#加拿大创业
#加拿大生活
#开公司
#管理
#沟通
#职场
```

Selection guidance:

- 销售/客户异议/价格主题：优先 `#销售`, `#客户价值`, `#价格`, `#客户心理`, `#商业认知`.
- 创业/开公司/做生意主题：优先 `#创业`, `#创业认知`, `#做生意`, `#开公司`, `#加拿大创业`.
- 个人反思/工作方法主题：优先 `#认知`, `#个人成长`, `#工作思考`, `#职场`.
- 加拿大场景明显时，可加入 `#加拿大创业` 或 `#加拿大生活`.

## Description Style

The `描述` goes into `备注(内部使用,不发到平台)`.

Write 2-4 short paragraphs:

- Paragraph 1: open with the audience's concrete question, fear, or familiar stuck point.
- Paragraph 2: tease the counterintuitive point without giving away the whole answer.
- Paragraph 3: explain why watching the full口播 matters.
- Final line: include `来源：<original path>` when a source file path is provided.

Example shape:

```text
客户一说“太贵了”，很多做生意的人第一反应就是解释、降价，甚至自己先心虚。

但这条视频真正要讲的，不是怎么把价格说低，而是客户为什么还没有看见这个东西“值”。

如果你在中国或加拿大开公司、做销售、做服务，这条值得看完。

来源：E:\00Wallace\07 视频日记\01中文认知圈\1197\1197.txt
```

## Script Formatting Rule

For `主内容 / 口播稿`, make the script readable with paragraphs and punctuation, but do not change any wording.

Do:

- Preserve every original Chinese word and filler word, including `啊`, `呃`, `哈`, `呢`.
- Preserve embedded English phrases that appear inside the Chinese口播, such as `financial planning` or quoted customer lines.
- Add Chinese punctuation and paragraph breaks.
- Merge raw line breaks into natural sentences.
- Use only the Chinese口播 portion unless the user explicitly asks to include the English machine translation.

Do not:

- Rewrite, polish, paraphrase, delete, or add words.
- Remove filler words.
- Summarize the script in the main content field.
- Change the business/cognition angle into a finance topic unless the script itself is about finance.

## Publishing Procedure

Use an authenticated browser session for `https://marketing.wallacewang.ca/publish`.

1. Open the publish page if it is not already open.
2. If logged out, ask the user to log in.
3. Click the `Wallace认知圈` tab.
4. Check existing issues for duplicate source path, same script number, or same title.
5. If an issue exists, click `编辑标题/备注` and update fields that are missing or below this skill's standard.
6. If no issue exists, click `+ 新建一期` and fill:
   - `IP` = `Wallace认知圈`
   - `标题(平台帖子/视频标题)` = generated title
   - `封面标题` = generated cover title
   - `封面副标题` = generated cover subtitle
   - `标签(用 逗号 / 空格 分隔,自动去 #)` = generated tags
   - `主内容 / 口播稿` = formatted Chinese script
   - `备注(内部使用,不发到平台)` = hook-style description and source path
7. Leave platform defaults alone unless the user asks otherwise.
8. Save/create and verify the issue appears under `Wallace认知圈` with 9 platforms.

## Browser and API Notes

- Prefer the current authenticated browser page when available, because the publish API is protected by login cookies.
- Do not use server SSH or database edits unless the user explicitly asks for direct server maintenance.
- Use screenshots or DOM state to verify the selected tab, field placement, and final platform list.
- If a click or paste misses, do not submit; correct the field first.

## Final Response

Keep the final response brief. Confirm creation or update and list:

- 标题
- 封面标题
- 封面副标题
- 标签

Mention that the description went into remarks and the formatted Chinese script went into `主内容 / 口播稿`.
