import os
from dotenv import load_dotenv
from db.client import Client as DBClient


class BlogUploader:
    def __init__(self):
        load_dotenv()
        self.db = DBClient()

    def upload_blogs_to_supabase(self):
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(base_dir, "..", "..", "content")
        blog_files = [f for f in os.listdir(content_dir) if f.endswith(".md")]

        for filename in blog_files:
            full_path = os.path.join(content_dir, filename)
            md_slug = filename[:-3]  # Strip the '.md' extension to use as a slug
            content = self.read_and_parse_file(full_path)
            if content:
                self.db.upload_blog(md_slug, content)  # Use the upload method

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


if __name__ == "__main__":
    uploader = BlogUploader()
    uploader.upload_blogs_to_supabase()
