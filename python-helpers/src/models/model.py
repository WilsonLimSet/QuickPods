import os
import google.generativeai as genai
import time


class Model:
    def __init__(self):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=google_api_key)
        GEMINI_MODEL = "models/gemini-1.5-pro-latest"
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        self.model = genai.GenerativeModel(
            GEMINI_MODEL, safety_settings=safety_settings
        )

    def get_response(self, query: str):
        try:
            res = self.model.generate_content([query])
            if not res:
                return ""

            return res.text
        except Exception as e:
            print(f"Model.get_response: {str(e)}")
            return ""

    def execute_prompt_from_audio(self, prompt: str, audio_file_path):
        retries = 1  # Number of retries
        for attempt in range(retries):
            try:
                file_id = genai.upload_file(path=audio_file_path)
                res = self.model.generate_content(
                    [prompt, file_id], request_options={"timeout": 10000}
                )
                if res:
                    time.sleep(1)
                    return res.text

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                print(res.prompt_feedback)
                if attempt < retries - 1:
                    print("Retrying...")
                else:
                    print("All attempts failed.")
        return ""
