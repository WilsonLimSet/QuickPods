#!/usr/bin/env python3
"""
Fix existing blog post slugs to be more readable
"""

import os
import re
import ssl
from pathlib import Path
from dotenv import load_dotenv
from pytubefix import YouTube
from supabase import create_client, Client

ssl._create_default_https_context = ssl._create_unverified_context

env_path = Path(__file__).parent / '.env.local'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_slug(text: str) -> str:
    """Create URL-friendly slug"""
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower())
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def main():
    print("=" * 60)
    print("  Fix Blog Post Slugs")
    print("=" * 60)

    result = supabase.table("podcasts").select("*").execute()
    posts = result.data

    print(f"\n📊 Found {len(posts)} posts\n")

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['interviewee']}")
        print(f"   Old slug: {post['md_slug']}")

        try:
            yt = YouTube(post['youtube_url'])
            title = yt.title
            publish_date = post['publish_date']

            # Create new slug from title
            date_str = publish_date.replace("-", "")
            title_slug = clean_slug(title[:60])
            new_slug = f"{date_str}-{title_slug}"

            print(f"   New slug: {new_slug}")

            supabase.table("podcasts").update({
                "md_slug": new_slug
            }).eq("id", post['id']).execute()
            print("   ✅ Updated!\n")

        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    print("🎉 Complete!")

if __name__ == "__main__":
    main()