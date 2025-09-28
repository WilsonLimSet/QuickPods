#!/usr/bin/env python3
"""
Update existing posts with better name/title extraction
"""

import os
import ssl
from pathlib import Path
from dotenv import load_dotenv
from pytubefix import YouTube
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

def extract_interviewee_info(description: str, title: str) -> dict:
    """Extract interviewee name and title from video description or title"""
    prompt = f"""
    Extract information about the person being interviewed from this YouTube video info.

    Title: {title}
    Description: {description[:1000]}

    Look for patterns like:
    - "*Name*" (markdown emphasis)
    - "CEO Name"
    - "Name, Title"
    - "Title Name"

    IMPORTANT:
    - If you cannot find a clear person's name, return null for the name field
    - Do NOT make up names or use placeholders like "Unknown Guest"
    - Only return a name if you are confident it's correct

    Return a JSON object with:
    {{
        "name": "First Last" or null if not found,
        "title": "CEO of Company" or "Author of Book" or similar role description or empty string
    }}

    Return ONLY valid JSON, nothing else.
    """

    try:
        response = model.generate_content(prompt)
        import json
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]

        data = json.loads(text.strip())
        name = data.get("name")
        title = data.get("title", "")

        if not name or "unknown" in name.lower():
            return None

        return {"name": name, "title": title}
    except Exception as e:
        print(f"   ⚠️  Error extracting: {e}")
        return None

def main():
    print("=" * 60)
    print("  Update Existing Names & Titles")
    print("=" * 60)

    result = supabase.table("podcasts").select("*").execute()
    posts = result.data

    print(f"\n📊 Found {len(posts)} posts\n")

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['interviewee']}")

        # Skip if already has good data
        if post['interviewee'] and post['interviewee'] != 'Unknown Guest' and 'unknown' not in post['interviewee'].lower():
            if post.get('interviewee_title'):
                print(f"   ✅ Already good: {post['interviewee']} - {post['interviewee_title']}\n")
                continue

        try:
            yt = YouTube(post['youtube_url'])
            title = yt.title
            description = yt.description or ""

            print("   🤖 Re-extracting info...")
            info = extract_interviewee_info(description, title)

            if info:
                print(f"   ✓ Found: {info['name']}")
                if info['title']:
                    print(f"   ✓ Title: {info['title']}")

                supabase.table("podcasts").update({
                    "interviewee": info['name'],
                    "interviewee_title": info['title']
                }).eq("id", post['id']).execute()
                print("   📤 Updated!\n")
            else:
                print("   ⚠️  Could not extract name - keeping original\n")

        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    print("🎉 Complete!")

if __name__ == "__main__":
    main()