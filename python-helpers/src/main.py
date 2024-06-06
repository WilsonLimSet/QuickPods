from pytube import Playlist
from youtube_to_supabase import Summarizer


def main():
    summarizer = Summarizer()
    CURATED_PLAYLIST = "https://youtube.com/playlist?list=PL-GTGzXj_qq-MaH0q0aRXJKiL4PhB_0zN&si=s2iCLSrkZob_BoCN"
    playlist = Playlist(CURATED_PLAYLIST)
    summarizer.process_youtube_videos(playlist.video_urls)


if __name__ == "__main__":
    main()
