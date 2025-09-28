# Podummary Utility Scripts

This directory contains utility scripts for managing and maintaining the Podummary platform.

## Main Scripts (Root Directory)

### `generate_blogs.py`

**Purpose**: Generate English blog posts from YouTube videos

**Usage**:

```bash
python3 generate_blogs.py
```

**What it does**:

1. Prompts for YouTube URL
2. Extracts video metadata (title, description, thumbnail)
3. Uses Google Gemini AI to generate blog content
4. Creates entry in Supabase with `locale='en'` and new `article_id`
5. Outputs success message with article details

**Required env vars**: `GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

---

### `translate_blogs.py`

**Purpose**: Translate English blogs into 12 other languages

**Usage**:

```bash
python3 translate_blogs.py
```

**What it does**:

1. Fetches all English posts from Supabase
2. For each post, checks if translations exist
3. AI-translates missing language versions (es, pt, hi, fr, de, id, zh, zh-TW, ja, ko, th, vi)
4. Copies `article_id` to link all translations
5. Shows progress with success/error counts

**Required env vars**: `GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

**Note**: Uses OpenCC for Simplified → Traditional Chinese conversion

---

## Utility Scripts (This Directory)

### `fix_slugs.py`

**Purpose**: Update slugs to match new format (YYYYMMDD-name)

**When to use**: After slug format changes

---

### `force_regenerate.py`

**Purpose**: Force regenerate specific blog posts by ID

**When to use**: When a specific post needs content refresh

---

### `regenerate_blogs.py`

**Purpose**: Batch regenerate multiple blog posts

**When to use**: For bulk content updates

---

### `update_existing_names.py`

**Purpose**: Update interviewer/interviewee names in existing posts

**When to use**: To fix name formatting issues

---

### `generate_multilingual_blogs.py`

**Purpose**: Legacy script (use `generate_blogs.py` + `translate_blogs.py` instead)

**Status**: Deprecated - kept for reference

---

## Typical Workflow

### Adding New Content

1. **Generate English blog**:

   ```bash
   python3 generate_blogs.py
   # Enter YouTube URL when prompted
   ```

2. **Translate to all languages**:

   ```bash
   python3 translate_blogs.py
   ```

3. **Verify in database**:
   - Check Supabase for 13 rows (1 per language)
   - Verify same `article_id` across all translations

### Bulk Content Creation

For multiple videos, run generate + translate in a loop:

```bash
for url in "url1" "url2" "url3"; do
  echo "$url" | python3 generate_blogs.py
  python3 translate_blogs.py
done
```

---

## Database Schema

Required columns in `podcasts` table:

- `id` (serial primary key)
- `locale` (text) - Language code (en, zh, ja, etc.)
- `article_id` (uuid) - Groups translations together
- `total_views` (integer) - Shared view count across translations
- `views` (integer) - Individual language view count
- `md_slug` (text) - URL slug
- `interviewee` (text)
- `interviewer` (text)
- `interviewee_title` (text)
- `blog_content` (text)
- `thumbnail_url` (text)
- `publish_date` (date)
- `youtube_url` (text)

---

## Troubleshooting

**Script fails with API error**:

- Check `GEMINI_API_KEY` is valid
- Verify API quota hasn't been exceeded

**Translation script skips posts**:

- Ensure English version exists first
- Check if translations already exist (script skips duplicates)

**Slugs not generating correctly**:

- Run `scripts/fix_slugs.py` to normalize slugs

**View counts not syncing**:

- Verify `article_id` is same across all language versions
- Check database trigger for `total_views` update
