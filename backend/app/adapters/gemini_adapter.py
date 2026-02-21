# adapters/gemini_adapter.py (實作配接器)

import google.generativeai as genai
from langfuse import Langfuse
from app.ports.ai_service import AIServicePort

class GeminiAdapter(AIServicePort):
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.langfuse = Langfuse() # 初始化 Langfuse

    def grade_essay(self, content: str):
        # 使用 Langfuse 追蹤 Prompt
        trace = self.langfuse.trace(name="essay-grading")
        prompt = f"請批改這篇英文作文並給予評分(0-100)與建議：{content}"
        
        response = self.model.generate_content(prompt)
        
        # 這裡簡化處理，實際建議解析 JSON
        return {"feedback": response.text}