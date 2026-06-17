---
name: main-site-insights-updater
description: Convert Wallace Wang oral-script drafts into official bilingual English/Chinese Insights articles for wallacewang.ca, generate a 16:9 cover image, publish through the website admin, and verify the live article. Use when the user asks to update the main website, publish an Insights article, or gives an oral/short-video script for Wallace Wang's financial website.
---

# Main Site Insights Updater

Use this skill to turn a user-provided oral script into a polished bilingual Insights article on `https://www.wallacewang.ca/`, with a matching 16:9 cover image and live publication verification.

## Inputs

Accept either:

- A pasted oral-script draft.
- A local `.txt` file path.
- A referenced image to use as the final cover.
- Admin credentials provided in the current user request or current conversation.

Do not store credentials in the skill. Do not repeat passwords in final responses.

## Core Workflow

1. Read the oral script.
   - Use `Get-Content -LiteralPath ... -Raw -Encoding UTF8` for local text files.
   - If the file path is outside the workspace but readable, read it directly.
   - Preserve the user's intended topic, but remove filler, repetition, and loose speech patterns.

2. Rewrite into an official website article.
   - English must read like native professional financial writing.
   - Chinese must be natural, formal, and not a rigid translation.
   - Use a suitable tone for Wallace Wang Financial Services: official, compliant, clear, educational, and advisory.
   - Correct grammar, terminology, and awkward phrasing.
   - Remove casual calls to action such as "link in bio", "we should talk", "subscribe", and social-platform language.
   - Add an educational disclaimer when the topic touches investment, tax, insurance, lending, or legal matters.
   - Avoid guaranteed returns, aggressive tax avoidance framing, fear-based claims, or product-specific advice.

3. Add metadata.
   - Provide:
     - English title
     - Chinese title
     - English description/excerpt
     - Chinese description/excerpt
     - English tags
     - Chinese tags
     - slug in lowercase hyphen-case
     - category
     - read time in English and Chinese
   - Keep titles attractive but professional.
   - Prefer categories already used by the site such as `Tax Planning`, `Financial Planning`, `Investment Strategy`, `Wealth Structuring`, or `Capital Protection`.

4. Verify current facts when needed.
   - Browse or otherwise verify temporally sensitive facts, especially:
     - CRA limits and thresholds
     - TFSA/RRSP/FHSA rules
     - tax rates or contribution limits
     - insurance or lending rules
   - Prefer official sources such as `canada.ca`, CRA pages, or primary government references.
   - Paraphrase sources and include source links in the article only when useful or requested.

5. Generate a 16:9 cover image.
   - Use the `imagegen` skill / built-in `image_gen` tool for new cover images.
   - Style: premium financial advisory website hero image, formal, clean, Canadian context, no readable text unless explicitly required.
   - Avoid: government logos, real company logos, guaranteed return imagery, cash piles, crypto, QR codes, aggressive sales style, watermarks, misspelled text.
   - Save the final project-bound image under:
     - the current Wallace Wang website workspace under `insights-update`
   - If the user supplies a specific image and says "use this one", treat that as authoritative. Upload that image and update only `coverImage` unless they ask for content changes.
   - Do not trust "latest generated image" by timestamp alone. After generating or selecting an image, immediately inspect the exact file with `view_image` before uploading.
   - The cover must pass a visual relevance check:
     - It clearly matches the article topic.
     - It is visually distinct from the previous article's cover unless the user explicitly asks to reuse it.
     - It does not show the wrong concept, such as a risk checklist cover for an institutional portfolio article.
     - It has no unwanted readable text, logos, watermarks, or obvious image-generation errors.
   - If the visual check fails, do not upload it. Regenerate once with stronger negative constraints, or create/select a corrected local image and inspect it again.
   - If multiple plausible images exist or the user says the image is wrong, ask the user to provide or choose the exact image. Treat an attached/clipboard image as the source of truth.

6. Save local backups.
   - Create or reuse the `insights-update` directory in the current Wallace Wang website workspace.
   - Save:
     - `<slug>-en.md`
     - `<slug>-zh.md`
     - `<slug>-cover.png`
   - Use YAML frontmatter matching the admin fields:
     - `title`, `description`, `slug`, `category`, `tags`, `readTime`, `coverImage`, `status`.

