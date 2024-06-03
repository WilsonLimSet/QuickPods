import time
import json
import re
import os
from dotenv import load_dotenv
from pytube import YouTube
from db.client import Client as DBClient
from models.model import Model as GeminiModel


class Summarizer:
    """Summarizes a list of YouTube urls, then stores them in a Supabase DB."""

    def __init__(self):
        load_dotenv()
        self.db = DBClient()
        self.model = GeminiModel()

    def generate_slug(self, publish_date, interviewee, interviewer):
        pattern = re.compile("[^a-zA-Z0-9_-]+")
        interviewee = pattern.sub("", interviewee).lower()
        interviewer = pattern.sub("", interviewer).lower()
        publish_date = publish_date.replace("-", "")
        return f"{publish_date}-{interviewee}-{interviewer}"

    def get_interviewee_name(self, yt_description: str):
        prompt = f"""
        Extract the full name of the interviewee from the following YouTube description. 
        The interviewee's name might appear early in the description, possibly following phrases like:
        - "interview with"
        - "talking to"
        - "conversation with"
        - "joined by"
        Please format the name in the 'First Last' format (e.g., 'John Doe'), even if the description presents it differently (e.g., 'Doe, John'). 
        Ensure that you provide only the full name of the interviewee and exclude any additional information.
        Description:
        {yt_description}
        """
        res = self.model.get_response(prompt)
        return res.strip()

    def process_youtube_videos(self, urls):
        """Process each YouTube video URL for content generation and upload the results if not already in the database."""

        for url in urls:
            if self.db.url_exists(url):
                print(f"URL present in DB, skipping: {url}")
                continue

            try:
                yt = YouTube(url)
                stream = yt.streams.first()  # needed or else description doesnt work
                print(yt.description)

                interviewee_name = self.get_interviewee_name(yt.description)

                slug = self.generate_slug(
                    yt.publish_date.strftime("%Y%m%d")
                    if yt.publish_date
                    else "UnknownDate",
                    interviewee_name,
                    yt.author,
                )

                data = {
                    "publish_date": yt.publish_date.strftime("%Y-%m-%d")
                    if yt.publish_date
                    else "Unknown publish date",
                    "youtube_url": yt.watch_url,
                    "thumbnail_url": yt.thumbnail_url,
                    "interviewer": yt.author,
                    "interviewee": interviewee_name,
                    "md_slug": slug,
                }

                self.db.upload(data)

                print(f'"{yt.title}" with slug: {slug}')
                print(json.dumps(data, indent=4))

                # Don't get rate-limited
                time.sleep(1)

            except ValueError as e:
                print(f"Skipping URL {url} due to error: {str(e)}")
