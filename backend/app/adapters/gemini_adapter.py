# backend/app/adapters/gemini_adapter.py (實作配接器)

import os
import google.genai as genai
from google.genai import Client
# from langfuse.decorators import observe, langfuse_context
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
      # 將 Langfuse 初始化放在這裡，避免每次請求都重新連線
      self.lf = Langfuse()

    # def grade_essay(self, content: str):
    #   # 使用 Langfuse 追蹤 Prompt
    #   # trace = self.langfuse.trace(name="essay-grading")
    #   prompt = f"你是一位專業英文老師。請修正語法錯誤，並給予建議：{content}"
      
    #   # response = self.model.generate_content(prompt)

    #   response = self.client.models.generate_content(
    #       model=self.model, 
    #       contents=prompt
    #   )
      
    #   # 這裡簡化處理，實際建議解析 JSON
    #   return {"feedback": response.text}

    def grade_essay(self, content: str):
        # 1. 抓取 Prompt (預設會抓 production label)
        langfuse_prompt = self.lf.get_prompt("essay-teacher-prompt")
        
        # 2. 編譯 Prompt (將 {{user_content}} 替換為實際內容)
        compiled_prompt = langfuse_prompt.compile(user_content=content)
        # response = self.model.generate_content(compiled_prompt)

        # 3. 呼叫 Gemini SDK
        response = self.client.models.generate_content(
            model=self.model, 
            contents=compiled_prompt
        )
        return {"feedback": response.text}
