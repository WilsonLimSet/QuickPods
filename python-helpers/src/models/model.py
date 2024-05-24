import os
import google.generativeai as genai

class Model:
    def __init__(self):
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        GEMINI_MODEL = "models/gemini-1.5-pro-latest"
        
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
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
        try:
            file_id = genai.upload_file(path=audio_file_path)
            res = self.model.generate_content([prompt, file_id])
            if not res:
                return ""
        
            return res.text
        except Exception as e:
            print(f"Model.get_insights_from_audio: {str(e)}")
            return ""
