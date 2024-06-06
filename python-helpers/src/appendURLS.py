import os
from dotenv import load_dotenv
from db.client import Client as DBClient


class Appender:
    def __init__(self):
        load_dotenv()
        self.db = DBClient()

    def append_youtube_url_to_md(self):
        base_dir = os.path.dirname(__file__)
        content_dir = os.path.join(base_dir, "..", "..", "content")
        processed_entries = (
            self.db.get_processed_urls()
        )  # Use the db client from the instance
        for youtube_url, md_slug in processed_entries:
            full_path = os.path.join(content_dir, f"{md_slug}.md")
            try:
                with open(full_path, "r+", encoding="utf-8") as file:
                    content = file.read()
                    # Create the HTML link with target="_blank"
                    link = f'\n<a href="{youtube_url}" target="_blank">Watch the podcast here!</a>\n'
                    if youtube_url not in content:
                        file.seek(
                            0, os.SEEK_END
                        )  # Move cursor to the end of file before writing
                        file.write(link)
                        self.db.update_url_appended(md_slug)
                        print(f"Updated '{full_path}' with YouTube URL.")
                    else:
                        print(f"URL already appended for '{md_slug}'.")
            except FileNotFoundError:
                print(f"Markdown file not found for slug: {md_slug}")
            except Exception as e:
                print(f"An error occurred while appending URL: {e}")


if __name__ == "__main__":
    appender = Appender()
    appender.append_youtube_url_to_md()
