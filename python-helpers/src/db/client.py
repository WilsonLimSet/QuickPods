import os
from supabase import create_client, Client


class Client:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        self.cli: Client = create_client(supabase_url, supabase_key)
        self.table_name = "Podcasts"

    def upload(self, data):
        self.cli.table(self.table_name).insert(data).execute()

    def update_blog_generated(self, url):
        """Update the 'blog_generated' status to True for a specific YouTube URL."""
        update_result = (
            self.cli.table(self.table_name)
            .update(
                {
                    "blog_generated": True  # Set the field to True
                }
            )
            .eq("youtube_url", url)
            .execute()
        )  # Match the row where 'youtube_url' equals the given URL

    def update_url_appended(self, url):
        """Update the 'url_appended' status to True for a specific YouTube URL."""
        update_result = (
            self.cli.table(self.table_name)
            .update(
                {
                    "url_appended": True  # Set the field to True
                }
            )
            .eq("md_slug", url)
            .execute()
        )

    def get_unprocessed_urls(self):
        """Retrieve YouTube URLs and slugs from the database where blog_generated is false."""

        query_result = (
            self.cli.table(self.table_name)
            .select("youtube_url, md_slug, publish_date")
            .eq("blog_generated", False)
            .execute()
        )
        print(query_result)
        return [
            (item["youtube_url"], item["md_slug"], item["publish_date"])
            for item in query_result.data
        ]

    def get_processed_urls(self):
        """Retrieve YouTube URLs and slugs from the database where blog_generated is true."""

        query_result = (
            self.cli.table(self.table_name)
            .select("youtube_url, md_slug")
            .eq("blog_generated", True)
            .execute()
        )
        print(query_result)
        return [(item["youtube_url"], item["md_slug"]) for item in query_result.data]

    def url_exists(self, url: str):
        def standardize_url(url: str):
            if url.startswith("http://www."):
                url = "https://" + url[len("http://www.") :]
            elif url.startswith("http://"):
                url = "https://" + url[len("http://") :]
            elif url.startswith("https://www."):
                url = "https://" + url[len("https://www.") :]
            elif url.startswith("https://"):
                url = url
            else:
                url = "https://" + url

            return url

        TARGET_COL = "youtube_url"
        res = self.cli.table(self.table_name).select(TARGET_COL).execute()

        urls = set(item[TARGET_COL] for item in res.data)
        standardized = standardize_url(url)

        return standardized in urls
