# backend/app/adapters/gemini_adapter.py (實作配接器)

import os
import google.genai as genai
from google.genai import Client
from langfuse import Langfuse
from app.ports.ai_service import AIServicePort

class GeminiAdapter(AIServicePort):
    def __init__(self, api_key=None):
      my_api_key = api_key or os.getenv("GEMINI_API_KEY")
      if not my_api_key:
          raise ValueError("GEMINI_API_KEY 未設定，請在 .env 檔案中加入 GEMINI_API_KEY=你的金鑰")
      self.client = Client(api_key=my_api_key)

      # genai.configure(api_key=api_key)
      # self.model = genai.GenerativeModel('gemini-flash-latest')
      self.model = "gemini-flash-latest"
      # self.langfuse = Langfuse() # 初始化 Langfuse

    def grade_essay(self, content: str):
      # 使用 Langfuse 追蹤 Prompt
      # trace = self.langfuse.trace(name="essay-grading")
      prompt = f"你是一位專業英文老師。請修正語法錯誤，並給予建議：{content}"
      
      # response = self.model.generate_content(prompt)

      response = self.client.models.generate_content(
          model=self.model, 
          contents=prompt
      )
      
      # 這裡簡化處理，實際建議解析 JSON
      return {"feedback": response.text}