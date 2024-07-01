import os
import tempfile
import time
import json
import re
from pytube import YouTube, Playlist
from dotenv import load_dotenv
from models.model import Model as GeminiModel
from db.client import Client as DBClient
from playlist_creator import create_youtube_playlist_with_videos
from youtube_to_supabase import Summarizer
from generator import Generator

# Load environment variables once
load_dotenv()


class BlogUploader:
    def __init__(self):
        load_dotenv()
        self.db = DBClient()

    def upload_blogs_to_supabase(self):
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(base_dir, "content")
        blog_files = [f for f in os.listdir(content_dir) if f.endswith(".md")]

        for filename in blog_files:
            full_path = os.path.join(content_dir, filename)
            md_slug = filename[:-3]  # Strip the '.md' extension to use as a slug
            content = self.read_and_parse_file(full_path)
            if content:
                self.db.upload_blog(md_slug, content)

    def read_and_parse_file(self, full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                content = file.read()
            print(
                "File content read successfully:", content[:200]
            )  # Debugging: print first 200 chars
            return content
        except Exception as e:
            print(f"Error reading or parsing file {full_path}: {e}")
            return None


def main():
    # Step 1: Create or update the YouTube playlist
    print("Creating/updating YouTube playlist...")
    playlist_id = create_youtube_playlist_with_videos()
    print(f"Playlist ID: {playlist_id}")

    if playlist_id is not None:
        # Step 2: Process the videos in the playlist using Summarizer
        print("Processing videos in the playlist...")
        summarizer = Summarizer()
        CURATED_PLAYLIST = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Optional Manual Playlist here:
        ##CURATED_PLAYLIST = f"https://www.youtube.com/playlist?list={playlist_id}"
        print(f"Curated playlist URL: {CURATED_PLAYLIST}")

        try:
            playlist = Playlist(CURATED_PLAYLIST)
            urls = [
                video.watch_url for video in playlist.videos
            ]  # Get the URLs of the videos in the playlist
            print(f"Found {len(urls)} videos in the playlist.")
            summarizer.process_youtube_videos(urls)
            print("Videos processed successfully")
        except Exception as e:
            print(f"Error processing playlist: {e}")

        # Step 3: Generate blog posts from processed videos using Generator
        print("Generating blog posts from processed videos...")
        generator = Generator()
        generator.generate_blog_posts()
        print("Blog posts generated successfully")

        # Step 4: Upload blog posts to Supabase
        print("Uploading blog posts to Supabase...")
        uploader = BlogUploader()
        uploader.upload_blogs_to_supabase()
        print("Blog posts uploaded successfully")
    else:
        print("Failed to create or update the playlist.")


if __name__ == "__main__":
    main()
