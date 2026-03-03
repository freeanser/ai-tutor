# backend/app/adapters/gemini_adapter.py (實作配接器)

import os
import google.genai as genai
from google.genai import Client
# from langfuse.decorators import observe, langfuse_context
from langfuse import Langfuse
from app.ports.ai_service import AIServicePort
import google.genai.errors as errors

class GeminiAdapter(AIServicePort):
    def __init__(self, api_key=None):
      my_api_key = api_key or os.getenv("GEMINI_API_KEY")
      if not my_api_key:
          raise ValueError("GEMINI_API_KEY 未設定，請在 .env 檔案中加入 GEMINI_API_KEY=你的金鑰")
      self.client = Client(api_key=my_api_key)

      self.model = "gemini-flash-latest"
      self.lf = Langfuse()

    def grade_essay(self, content: str):
        try:
            # 1. 從 Langfuse 拿 Prompt
            langfuse_prompt = self.lf.get_prompt("essay-teacher-prompt")
            compiled_prompt = langfuse_prompt.compile(user_content=content)

            # 2. 呼叫 Gemini
            response = self.client.models.generate_content(
                model=self.model, 
                contents=compiled_prompt
            )
            return {"feedback": response.text}

        except errors.ServerError:
            return {"feedback": "抱歉，目前 AI 老師太忙了（太多學生同時在使用此 AI 功能），請稍後再試。"}
        except Exception as e:
            print(f"Error: {e}")
            return {"feedback": "發生未知的錯誤，請檢查網路連線。"}

    # def grade_essay(self, content: str):
    #     # 1. 抓取 Prompt (預設會抓 production label)
    #     langfuse_prompt = self.lf.get_prompt("essay-teacher-prompt")
        
    #     # 2. 編譯 Prompt (將 {{user_content}} 替換為實際內容)
    #     compiled_prompt = langfuse_prompt.compile(user_content=content)

    #     # 3. 呼叫 Gemini SDK
    #     response = self.client.models.generate_content(
    #         model=self.model, 
    #         contents=compiled_prompt
    #     )
    #     return {"feedback": response.text}
