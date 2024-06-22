from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime


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
        "status": {"privacyStatus": "private"},
    }

    try:
        playlist_response = (
            youtube.playlists().insert(part="snippet,status", body=body).execute()
        )
        playlist_id = playlist_response["id"]
        print(f"Created playlist ID: {playlist_id}")
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return

    # Search for "tech podcast" on YouTube and retrieve the top 10 results
    search_response = (
        youtube.search()
        .list(q="tech podcast", part="snippet", type="video", maxResults=10)
        .execute()
    )

    # Insert search results into the playlist
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
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


# Example usage
create_youtube_playlist_with_videos()
