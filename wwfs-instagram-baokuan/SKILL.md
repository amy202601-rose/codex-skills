---
name: wwfs-instagram-baokuan
description: Find the most-liked post on the Wallace Wang Instagram channel, extract exact post metadata and transcript, then update the matching English hit-library entry on the WWFS marketing site.
metadata:
  short-description: Instagram爆款查找并同步到WWFS爆款库
---

# WWFS Instagram Baokuan

Use this skill when Wallace asks to start from the Instagram channel `https://www.instagram.com/wallacewang.ca/`, find the most-liked post, collect its exact metadata/transcript, and update the matching item in `https://marketing.wallacewang.ca/hit-library`.

The workflow touches two live services: Instagram and the WWFS marketing site. Treat browsing and editing as separate phases. Reading and verification are okay to do directly; before saving changes on the marketing site, summarize the exact fields to be changed and get explicit user confirmation.

## Required Output

When asked to report the winning Instagram post, provide:

- title/caption
- cover title and cover subtitle, if visible
- publish date
- like count
- comment count
- save count, only if available from the user's own account or existing trusted exports
- canonical link
- exact original spoken transcript

If the user asks to update the marketing site, update the existing matching item instead of creating a duplicate unless the item is genuinely missing.

## Instagram Ranking

Prefer the user's logged-in desktop Chrome session when Instagram data depends on an authenticated account. Use the Chrome browser control skill/tooling for this; do not rely on an anonymous web search result for ranking.

For `wallacewang.ca`, do not assume a previous ranking file is complete. The profile count may change, and Instagram's virtual grid can unload old cards while scrolling. Use this approach:

1. Open `https://www.instagram.com/wallacewang.ca/`.
2. Confirm whether Chrome is logged in. If the profile shows `已关注` / `发消息` and the sidebar profile points to another handle, it is logged in but not as `wallacewang.ca`; this is still enough for public likes/comments, but not owner-only saves/insights.
3. Scroll the profile while accumulating every `/reel/` and `/p/` URL into a set. Do not only read the final DOM after scrolling.
4. Compare the accumulated URL set with any existing local ranking files in `C:\Users\admin\Documents\已发贴爆款报告`, especially `wallacewang_full_like_ranking.json`, and verify coverage. The old file may be incomplete.
5. Open and verify every candidate that could beat the current top item, including new links missing from the old file and the old top-ranked items.
6. Parse likes/comments from Instagram page text and meta description. If current page numbers and older export numbers differ slightly, use current page numbers for "current" metrics and mention the older number only as historical context.

For the known historical top candidate, verify rather than assuming:

- Shortcode: `DRi4bbME-YD`
- Canonical URL: `https://www.instagram.com/wallacewang.ca/reel/DRi4bbME-YD/`
- Caption/title: `Company vs Personal: Who Pays CRA Less? #Calgaryfinancialadvisor #PayLessTax #TaxSmart #CRATips #CanadianBusiness #financialeducation #CanadaFinance`
- Cover title: `How to Legally Pay LESS to CRA`
- Cover subtitle: empty/none visible

## Transcript Source Priority

The transcript must be exact enough to preserve wording, punctuation, numbers, and line breaks where known. Use the strongest available source in this order:

1. Existing verified local workbook/report exports under `C:\Users\admin\Documents\已发贴爆款报告`.
2. Downloaded audio/video plus existing transcription artifacts if the local export is missing or contradicted.
3. A fresh transcription only if no trusted transcript exists; clearly mark it as newly transcribed and verify obvious numeric terms manually.

For `DRi4bbME-YD`, the later Excel export in `outputs\instagram_saves_top20_20260806\instagram_saves_top20_corrected.xlsx.inspect.ndjson` contains the preferred transcript. It is more polished than the early Markdown report and should be used unless the user supplies a better primary source.

## Cover Verification

Do not infer cover text from captions. Open or inspect the downloaded cover image when available. For `DRi4bbME-YD`, inspect:

`C:\Users\admin\Documents\已发贴爆款报告\DRi4bbME-YD_cover.jpg`

The visible cover title is:

`How to Legally Pay LESS to CRA`

There is no separate visible cover subtitle.

## Marketing Site Update

Open `https://marketing.wallacewang.ca/hit-library` in the logged-in Chrome session. The page is usually under `WWFS Marketing` and may show the logged-in staff account, such as `Amy He`.

Steps:

1. Switch to `英文爆款库`.
2. Search by a stable phrase from the title, such as `Company vs Personal`.
3. Open `编辑标题/备注` for the matching item.
4. Preserve existing fields when they are already correct, especially status, selected distribution platforms, notes, save count, and existing transcript.
5. Update only missing or incorrect fields. For the known top post, the important correction is often:
   - `封面标题`: `How to Legally Pay LESS to CRA`
   - `链接`: `https://www.instagram.com/wallacewang.ca/reel/DRi4bbME-YD/`
6. Before clicking `保存修改`, tell the user exactly what will change and ask for confirmation.
7. After saving, reopen the edit dialog and read the fields back to verify the persisted values.

Do not mark items as published, delete items, create new items, change channel settings, or log out unless the user explicitly asks for that action.

## Known DRi4bbME-YD Transcript

Use this only after confirming the target post is `DRi4bbME-YD`.

```text
I always tell people in Canada, you must have your own business. Not because entrepreneurship sounds cool, but because the tax system is literally designed to reward business owners, not employees.

Today I'll prove it to you with two powerful tools: CDA and RDTOH account. Understand these two accounts, and you will realize the same $100K investment return in a company can put more money in your pocket than if you made the same $100K personally.

Under the same risk, same investment, but your money grows 20 to 30% faster. Let me show this to you.

If your company earns $100K capital gain, only half, that's $50,000, is taxable. Now after tax, the company still has $75,000 left.

Here's the magic. The other $50,000 goes into CDA, which means you can take a full $50,000 out of the company completely tax-free. No personal tax, and no corporate tax. CRA gets nothing.

And now, what about the remaining $25,000 you think is stuck inside the company? That's when our RDTOH account comes in.

On the same capital gain, the company gets about $15,166 recorded in our RDTOH account. And that's not an extra tax. It's money waiting to be refunded back to you when you issue taxable dividends.

So when you pay yourself about $40,000 of dividends, CRA will actually refund that $15,166 back to your company. And that means you take out $40,000, but it only costs the company about $25,000.

And in the end, from that same $100K gain, you can legally get around $80,000 into a personal pocket, with an effective tax rate of only about 20%. And that's lower than if you reinvested it personally.

So here's the real lesson. It's not about working harder or even investing better. It's about using the tax system the way business owners do.
```
