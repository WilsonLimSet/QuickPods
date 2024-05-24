import os
import tempfile
from pytube import YouTube
from dotenv import load_dotenv
from models.model import Model as GeminiModel


class Generator:
    def __init__(self):
        load_dotenv()
        self.model = GeminiModel()

    def download_audio(self, url: str):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            yt = YouTube(url)
            if yt.length > 8800:  # Limiting the video duration
                raise ValueError(f"Video duration too long: {yt.length / 60} minutes")
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                raise ValueError("No audio streams available.")
            audio_file = temp_file.name
            audio_stream.download(output_path=".", filename=audio_file)
            return yt, audio_file

    def upload_and_transcribe(self, file_path: str):
        prompt = """
        Given this audio file, write an engaging blog post the most interesting insights learnt

        """
        res = self.model.execute_prompt_from_audio(prompt, file_path)
        return res.strip()

    def process_podcast(self, url: str):
        try:
            yt, audio_file = self.download_audio(url)
            insights = self.upload_and_transcribe(audio_file)
            return insights
        except ValueError as e:
            print(f"Error processing podcast: {str(e)}")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    def generate_markdown_file(self, insights, file_path):
        title = "Podcast Insights on Technology and Innovation"
        date = "2024-05-23"
        tags = "Tech, Innovation, AI"

        markdown_content = f"""
---
title: "{title}"
date: "{date}"
tags: [{tags}]
---

## Key Insights

{insights}

---
        """
        # Construct the path to the 'content' folder relative to the current script location
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(
            base_dir, "..", "..", "content"
        )  # Move one directory up and into 'content'
        full_path = os.path.join(content_dir, file_path)

        # Create the content directory if it does not exist
        os.makedirs(content_dir, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as file:
            file.write(markdown_content)


if __name__ == "__main__":
    generator = Generator()
    url = "https://www.youtube.com/watch?v=a3sQEIfYMxU"  # Example URL
    insights = generator.process_podcast(url)
    if insights:
        generator.generate_markdown_file(insights, "output_markdown.md")
