from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import re


def parse_duration(duration):
    # Parse the ISO 8601 duration string to get the total seconds
    match = re.match(
        r"P(?:(?P<days>\d+)D)?T?(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?",
        duration,
    )
    if not match:
        return 0
    parts = match.groupdict()
    time_seconds = (
        int(parts.get("days") or 0) * 86400
        + int(parts.get("hours") or 0) * 3600
        + int(parts.get("minutes") or 0) * 60
        + int(parts.get("seconds") or 0)
    )
    return time_seconds


def create_youtube_playlist_with_videos():
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/youtube"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    PORT = 8080

    # Get credentials and create an API client
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=PORT)
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Create a new, private playlist with the current date as the title
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    playlist_title = f"Tech Podcasts on {current_date}"
    body = {
        "snippet": {
            "title": playlist_title,
            "description": "A collection of top tech podcasts found on YouTube.",
            "tags": ["tech podcast", "API call"],
            "defaultLanguage": "en",
        },
        "status": {"privacyStatus": "public"},
    }

    try:
        playlist_response = (
            youtube.playlists().insert(part="snippet,status", body=body).execute()
        )
        playlist_id = playlist_response["id"]
        print(f"Created playlist ID: {playlist_id}")
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None

    # Calculate the date 7 days ago from today
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat(
        "T"
    ) + "Z"

    # Search for "tech podcast" on YouTube and retrieve more results from the past 7 days
    search_response = (
        youtube.search()
        .list(
            q="tech podcast interview",
            part="snippet",
            type="video",
            maxResults=30,  # Increase the number of results to ensure we get 10 videos longer than 2 minutes
            publishedAfter=seven_days_ago,
        )
        .execute()
    )

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

    # Get video details to filter out videos shorter than 2 minutes
    video_details_response = (
        youtube.videos().list(part="contentDetails", id=",".join(video_ids)).execute()
    )

    count = 0
    for item in video_details_response.get("items", []):
        duration = parse_duration(item["contentDetails"]["duration"])
        if duration >= 120:  # 2 minutes
            video_id = item["id"]
            add_video_request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            )
            add_video_response = add_video_request.execute()
            print(f"Added video {video_id} to playlist {playlist_id}")
            count += 1
        if count >= 10:  # Stop after adding 10 videos
            break

    return playlist_id
