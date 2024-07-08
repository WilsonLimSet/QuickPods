import os
import re
import random
from dotenv import load_dotenv
from db.client import Client as DBClient
from appendURLS import Appender  # Import the Appender class


def clean_and_append_links(content, video_url, backlink_title, backlink_slug):
    """
    Clean up the end part of the blog post and append the video link and backlink consistently.

    Args:
    - content (str): The content of the blog post.
    - video_url (str): The URL of the video to be appended.
    - backlink_title (str): The title of the backlink blog post.
    - backlink_slug (str): The slug of the backlink blog post (without .md).

    Returns:
    - str: The cleaned and updated content of the blog post.
    """
    # Remove existing "Watch the podcast here!" and "Read another blog about" links
    content = re.sub(
        r'<a href="https://youtube.com/watch\?v=.*?" target="_blank">Watch the podcast here!</a>',
        "",
        content,
    )
    content = re.sub(r"\*\*Read another blog about \[.*?\]\(.*?\)\*\*", "", content)
    content = re.sub(r"---", "", content)

    # Remove any trailing whitespace
    content = content.rstrip()

    # Append the links consistently
    video_text = f'\n\n---\n\n<a href="{video_url}" target="_blank">Watch the podcast here!</a>\n'
    backlink_text = f"\n\n---\n\n**Read another blog about [{backlink_title}](./{backlink_slug})**\n"

    return content + video_text + backlink_text


def get_blog_titles_and_files(blog_dir):
    """Get a list of blog titles and their corresponding file paths."""
    blog_titles_files = []
    for filename in os.listdir(blog_dir):
        if filename.endswith(".md"):
            with open(os.path.join(blog_dir, filename), "r", encoding="utf-8") as file:
                content = file.read()
                title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                    blog_titles_files.append((title, filename))
    print(f"Found {len(blog_titles_files)} blog posts with titles.")
    return blog_titles_files


def clean_old_blogs(blog_dir, processed_entries):
    """Clean up old blog posts and append the video link and backlink consistently."""
    blog_titles_files = get_blog_titles_and_files(blog_dir)

    for youtube_url, md_slug in processed_entries:
        full_path = os.path.join(blog_dir, f"{md_slug}.md")
        other_blogs = [t for t in blog_titles_files if t[1] != f"{md_slug}.md"]
        if other_blogs:
            random_blog = random.choice(other_blogs)
            random_blog_slug = random_blog[1][:-3]  # Remove the '.md' extension
            with open(full_path, "r+", encoding="utf-8") as file:
                content = file.read()
                # Clean and append links
                updated_content = clean_and_append_links(
                    content, youtube_url, random_blog[0], random_blog_slug
                )
                file.seek(0)
                file.write(updated_content)
                file.truncate()
            print(f"Cleaned and updated {full_path}")
        else:
            print(f"No other blogs found to link for {md_slug}")


def main():
    load_dotenv()
    db = DBClient()
    appender = Appender()

    blog_dir = os.path.join(os.path.dirname(__file__), "..", "..", "content")
    processed_entries = (
        db.get_processed_urls()
    )  # Get processed entries from the database

    clean_old_blogs(blog_dir, processed_entries)


if __name__ == "__main__":
    main()
