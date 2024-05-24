from pytube import Playlist
from src.youtube_to_supabase import Summarizer


def main():
    summarizer = Summarizer()
    CURATED_PLAYLIST = (
        "https://www.youtube.com/playlist?list=PL-GTGzXj_qq_pZCl6F2n1EsWtoet9dciH"
    )
    playlist = Playlist(CURATED_PLAYLIST)
    summarizer.process_youtube_videos(playlist.video_urls)


if __name__ == "__main__":
    main()
