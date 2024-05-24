import os
from supabase import create_client, Client

class Client:
    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        self.cli: Client = create_client(supabase_url, supabase_key)
        self.table_name = "Podcasts"
    
    def upload(self, data):
        self.cli.table(self.table_name).insert(data).execute()
    
    def url_exists(self, url: str):
        def standardize_url(url: str):
            if url.startswith('http://www.'):
                url = 'https://' + url[len('http://www.'):]
            elif url.startswith('http://'):
                url = 'https://' + url[len('http://'):]
            elif url.startswith('https://www.'):
                url = 'https://' + url[len('https://www.'):]
            elif url.startswith('https://'):
                url = url
            else:
                url = 'https://' + url

            return url
        TARGET_COL = "youtube_url"
        res = self.cli.table(self.table_name).select(TARGET_COL).execute()

        urls = set(item[TARGET_COL] for item in res.data)
        standardized = standardize_url(url)

        return standardized in urls

