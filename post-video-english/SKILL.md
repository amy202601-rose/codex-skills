---
name: post-video-english
description: Schedule English spoken-video posts from Wallace marketing center content to YouTube, TikTok, LinkedIn, Instagram, Threads, X, and Facebook. Use when the user provides a local video path plus an article/post title from https://marketing.wallacewang.ca/publish and wants Codex to extract title, tags, and remarks/description, optionally write an English hook-style remark first, then complete browser-based scheduled publishing with minimal user intervention.
---

# Post English Video From Marketing Center

Use this skill for English video publishing workflows where the source content lives in the Wallace marketing center and the output is a scheduled spoken-video post across social platforms.

## Inputs

- Local video path.
- Marketing center article title.
- Publishing account/tab, usually `wallacewang.ca` for English posts unless the user says otherwise.
- Schedule date and time.
- Target platforms and browser mapping.

## Hard rules

- Never click immediate `Post`, `Share`, `Publish`, or equivalent if the user requested scheduling.
- Never trim, crop, shorten, or substitute the video unless the user explicitly approves.
- Stop and ask the user for login, 2FA, captcha, password, account ownership, payment, or permission prompts.
- If a platform cannot schedule the full video, report it as blocked rather than posting immediately.
- Use the exact requested browser mapping when possible. If a platform scheduler is only available in a different Meta surface, state the reason before using it.

## Marketing center workflow

1. Open `https://marketing.wallacewang.ca/publish`.
2. Select the requested publishing-center tab, usually `wallacewang.ca` for English content.
3. Locate the exact article title.
4. If the user asks for a hook or if `备注` is empty:
   - Read `主内容 / 口播稿`.
   - Write a short, internet-native English hook that creates curiosity rather than summarizing the script.
   - Save it into `备注`.
   - Ask the user to review before platform publishing.
5. Extract:
   - `标题` as the platform title.
   - `标签` as hashtags.
   - `备注` as the description/caption.

## Caption mapping

Use this format for platforms with enough text length:

```text
{title}

{remark}

{hashtags}
```

For X, shorten the caption if needed. Preserve the title, the central hook, and the most important hashtags.

## Platform procedures

### YouTube

- Open YouTube Studio upload in the requested browser.
- Upload the exact video file.
- Set title, description, and hashtags.
- Mark `No, it is not made for kids` unless the user says otherwise.
- Use Visibility -> Schedule.
- Set the exact date/time and click final `Schedule` only after the requested time is visible.
- Record the confirmation message and video link if shown.

### TikTok

- Open TikTok Studio upload.
- Upload the exact video file.
- Paste the full caption.
- Choose scheduled publishing, not immediate publishing.
- Set the exact date and time.
- Wait for copyright/content checks when shown.
- Click final scheduled-publish only after the time is visible.

### LinkedIn

- Start a video post from the logged-in profile or requested page.
- Upload the video and paste the full caption.
- Use the clock/schedule control.
- Set the exact date/time and proceed to the final confirmation.
- Click `Schedule`, then keep the page open if LinkedIn continues uploading in the background.

### Instagram

- Try Meta Business Suite first when scheduling is required.
- If Meta Business Suite says the Instagram account is not connected, try native Instagram web upload only to inspect options.
- Native Instagram web may accept the full video as a Reel but only show `Share` without scheduling.
- If no schedule option is available, leave the draft unposted and report Instagram as blocked by scheduling limitations.
- Do not click `Share` for immediate publishing.

### Threads

- Open Threads in Chrome when requested.
- If prompted, use the already logged-in Instagram account to enter Threads; stop for 2FA/password prompts.
- Compose the full caption and attach the exact video.
- Use the more menu (`...`) and choose the schedule/pre-set publishing time option.
- Set the requested date/time and click the scheduled-post button only after the banner shows the correct scheduled time.

### X

- Open X compose in Safari when requested.
- Use a concise caption if the full caption exceeds the character limit.
- Attach the exact video and wait for a visible thumbnail or media attachment.
- If the upload spins indefinitely or the account rejects the video length, do not schedule a text-only post; report X as blocked by video upload/length handling.
- If media attaches successfully, use the calendar/schedule control and click final `Schedule` only after the requested send time is visible.

### Facebook / Meta Business Suite

- Use Meta Business Suite as the Facebook scheduler.
- Select only the intended Facebook page/account unless the user asks for cross-posting.
- Upload the exact video and paste the full caption.
- If Meta offers Story sharing and the user did not request Story, turn Story sharing off.
- Turn on Schedule and set the exact date/time.
- Click final `Schedule` only after the date/time is visible.
- If Meta says scheduling may take a few moments, report the scheduler submission and note that the Posts tab is the confirmation location.

## Final report

Report each platform as:

- Scheduled successfully, with date/time and link/confirmation if available.
- Submitted to scheduler, with platform wording if confirmation is pending.
- Blocked, with the exact reason and the safest next action.

Keep the final report short and practical.
