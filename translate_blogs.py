#!/usr/bin/env python3
"""
QuickPods Blog Translator
Translates existing English blog posts into multiple languages
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import google.generativeai as genai

env_path = Path(__file__).parent / '.env.local'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

LANGUAGES = {
    "zh": "Simplified Chinese (简体中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "id": "Indonesian (Bahasa Indonesia)",
    "es": "Spanish (Español)",
    "pt": "Portuguese (Português)",
    "hi": "Hindi (हिन्दी)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "th": "Thai (ไทย)",
    "vi": "Vietnamese (Tiếng Việt)",
}

def translate_blog_content(content: str, target_language: str, language_name: str) -> str:
    """Translate blog content to target language"""
    prompt = f"""
    Translate the following tech CEO interview blog post to {language_name}.

    REQUIREMENTS:
    1. Maintain the exact same structure and formatting (markdown, bullet points, etc.)
    2. Translate naturally - don't be literal, make it sound native
    3. Keep proper nouns (names, companies) as-is
    4. Keep technical terms where appropriate (e.g., "CEO", "startup" can remain in some languages)
    5. Return ONLY the translated text, no explanations or metadata

    Original text in English:
    {content}

    Translated text in {language_name}:
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"   ❌ Translation error: {e}")
        return None

def entry_exists(slug: str, locale: str) -> bool:
    """Check if translated entry already exists"""
    try:
        result = supabase.table("podcasts").select("id").eq("md_slug", slug).eq("locale", locale).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"   Error checking existence: {e}")
        return False

def translate_podcast(podcast: dict, target_locale: str, language_name: str):
    """Translate a single podcast entry to target language"""
    try:
        slug = podcast['md_slug']

        if entry_exists(slug, target_locale):
            print(f"   ⏭️  {target_locale.upper()} translation already exists")
            return

        print(f"   🔄 Translating to {language_name}...")

        translated_content = translate_blog_content(
            podcast['blog_content'],
            target_locale,
            language_name
        )

        if not translated_content:
            print(f"   ❌ Failed to translate")
            return

        new_entry = {
            "interviewer": podcast['interviewer'],
            "interviewee": podcast['interviewee'],
            "interviewee_title": podcast['interviewee_title'],
            "thumbnail_url": podcast['thumbnail_url'],
            "publish_date": podcast['publish_date'],
            "md_slug": slug,
            "blog_content": translated_content,
            "youtube_url": podcast['youtube_url'],
            "views": 0,
            "tag": podcast.get('tag', 'tech'),
            "locale": target_locale,
            "article_id": podcast['article_id'],
            "total_views": podcast.get('total_views', 0)
        }

        result = supabase.table("podcasts").insert(new_entry).execute()
        print(f"   ✅ {target_locale.upper()} translation created")

    except Exception as e:
        print(f"   ❌ Error translating to {target_locale}: {e}")

def main():
    """Main entry point"""
    print("=" * 60)
    print("  QuickPods Blog Translator")
    print("=" * 60)

    if not GEMINI_API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
        print("\n❌ Error: Missing credentials in .env.local")
        return

    print(f"\n✅ Configuration loaded")
    print(f"   Supabase: {SUPABASE_URL}")
    print(f"   Languages: {len(LANGUAGES)}")

    print("\n📊 Fetching English blog posts...")
    result = supabase.table("podcasts").select("*").eq("locale", "en").execute()

    english_posts = result.data
    print(f"   Found {len(english_posts)} English posts")

    if not english_posts:
        print("   No English posts to translate")
        return

    print(f"\n🌍 Starting translation to {len(LANGUAGES)} languages...\n")

    for i, post in enumerate(english_posts, 1):
        print(f"[{i}/{len(english_posts)}] {post['interviewee']} - {post['md_slug']}")

        for locale, language_name in LANGUAGES.items():
            translate_podcast(post, locale, language_name)

        print()

    print(f"\n🎉 Translation complete!")
    print(f"   Original: {len(english_posts)} English posts")
    print(f"   Generated: {len(english_posts) * len(LANGUAGES)} translations")

if __name__ == "__main__":
    main()