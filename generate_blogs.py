#!/usr/bin/env python3
"""
QuickPods Blog Generator
Generates blog posts from YouTube playlist videos and uploads to Supabase
"""

import os
import re
import ssl
import uuid
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pytubefix import YouTube, Playlist
from supabase import create_client, Client
import google.generativeai as genai

# Fix SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

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

def clean_slug(text: str) -> str:
    """Create URL-friendly slug"""
    # Replace spaces and special chars with hyphens, then remove extra hyphens
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower())
    slug = re.sub(r'-+', '-', slug)  # Replace multiple hyphens with single
    return slug.strip('-')  # Remove leading/trailing hyphens

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
        # Clean response to extract JSON
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]

        data = json.loads(text.strip())
        name = data.get("name")
        title = data.get("title", "")

        # Return None if name is null, empty, or contains "unknown"
        if not name or "unknown" in name.lower():
            return None

        return {"name": name, "title": title}
    except Exception as e:
        print(f"   ⚠️  Error extracting interviewee info: {e}")
        return None

def generate_blog_post(video_url: str, title: str, description: str, interviewee: str, interviewer: str) -> str:
    """Generate blog post content using Gemini"""
    prompt = f"""
    Write a concise, informative blog post about this interview. Use the actual video details provided:

    Video Title: {title}
    Interviewee: {interviewee}
    Interviewer: {interviewer}
    Video Description: {description[:2000]}

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
            return f"In this interview, {interviewer} speaks with {interviewee}. {description[:200]}..."

        return blog_content
    except Exception as e:
        print(f"Error generating blog: {e}")
        return f"In this interview, {interviewer} speaks with {interviewee} about their experiences and insights in the industry."

def video_exists_in_db(youtube_url: str) -> bool:
    """Check if video already exists in database"""
    try:
        result = supabase.table("podcasts").select("id").eq("youtube_url", youtube_url).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error checking video existence: {e}")
        return False

def process_video(video_url: str):
    """Process a single video and upload to Supabase"""
    try:
        # Check if already processed
        if video_exists_in_db(video_url):
            print(f"⏭️  Video already in database: {video_url}")
            return

        print(f"\n📹 Processing: {video_url}")

        # Get video details
        yt = YouTube(video_url)
        title = yt.title
        description = yt.description or ""
        thumbnail = yt.thumbnail_url
        publish_date = yt.publish_date.strftime("%Y-%m-%d") if yt.publish_date else None
        channel_name = yt.author

        print(f"   Title: {title}")
        print(f"   Channel: {channel_name}")

        # Extract interviewee info
        print("   🤖 Extracting interviewee info...")
        interviewee_info = extract_interviewee_info(description, title)

        if not interviewee_info:
            print("   ⚠️  Could not extract interviewee name - skipping video")
            print("   Please manually verify the video description has a clear guest name\n")
            return

        interviewee = interviewee_info["name"]
        interviewee_title = interviewee_info["title"]
        print(f"   ✓ Interviewee: {interviewee}")
        if interviewee_title:
            print(f"   ✓ Title: {interviewee_title}")

        # Generate blog content
        print("   ✍️  Generating blog post...")
        blog_content = generate_blog_post(video_url, title, description, interviewee, channel_name)

        # Create slug from video title (more readable than names)
        date_str = publish_date.replace("-", "") if publish_date else datetime.now().strftime("%Y%m%d")
        # Use video title for slug, fallback to interviewee name
        title_slug = clean_slug(title[:60])  # Limit length
        slug = f"{date_str}-{title_slug}"

        # Upload to Supabase
        print("   📤 Uploading to Supabase...")
        article_id = str(uuid.uuid4())
        data = {
            "interviewer": channel_name,
            "interviewee": interviewee,
            "interviewee_title": interviewee_title,
            "thumbnail_url": thumbnail,
            "publish_date": publish_date,
            "md_slug": slug,
            "blog_content": blog_content,
            "youtube_url": video_url,
            "views": 0,
            "tag": "tech",
            "locale": "en",
            "article_id": article_id,
            "total_views": 0
        }

        result = supabase.table("podcasts").insert(data).execute()
        print(f"   ✅ Success! Slug: {slug} | Article ID: {article_id}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

def process_playlist(playlist_url: str):
    """Process all videos in a YouTube playlist"""
    try:
        print(f"\n🎬 Loading playlist: {playlist_url}")
        playlist = Playlist(playlist_url)
        videos = playlist.video_urls

        print(f"📊 Found {len(videos)} videos\n")

        for i, video_url in enumerate(videos, 1):
            print(f"[{i}/{len(videos)}]")
            process_video(video_url)

        print(f"\n🎉 Complete! Processed {len(videos)} videos")

    except Exception as e:
        print(f"❌ Playlist error: {e}")

def main():
    """Main entry point"""
    print("=" * 60)
    print("  QuickPods Blog Generator")
    print("=" * 60)

    # Check environment variables
    if not GEMINI_API_KEY:
        print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
        print("   Set it in .env.local file")
        print("   Get your key at: https://makersuite.google.com/app/apikey")
        return

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("\n❌ Error: Supabase credentials missing!")
        return

    print(f"\n✅ Configuration loaded")
    print(f"   Supabase: {SUPABASE_URL}")
    print(f"   Gemini: Configured")

    # Get playlist URL from user
    playlist_url = input("\n📎 Enter YouTube playlist URL: ").strip()

    if not playlist_url:
        print("❌ No URL provided")
        return

    process_playlist(playlist_url)

if __name__ == "__main__":
    main()