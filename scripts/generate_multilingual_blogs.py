#!/usr/bin/env python3
"""
Generate multilingual blog posts from existing English content
"""

import os
import ssl
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import google.generativeai as genai

ssl._create_default_https_context = ssl._create_unverified_context

env_path = Path(__file__).parent / '.env.local'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# All supported languages (10 total)
LANGUAGES = {
    'en': 'English',
    'zh': 'Simplified Chinese (简体中文)',
    'ja': 'Japanese (日本語)',
    'ko': 'Korean (한국어)',
    'id': 'Indonesian (Bahasa Indonesia)',
    'es': 'Spanish (Español)',
    'pt': 'Portuguese (Português)',
    'hi': 'Hindi (हिन्दी)',
    'fr': 'French (Français)',
    'de': 'German (Deutsch)',
}

def translate_blog_post_and_slug(english_content: str, english_slug: str, target_locale: str, interviewee: str, interviewer: str) -> dict:
    """Translate English blog content and create localized slug"""
    target_language = LANGUAGES[target_locale]

    # First, translate the blog content
    content_prompt = f"""
    Translate this blog post to {target_language}. Maintain the same structure, tone, and meaning.

    Original English content:
    {english_content}

    Requirements:
    1. Translate to natural, fluent {target_language}
    2. Keep all markdown formatting intact
    3. Preserve technical terms when appropriate
    4. Maintain the same paragraph structure
    5. Keep names (like "{interviewee}", "{interviewer}") in their original form
    6. Ensure the content reads naturally for native speakers
    7. Do NOT add any additional content or explanations

    Return ONLY the translated blog post in {target_language}, nothing else.
    """

    # Then, create a localized slug
    # Extract date from original slug (first 8 chars: YYYYMMDD)
    date_part = english_slug[:8]
    title_part = english_slug[9:]  # Everything after date and hyphen

    slug_prompt = f"""
    Create a URL-friendly slug in {target_language} for this interview title.

    Original English slug: "{title_part}"
    Interviewee: {interviewee}

    Requirements:
    1. Translate the key concepts to {target_language}
    2. Keep it under 60 characters
    3. Use only lowercase letters, numbers, and hyphens
    4. Make it SEO-friendly for {target_language} speakers
    5. Replace spaces with hyphens

    Return ONLY the translated slug part (without the date), nothing else.
    """

    try:
        # Get translated content
        content_response = model.generate_content(content_prompt)
        translated_content = content_response.text.strip()

        # Get localized slug
        slug_response = model.generate_content(slug_prompt)
        translated_slug_part = slug_response.text.strip().lower()

        # Clean slug (remove any non-URL-friendly chars)
        import re
        clean_slug_part = re.sub(r'[^a-z0-9\-]', '', translated_slug_part.replace(' ', '-'))
        clean_slug_part = re.sub(r'-+', '-', clean_slug_part).strip('-')

        # Combine date + translated slug
        localized_slug = f"{date_part}-{clean_slug_part}"

        return {
            "content": translated_content,
            "slug": localized_slug
        }
    except Exception as e:
        print(f"   ❌ Error translating to {target_locale}: {e}")
        return None

def main():
    print("=" * 60)
    print("  Multilingual Blog Generator")
    print("=" * 60)
    print(f"🌍 Generating content in {len(LANGUAGES)} languages")
    print(f"📋 Languages: {', '.join(LANGUAGES.keys())}")

    # First, run the database migration
    print("\n📊 Setting up database schema...")
    try:
        # Read and execute the SQL migration
        with open('supabase-multilingual.sql', 'r') as f:
            sql_commands = f.read()

        # Note: This won't work with python supabase client, user needs to run manually
        print("⚠️  Please run the following SQL in your Supabase dashboard:")
        print("   Settings → SQL Editor → New Query → Paste this:")
        print("-" * 40)
        print(sql_commands)
        print("-" * 40)
        input("Press Enter after running the SQL migration...")
    except Exception as e:
        print(f"⚠️  Could not read SQL file: {e}")
        input("Press Enter to continue anyway...")

    # Get all English blog posts
    print("\n📚 Fetching English blog posts...")
    result = supabase.table("podcasts").select("*").eq("locale", "en").execute()
    english_posts = result.data

    if not english_posts:
        print("❌ No English posts found. Make sure existing posts have locale='en'")
        return

    print(f"   Found {len(english_posts)} English posts")

    # Generate translations for each post
    for i, post in enumerate(english_posts, 1):
        print(f"\n[{i}/{len(english_posts)}] {post['interviewee']}")

        # Skip if no blog content
        if not post.get('blog_content'):
            print("   ⏭️  No blog content, skipping")
            continue

        # Generate for each target language (skip English)
        for locale in LANGUAGES.keys():
            if locale == 'en':
                continue  # Skip English (already exists)

            print(f"   🌐 Translating to {LANGUAGES[locale]}...")

            # Translate the content and create localized slug
            translation_result = translate_blog_post_and_slug(
                post['blog_content'],
                post['md_slug'],
                locale,
                post['interviewee'],
                post['interviewer']
            )

            if translation_result:
                translated_content = translation_result['content']
                localized_slug = translation_result['slug']

                # Check if translation already exists (by localized slug)
                existing = supabase.table("podcasts").select("id").eq("md_slug", localized_slug).eq("locale", locale).execute()
                if existing.data:
                    print(f"      ✅ Already exists, skipping")
                    continue
                # Create new row for this language
                new_post = {
                    'interviewer': post['interviewer'],
                    'interviewee': post['interviewee'],
                    'interviewee_title': post.get('interviewee_title', ''),
                    'thumbnail_url': post['thumbnail_url'],
                    'publish_date': post['publish_date'],
                    'md_slug': localized_slug,  # Localized slug for this language
                    'blog_content': translated_content,
                    'youtube_url': post['youtube_url'],
                    'views': 0,  # Start with 0 views for translations
                    'tag': post.get('tag', 'tech'),
                    'locale': locale  # Different locale
                }

                try:
                    supabase.table("podcasts").insert(new_post).execute()
                    print(f"      ✅ Created {locale} version: /{locale}/blog/{localized_slug}")
                except Exception as e:
                    print(f"      ❌ Error saving {locale}: {e}")
            else:
                print(f"      ⚠️  Translation failed for {locale}")

    total_posts = len(english_posts) * (len(LANGUAGES) - 1)  # -1 for English
    cost = total_posts * 0.0004
    print(f"\n🎉 Complete!")
    print(f"   📊 Generated {total_posts} translated posts")
    print(f"   💰 Estimated cost: ${cost:.2f}")
    print(f"\n🌐 Your site now supports:")
    for locale, name in LANGUAGES.items():
        print(f"   • /{locale}/ - {name}")

if __name__ == "__main__":
    main()