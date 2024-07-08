import os
import random
import re
import json
from dotenv import load_dotenv
from db.client import Client as DBClient
from playlist_creator import create_youtube_playlist_with_videos
from youtube_to_supabase import Summarizer
from url_to_blogpost import Generator
from pytube import Playlist

# Load environment variables once
load_dotenv()


class BlogUploader:
    def __init__(self):
        load_dotenv()
        self.db = DBClient()
        self.processed_file = os.path.join(
            os.path.dirname(__file__), "processed_blogs.json"
        )
        self.processed_blogs = self.load_processed_blogs()

    def load_processed_blogs(self):
        """Load the list of processed blog files."""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_processed_blogs(self):
        """Save the list of processed blog files."""
        with open(self.processed_file, "w", encoding="utf-8") as file:
            json.dump(self.processed_blogs, file)

    def get_blog_titles_and_files(self, blog_dir):
        """Get a list of blog titles and their corresponding file paths."""
        blog_titles_files = []
        for filename in os.listdir(blog_dir):
            if filename.endswith(".md"):
                with open(
                    os.path.join(blog_dir, filename), "r", encoding="utf-8"
                ) as file:
                    content = file.read()
                    title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1)
                        blog_titles_files.append((title, filename))
        return blog_titles_files

    def append_backlink_to_blog(self, blog_dir, blog_titles_files):
        """Append a backlink to each new blog post."""
        for title, filename in blog_titles_files:
            if filename not in self.processed_blogs:
                other_blogs = [t for t in blog_titles_files if t[1] != filename]
                if other_blogs:
                    random_blog = random.choice(other_blogs)
                    backlink_text = f"\n\n---\n\n**Read another blog about [{random_blog[0]}](./{random_blog[1]})**\n"
                    with open(
                        os.path.join(blog_dir, filename), "a", encoding="utf-8"
                    ) as file:
                        file.write(backlink_text)
                    self.processed_blogs.append(filename)
                    print(f"Appended backlink to {filename}")

    def upload_blogs_to_supabase(self):
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(base_dir, "..", "..", "content")
        blog_files = [f for f in os.listdir(content_dir) if f.endswith(".md")]

        blog_titles_files = self.get_blog_titles_and_files(content_dir)
        self.append_backlink_to_blog(content_dir, blog_titles_files)
        self.save_processed_blogs()

        for filename in blog_files:
            if filename not in self.processed_blogs:
                full_path = os.path.join(content_dir, filename)
                md_slug = filename[:-3]  # Strip the '.md' extension to use as a slug
                content = self.read_and_parse_file(full_path)
                if content:
                    self.db.upload_blog(md_slug, content)
                    self.processed_blogs.append(filename)
                    print(f"Uploaded blog: {filename}")

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
    # print("Creating/updating YouTube playlist...")
    # playlist_id = create_youtube_playlist_with_videos()
    # print(f"Playlist ID: {playlist_id}")

    # if playlist_id is not None:
    #     # Step 2: Process the videos in the playlist using Summarizer
    #     print("Processing videos in the playlist...")
    #
    ##CURATED_PLAYLIST = f"https://www.youtube.com/playlist?list={playlist_id}"
    # Optional Manual Playlist here:
    CURATED_PLAYLIST = (
        f"https://www.youtube.com/playlist?list=PL-GTGzXj_qq_hzY_YOo7NsyW7fSDwyNeJ"
    )
    print(f"Curated playlist URL: {CURATED_PLAYLIST}")
    summarizer = Summarizer()

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

    # else:
    #     print("Failed to create or update the playlist.")
# else:
#     print("Failed to create or update the playlist.")



if __name__ == "__main__":
    main()
