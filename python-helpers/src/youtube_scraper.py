import os
import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build


class YouTubeScraper:
    def __init__(self):
        load_dotenv()
        YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

        # Create a YouTube client
        SERVICE_NAME = "youtube"
        API_VERSION = "v3"

        self.yt = build(SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY)

    def get_youtube_urls(self, query: str):
        MAX_AGE = 7
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=MAX_AGE)

        MAX_RESULTS = 50
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        search_response = (
            self.yt.search()
            .list(
                q=query,
                part="id,snippet",
                maxResults=MAX_RESULTS,
                publishedAfter=start_date_str,
                publishedBefore=end_date_str,
                type="video",
            )
            .execute()
        )

        urls = []
        for search_result in search_response.get("items", []):
            video_id = search_result["id"]["videoId"]
            urls.append(f"https://www.youtube.com/watch?v={video_id}")

        return urls
