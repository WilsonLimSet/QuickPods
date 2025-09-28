# Podummary Internationalization (i18n) Guide

## How It Works

Podummary automatically detects user language and serves content in their language with full SEO optimization.

### Supported Languages (13 Total)

- **en** - English (default)
- **es** - Spanish (Español)
- **pt** - Portuguese (Português)
- **hi** - Hindi (हिन्दी)
- **fr** - French (Français)
- **de** - German (Deutsch)
- **id** - Indonesian (Bahasa Indonesia)
- **zh** - Simplified Chinese (简体中文)
- **zh-TW** - Traditional Chinese (繁體中文)
- **ja** - Japanese (日本語)
- **ko** - Korean (한국어)
- **th** - Thai (ไทย)
- **vi** - Vietnamese (Tiếng Việt)

## How URLs Work

### Automatic Detection

When someone visits `podummary.com`:

1. The middleware checks their browser's `Accept-Language` header
2. Redirects to appropriate locale (e.g., `/zh/` for Chinese users, `/ja/` for Japanese)
3. Default fallback is `/en/` (English)

### URL Structure

All pages are prefixed with locale:

- English: `podummary.com/en/blog/anthony-tan-grab-ceo`
- Indonesian: `podummary.com/id/blog/anthony-tan-grab-ceo`
- Simplified Chinese: `podummary.com/zh/blog/anthony-tan-grab-ceo`
- Traditional Chinese: `podummary.com/zh-TW/blog/anthony-tan-grab-ceo`

### Cookie Persistence

Once a user visits `/id/`, a cookie `NEXT_LOCALE=id` is set. They'll stay on Indonesian version until they manually switch.

## SEO Benefits

### Multi-Language Google Indexing

All 13 language versions are indexed separately by Google with proper SEO signals:

- **Hreflang tags**: Each page includes links to all language versions
- **Dynamic sitemap**: Auto-generates entries for all locales
- **Proper metadata**: Each locale gets correct `lang` attribute and OpenGraph locale
- **Unified views**: All translations share same view count via `article_id` grouping

### Example: Anthony Tan Interview (Grab CEO)

- **Indonesian Google**: Indexes `podummary.com/id/blog/anthony-tan-grab-ceo`
- **Chinese Google**: Indexes both `podummary.com/zh/...` (Simplified) and `podummary.com/zh-TW/...` (Traditional)
- **Japanese Google**: Indexes `podummary.com/ja/blog/anthony-tan-grab-ceo`

### Metadata Per Locale

Each locale gets proper HTML tags:

```html
<!-- Chinese visitor sees -->
<html lang="zh">
  <meta property="og:locale" content="zh_CN" />
  <link rel="alternate" hreflang="zh-TW" href="podummary.com/zh-TW/blog/..." />
  <link rel="alternate" hreflang="en" href="podummary.com/en/blog/..." />
  <!-- ...all 13 languages -->
</html>
```

## Blog Content Translation

**Status**: ✅ **Fully implemented**

Both UI and blog content are fully translated into all 13 languages:

- ✅ UI components localized (navigation, buttons, footer, etc.)
- ✅ Blog posts AI-translated using Google Gemini
- ✅ Database has `locale` column for filtering
- ✅ Each article has unique `article_id` linking translations
- ✅ View counts unified across all language versions

### How It Works

1. **Content Generation** (`generate_blogs.py`):

   - Creates English blog post from YouTube video
   - Saves to Supabase with `locale='en'` and new `article_id`

2. **Translation** (`translate_blogs.py`):

   - Fetches English posts without translations
   - AI-translates to all 12 other languages
   - Each translation shares same `article_id`
   - View tracking unified via `total_views` column

3. **Frontend Serving**:
   - User visits `/zh/blog/slug` → gets Chinese content
   - User visits `/ja/blog/slug` → gets Japanese content
   - All versions show same unified view count

## Testing Locally

### Test Indonesian:

```bash
curl -H "Accept-Language: id-ID" http://localhost:3000
```

### Test Thai:

```bash
curl -H "Accept-Language: th-TH" http://localhost:3000
```

### Manual Testing:

- Visit: `http://localhost:3000/id/` for Indonesian
- Visit: `http://localhost:3000/th/` for Thai

## Adding More Languages

To add a 14th language (e.g., Malay):

1. **Add to locale lists** in both:

   - `i18n/request.ts`
   - `i18n/locales.ts`

2. **Create translation file** (`messages/ms.json`):

```json
{
  "common": {
    "siteName": "Podummary",
    "tagline": "Ringkasan Temuduga CEO & Pengasas Teknologi"
  },
  "home": { ... },
  "blog": { ... }
}
```

3. **Update translation scripts**:

   - Add to `translate_blogs.py` LOCALES list
   - Add to `languageNames` dict

4. **Deploy** - Middleware and sitemap auto-detect the new locale

## Production Deployment

### Vercel (Recommended)

Vercel automatically handles:

- ✅ Locale-based routing
- ✅ Edge caching per locale
- ✅ Geo-IP detection (even better than Accept-Language)

### Environment Variables

No additional env vars needed - i18n is baked into the build.

## Analytics Tracking

Track which locales are most popular:

```typescript
// In app/page.tsx
useEffect(() => {
  const locale = document.documentElement.lang;
  analytics.track("page_view", { locale });
}, []);
```

## Current Implementation Status

✅ **Completed Features:**

1. 13 language support with automatic detection
2. Full UI and blog content translation
3. Unified view tracking across translations
4. SEO optimization (hreflang, sitemap, metadata)
5. Automated translation pipeline with AI

🎯 **Production Ready:**

- All content is indexed separately by Google for each language
- Users see fully localized experience (UI + content)
- Analytics track engagement across all locales
- Scalable architecture for adding more languages

---

## Example User Journey

**Indonesian user from Jakarta searching "Anthony Tan wawancara":**

1. Google Indonesia shows: `podummary.com/id/blog/anthony-tan-grab-ceo`
2. They click → land on `/id/` version
3. **UI in Indonesian**: "Beranda", "Wawancara Terbaru", "Dibuat oleh"
4. **Blog content in Indonesian**: Full AI-translated summary
5. View count shared across all 13 language versions

**Chinese user from Beijing searching "Anthony Tan 采访":**

1. Google China shows: `podummary.com/zh/blog/anthony-tan-grab-ceo`
2. **UI in Simplified Chinese**: "首页", "最新访谈"
3. **Blog content in Simplified Chinese**: AI-translated summary
4. Same article available in Traditional Chinese at `podummary.com/zh-TW/...`
