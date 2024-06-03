import os
import tempfile
from pytube import YouTube
from dotenv import load_dotenv
from models.model import Model as GeminiModel
from db.client import Client as DBClient


class Generator:
    def __init__(self):
        load_dotenv()
        self.model = GeminiModel()
        self.db = DBClient()

    def download_audio(self, url: str):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            yt = YouTube(url)
            if yt.length > 22000:  # Limiting the video duration
                raise ValueError(f"Video duration too long: {yt.length / 60} minutes")
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                raise ValueError("No audio streams available.")
            audio_file = temp_file.name
            audio_stream.download(output_path=".", filename=audio_file)
            return yt, audio_file

    def upload_and_transcribe(self, file_path: str):
        prompt = """
        Given this audio file, write an engaging blog post about the most interesting insights learned with subheadings, 
        summaries, a few bullet points and a single key quote to end things off.
        """
        res = self.model.execute_prompt_from_audio(prompt, file_path)
        return res.strip()

    def process_podcast(self, url: str):
        try:
            yt, audio_file = self.download_audio(url)
            print("Processing ", yt.title)
            insights = self.upload_and_transcribe(audio_file)
            return yt.title, insights
        except ValueError as e:
            print(f"Error processing podcast: {str(e)}")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    def generate_markdown_file(self, title, insights, slug, publish_date):
        tags = "Tech, Innovation, AI"

        markdown_content = f"""
---
title: "{title}"
date: "{publish_date}"
tags: [{tags}]
---

{insights}

---
        """
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(base_dir, "..", "..", "content")
        full_path = os.path.join(content_dir, f"{slug}.md")
        os.makedirs(content_dir, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(markdown_content)

    def generate_blog_posts(self):
        urls_and_slugs = (
            self.db.get_unprocessed_urls()
        )  # Get URLs and slugs where blog_generated is false
        for url, slug, publish_date in urls_and_slugs:
            podcast_title, insights = self.process_podcast(url)
            if insights:
                self.generate_markdown_file(podcast_title, insights, slug, publish_date)
                print(f"Generated Blog for {slug}")
                self.db.update_blog_generated(
                    url
                )  # Update the database to mark this URL as processed


if __name__ == "__main__":
    generator = Generator()
    generator.generate_blog_posts()
