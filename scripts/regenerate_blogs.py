#!/usr/bin/env python3
"""
Regenerate blog content for existing posts in Supabase
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import google.generativeai as genai

# Load .env.local file
env_path = Path(__file__).parent / '.env.local'
load_dotenv(dotenv_path=env_path)

# Configuration
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_blog_post(video_url: str, interviewee: str, interviewer: str, video_title: str, video_description: str) -> str:
    """Generate blog post content using Gemini"""
    prompt = f"""
    Write a concise, informative blog post about this interview. Use the actual video details provided:

    Interviewee: {interviewee}
    Interviewer: {interviewer}
    Video Title: {video_title}
    Video Description: {video_description[:2000]}
    Video URL: {video_url}

    REQUIREMENTS:
    1. Write 300-500 words (SHORT and punchy, not 800+ words of fluff)
    2. Start with 1-2 sentences about who {interviewee} is based on the description
    3. List 3-4 SPECIFIC topics/insights discussed (pull from video title/description)
    4. Use concrete details, NOT generic buzzwords like "treacherous waters" or "force to be reckoned with"
    5. NO placeholder text like [mention industry] - use actual information from the description
    6. Write in a straightforward, journalistic style - NOT marketing hype
    7. Format in Markdown with bullet points for key topics

    FORBIDDEN:
    - Do NOT write "Unknown Guest" or use placeholders
    - Do NOT include title (added separately)
    - Do NOT include "Watch the video" links
    - Do NOT use generic phrases like "navigate challenges", "force to be reckoned with", "game-changer"
    - Do NOT make up information not in the video details

    If you cannot write a good post with the information provided, return just 2-3 sentences summarizing what's in the video title/description.
    """

    try:
        response = model.generate_content(prompt)
        blog_content = response.text.strip()

        # Check for placeholder text and reject if found
        if '[mention' in blog_content.lower() or 'unknown guest' in blog_content.lower():
            print(f"   ⚠️  AI generated placeholder text, using fallback")
            return f"In this interview, {interviewer} speaks with {interviewee}. {video_description[:200]}..."

        return blog_content
    except Exception as e:
        print(f"   ❌ Error generating blog: {e}")
        return None

def main():
    print("=" * 60)
    print("  QuickPods Blog Content Regenerator")
    print("=" * 60)

    # Fetch all posts with empty or minimal blog content
    print("\n📊 Fetching posts from database...")
    result = supabase.table("podcasts").select("*").execute()

    posts = result.data
    print(f"   Found {len(posts)} total posts")

    # Filter posts that need regeneration
    posts_to_update = [
        p for p in posts
        if not p.get('blog_content') or
        len(p.get('blog_content', '')) < 200 or
        'Unknown Guest' in p.get('interviewee', '')
    ]

    print(f"   {len(posts_to_update)} posts need blog content regeneration\n")

    if not posts_to_update:
        print("✅ All posts already have good content!")
        return

    for i, post in enumerate(posts_to_update, 1):
        print(f"[{i}/{len(posts_to_update)}] Processing: {post['interviewee']}")
        print(f"   Interviewer: {post['interviewer']}")

        # Fetch video details
        try:
            from pytubefix import YouTube
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context

            yt = YouTube(post['youtube_url'])
            video_title = yt.title
            video_description = yt.description or ""
        except Exception as e:
            print(f"   ⚠️  Could not fetch video: {e}")
            video_title = ""
            video_description = ""

        # Generate new blog content
        print("   ✍️  Generating blog post...")
        blog_content = generate_blog_post(
            post.get('youtube_url', ''),
            post['interviewee'],
            post['interviewer'],
            video_title,
            video_description
        )

        if blog_content:
            # Update in database
            print("   📤 Updating database...")
            supabase.table("podcasts").update({
                "blog_content": blog_content
            }).eq("id", post['id']).execute()
            print(f"   ✅ Success!\n")
        else:
            print(f"   ⚠️  Skipped (generation failed)\n")

    print("🎉 Complete! All blog posts have been regenerated.")
    print("   Refresh your browser to see the updated content.")

if __name__ == "__main__":
    main()