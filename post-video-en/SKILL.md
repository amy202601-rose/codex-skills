---
name: post-video-en
description: Publish or schedule a spoken-video post from Wallace marketing center content to YouTube, TikTok, Instagram, LinkedIn, Facebook, and X. Use when the user gives a local video path plus an article/post title from https://marketing.wallacewang.ca/publish and wants Codex to extract title, tags, and remarks/description, optionally write a hook-style remark first, then complete browser-based posting with minimal user intervention.
---

# Post Video From Marketing Center

Use this skill to turn a marketing-center article into a scheduled multi-platform video post.

## Required inputs

- Local video file path.
- Marketing center article/post title.
- Target schedule date and time. If the user does not specify a date/time, ask before submitting any platform.
- Target platforms and browser mapping if the user provides one.

## Core rule

Never click an immediate publish/share/post button when the user requested scheduling. If a platform cannot schedule the full video at the requested time, stop on that platform and report the blocker instead of publishing immediately or trimming the video.

## Marketing center workflow

1. Open `https://marketing.wallacewang.ca/publish` in the requested browser.
2. Select the requested account/project, usually `加拿大Wallace` unless the user names another one.
3. Search or locate the article by exact title.
4. Open the article and extract:
   - `标题` as the platform title.
   - `标签` as hashtags.
   - `备注` as the platform description.
5. If `备注` is empty or the user asks for a hook:
   - Read `主内容 / 口播稿`.
   - Write a short, internet-native hook that creates curiosity rather than summarizing the article.
   - Save it into `备注`.
   - Ask the user to approve before continuing to platform publishing.

## Cross-platform content mapping

- Title: use the marketing center title.
- Description/caption: use the `备注` content, followed by tags when the platform supports long text.
- Hashtags: use the `标签` field exactly unless platform length requires shortening.
- For X, use a concise version if the full description exceeds the character limit. Preserve the title, central hook, and all possible tags.

## Browser and upload procedure

- Use the user's specified browsers. If not specified, use Chrome for YouTube, TikTok, Instagram, and LinkedIn; use Safari for Facebook and X.
- Use the logged-in account already present in the browser.
- Stop and ask the user for login, 2FA, captcha, account selection, payment, or permission prompts that cannot be safely handled.
- Upload the exact video path supplied by the user. Do not substitute another file unless the user approves.

## Platform procedures

### YouTube

1. Open YouTube Studio upload.
2. Upload the video.
3. Replace filename title with the extracted title.
4. Put description plus hashtags in the description box.
5. Select `No, it's not made for kids` unless the user specifies otherwise.
6. Go to visibility and choose schedule.
7. Set the exact requested date/time and confirm the final schedule button.
8. Capture or note the confirmation message and video link if shown.

### TikTok

1. Open TikTok Studio upload.
2. Upload the video.
3. Caption format: title, blank line, description, blank line, hashtags.
4. Choose scheduled publish rather than immediate post.
5. Set the exact requested date and time. TikTok may use separate hour and minute selectors.
6. Click the final scheduled publish button only after the requested time is visible.

### LinkedIn

1. Start a video post from the logged-in profile or page requested by the user.
2. Upload the video.
3. Paste title, description, and hashtags into the post text.
4. Use the clock/schedule control.
5. Set the exact requested date/time and click the final schedule control.
6. Wait for the scheduled-post confirmation toast if the upload continues in the background.

### Facebook / Meta Business Suite

1. Prefer the user's requested browser, but use Meta Business Suite if it is the available scheduler for the selected Facebook page.
2. Select only the intended Facebook page/account.
3. Upload the video and paste title, description, and hashtags.
4. Use the Schedule section and set the exact date/time.
5. Click final Schedule only after the requested time is shown.
6. If Meta says scheduling may take a few moments, note that the post was submitted and that the Posts tab is the confirmation location.

### Instagram

1. Try Meta Business Suite first when scheduling is required.
2. If Meta Business Suite forces trimming, aspect-ratio changes, or a maximum duration that would alter the video, do not accept without user approval.
3. Try native Instagram web upload if Meta rejects the full video.
4. Fill caption with title, description, and hashtags.
5. Inspect advanced settings for a scheduling option.
6. If native Instagram accepts the full video but offers no schedule control, leave it unposted and report that Instagram is prepared but blocked by scheduling limitations.
7. Never click `Share` for immediate publishing when the user requested a scheduled post.

### X

1. Open X compose in Safari or the requested browser.
2. Attach the video first and wait for upload/processing feedback.
3. Use a concise caption if necessary for character limits.
4. Open the schedule/calendar control.
5. Set the exact requested date/time and confirm.
6. Click final `Schedule` only after the composer shows the requested send time.
7. Wait for the confirmation toast such as `Your post will be sent on ...`.

## Reporting

At the end, report each platform as one of:

- Scheduled successfully, with date/time and any link or confirmation shown.
- Submitted to scheduler, with the platform's pending confirmation wording.
- Blocked, with the exact reason and what user decision is needed.

Keep the report brief and practical.
