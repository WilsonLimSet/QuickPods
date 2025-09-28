#!/usr/bin/env python3
"""
Force regenerate ALL blog posts with improved prompts
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
    print("  Force Regenerate ALL Blogs")
    print("=" * 60)

    result = supabase.table("podcasts").select("*").execute()
    posts = result.data

    print(f"\n📊 Found {len(posts)} posts to regenerate\n")

    for i, post in enumerate(posts, 1):
        print(f"[{i}/{len(posts)}] {post['interviewee']}")

        try:
            yt = YouTube(post['youtube_url'])
            video_title = yt.title
            video_description = yt.description or ""

            print("   ✍️  Generating new blog post...")
            blog_content = generate_blog_post(
                post['youtube_url'],
                post['interviewee'],
                post['interviewer'],
                video_title,
                video_description
            )

            if blog_content:
                supabase.table("podcasts").update({
                    "blog_content": blog_content
                }).eq("id", post['id']).execute()
                print(f"   ✅ Updated! ({len(blog_content)} chars)\n")
            else:
                print(f"   ⚠️  Skipped (generation failed)\n")

        except Exception as e:
            print(f"   ❌ Error: {e}\n")

    print("🎉 Complete! All blogs regenerated.")

if __name__ == "__main__":
    main()