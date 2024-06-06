import os


class YouTubeLinkRemover:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.content_dir = os.path.join(self.base_dir, "..", "..", "content")

    def remove_youtube_link(self):
        # Define the base URL pattern for YouTube
        youtube_base_url = "https://youtube.com/watch?v="

        # Iterate over each file in the content directory
        for filename in os.listdir(self.content_dir):
            if filename.endswith(".md"):  # Check if the file is a Markdown file
                filepath = os.path.join(self.content_dir, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                # Remove any trailing blank lines or lines with only whitespace
                while lines and lines[-1].strip() == "":
                    lines.pop()

                # Now check the last line if it exists and contains the YouTube URL
                if lines and youtube_base_url in lines[-1]:
                    # Write back all lines except the last one
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.writelines(lines[:-1])
                    print(f"Removed YouTube link from '{filename}'")
                else:
                    print(
                        f"No YouTube link found in the last non-blank line of '{filename}'"
                    )


# Usage
if __name__ == "__main__":
    remover = YouTubeLinkRemover()
    remover.remove_youtube_link()
