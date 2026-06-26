---
name: post-video-en
description: Publish or schedule a Chinese spoken-video post from Wallace marketing center content to YouTube, TikTok, Instagram, LinkedIn, Facebook, and X. Use when the user gives a local video path, target schedule time, and an article/post title from https://marketing.wallacewang.ca/publish and wants Codex to switch to Wallace Chinese platform accounts, extract title, tags, and the already-written remarks/description, then complete browser-based posting with minimal user intervention.
---

# Post Video From Marketing Center

Use this skill to turn a marketing-center article into a scheduled multi-platform video post.

## Required inputs

- Local video file path.
- Marketing center article/post title.
- Target schedule date and time. If the user does not specify a date/time, ask before submitting any platform.
- Target platforms and browser mapping if the user provides one.
- The marketing center `备注` field is expected to already contain the platform description.

## Core rule

Never click an immediate publish/share/post button when the user requested scheduling. If a platform cannot schedule the full video at the requested time, stop on that platform and report the blocker instead of publishing immediately or trimming the video.

Do not generate or rewrite the platform description from `主内容 / 口播稿` by default. Use the existing `备注` field exactly as the description. Only write or rewrite `备注` if the user explicitly asks for description/hook creation in the current request. If `备注` is empty and the user did not ask for writing a description, stop and ask the user to fill or approve a description before publishing.

## Default Chinese platform accounts

When the user asks to publish a Chinese video and does not provide different account links, prepare and use these Chinese platform accounts before posting:

- YouTube: `https://www.youtube.com/@%E5%8A%A0%E6%8B%BF%E5%A4%A7Wallace` (`加拿大Wallace`)
- TikTok: `https://www.tiktok.com/@wallacecanada`
- Instagram: `https://www.instagram.com/wallace_financial`
- Facebook: Meta Business Suite page/account at `https://business.facebook.com/latest/content_calendar?global_scope_id=422671744077867&business_id=422671744077867&page_id=1046044488600459&asset_id=1046044488600459`
- LinkedIn: `https://www.linkedin.com/in/%E7%AB%8B%E6%98%8A-%E7%8E%8B-71251a418/`
- X: `https://x.com/wallacewang_ca`
- Threads: do not publish Chinese-platform posts to Threads unless the user explicitly requests it.

Default browser mapping for Chinese posts:

- Open and use Google Chrome for YouTube, TikTok, Instagram, Facebook/Meta Business Suite, and LinkedIn.
- Open and use Safari for X.

Before publishing, switch/prepare platform pages by opening the account URLs above in the requested browser. If old English-account tabs are open, do not close them unless necessary; instead make the Chinese account tab active before composing. For X, ensure Safari's active X tab is `@wallacewang_ca`, not `@Wallace960809`.

## Marketing center workflow

1. Open `https://marketing.wallacewang.ca/publish` in the requested browser.
2. Select the requested account/project, usually `加拿大Wallace` unless the user names another one.
3. Search or locate the article by exact title.
4. Open the article and extract:
   - `标题` as the platform title.
   - `标签` as hashtags.
   - `备注` as the platform description.
5. If `备注` is empty, stop and ask the user to fill or approve the description before publishing.
6. Only if the user explicitly asks for a new hook/description in the current request:
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

- Use the user's specified browsers. If not specified for Chinese posts, use the default Chinese browser mapping above.
- Always use Meta Business Suite at `https://business.facebook.com/` for Instagram and Facebook posting or scheduling unless the user explicitly asks for another route or Meta Business Suite is unavailable.
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

1. Use Meta Business Suite at `https://business.facebook.com/` by default for all Facebook posting and scheduling.
2. Select only the intended Facebook page/account.
3. Upload the video and paste title, description, and hashtags.
4. Use the Schedule section and set the exact date/time.
5. Click final Schedule only after the requested time is shown.
6. If Meta says scheduling may take a few moments, note that the post was submitted and that the Posts tab is the confirmation location.

### Instagram

1. For Facebook/Instagram cross-posting through Meta Business Suite, use Meta Business Suite when it can schedule the requested Instagram post without altering the video.
2. For Chinese Instagram posts that must be released at a scheduled time and native Instagram web has no schedule control, create a Codex heartbeat automation for the requested local publish time instead of posting early. The automation must perform the immediate Instagram native web upload at trigger time.
3. Use the Chinese Instagram account `https://www.instagram.com/wallace_financial` unless the user provides another account.
4. In the heartbeat automation prompt, include the exact video path, title, description, hashtags, target account/page, and these native Instagram steps:
   - Open or use the logged-in Instagram page in Chrome.
   - Click create/upload video.
   - Select the exact supplied video file.
   - At the crop step, click the crop icon in the lower-left corner of the pop-up.
   - Set the aspect ratio to `9:16`.
   - Click the top-right continue button.
   - Click the top-right continue button again.
   - Paste the caption as title, blank line, description, blank line, hashtags.
   - Click share/publish only when the automation is running at the requested publish time.
   - Stop for login, 2FA, captcha, password, security, or account-selection prompts.
5. When creating the heartbeat automation, convert the requested Calgary/Mountain local time carefully if the automation system expects UTC. Always check the machine time with `date '+%Y-%m-%d %H:%M:%S %Z %z'` before deciding whether it is time to post.
6. After the heartbeat automation successfully publishes, delete the one-time automation to prevent repeat posting.
7. Never click `Share` for immediate publishing before the requested scheduled time.

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