7. Publish through the website admin API.
   - Admin URL: `https://www.wallacewang.ca/admin`.
   - The site uses tRPC at `/api/trpc`.
   - Login endpoint:
     - `POST https://www.wallacewang.ca/api/trpc/adminAuth.login`
     - Body shape:
       ```json
       {"json":{"email":"<email>","password":"<password>"}}
       ```
     - Use a `WebRequestSession` and `credentials/include` equivalent via cookies.
   - Upload image endpoint:
     - `POST https://www.wallacewang.ca/api/trpc/cms.uploadImage`
     - Body shape:
       ```json
       {"json":{"filename":"<file.png>","contentType":"image/png","dataBase64":"<base64>"}}
       ```
     - Capture returned `url`, such as `/uploads/article-images/...png`.
   - Create article endpoint:
     - `POST https://www.wallacewang.ca/api/trpc/cms.createArticle`
     - Body shape:
       ```json
       {
         "json": {
           "slug": "...",
           "titleEn": "...",
           "titleZh": "...",
           "excerptEn": "...",
           "excerptZh": "...",
           "contentEn": "...",
           "contentZh": "...",
           "category": "...",
           "tags": "...",
           "tagsZh": "...",
           "readTimeEn": "...",
           "readTimeZh": "...",
           "status": "published",
           "coverImage": "/uploads/article-images/..."
         }
       }
       ```
   - Use UTF-8 bytes when sending article JSON from PowerShell:
     - `-ContentType 'application/json; charset=utf-8'`
     - `-Body ([System.Text.Encoding]::UTF8.GetBytes($payload))`
   - Upload only the visually approved cover image. Never upload a cover that was not inspected in the current task.

8. Updating an existing article.
   - Fetch by slug with:
     - `GET https://www.wallacewang.ca/api/trpc/articles.getBySlug?input=<urlencoded {"json":{"slug":"..."}}>`
   - Update via:
     - `POST https://www.wallacewang.ca/api/trpc/cms.updateArticle`
   - Include the article `id` and all existing fields that should remain unchanged.
   - For cover-only replacement, preserve all content fields and change only `coverImage`.

9. Validate after publishing.
   - Verify article page returns `200`:
     - `https://www.wallacewang.ca/insights/<slug>`
   - Verify article API returns the new record:
     - `articles.getBySlug`
   - Verify Chinese title/body are not mojibake by reading API response as UTF-8.
   - Verify image URL returns `200`, `image/png` or expected image type, and nonzero length.
   - Verify the saved `coverImage` path from the article API matches the approved image uploaded in this task.
   - When practical, open or inspect the final local image used for upload and confirm it is the same visual concept requested by the article.
   - If the front-end HTML does not contain article text, do not treat that as failure; it is a React single-page app.

## PowerShell Patterns

Use these patterns when publishing from the local Windows environment.

Cover file selection rule:

- Avoid blindly running `Get-ChildItem ... | Sort-Object LastWriteTime -Descending | Select-Object -First 1` and uploading that file.
- If using generated-image output, first identify the exact candidate, copy it to a slug-specific filename, inspect that copied file with `view_image`, and only then upload it.
- Prefer deterministic names such as `<slug>-cover-final.png` or `<slug>-cover-corrected.png` for the image that passed visual review.

Login:

```powershell
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$payload = @{ json = @{ email = $email; password = $password } } | ConvertTo-Json -Depth 8 -Compress
Invoke-WebRequest -Uri "https://www.wallacewang.ca/api/trpc/adminAuth.login" `
  -Method Post -ContentType "application/json" -Body $payload `
  -WebSession $session -UseBasicParsing
```

Upload image:

```powershell
$imageB64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($imagePath))
$uploadPayload = @{ json = @{ filename = $filename; contentType = "image/png"; dataBase64 = $imageB64 } } |
  ConvertTo-Json -Depth 5 -Compress
$upload = Invoke-WebRequest -Uri "https://www.wallacewang.ca/api/trpc/cms.uploadImage" `
  -Method Post -ContentType "application/json" -Body $uploadPayload `
  -WebSession $session -UseBasicParsing
$coverUrl = ($upload.Content | ConvertFrom-Json).result.data.json.url
```

Extract article body from local Markdown backup:

```powershell
function Get-ArticleBody($path) {
  $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  if ($raw -match '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { return $Matches[1].Trim() }
  return $raw.Trim()
}
```

## Final Response

Keep the final response short. Include:

- Live article URL.
- Confirmation that API/article/image/Chinese encoding were verified.
- Local backup paths.
- New cover image URL if a cover was uploaded.

Do not include the password.
