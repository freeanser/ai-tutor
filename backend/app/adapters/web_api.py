# adapters/web_api.py (Flask 入口)

from flask import Flask, request, jsonify
from app.adapters.gemini_adapter import GeminiAdapter

app = Flask(__name__)
# 依賴注入：將 Adapter 注入到 Service 中
ai_service = GeminiAdapter(api_key="YOUR_GEMINI_API_KEY")

@app.route('/api/grade', methods=['POST'])
def grade():
    data = request.json
    result = ai_service.grade_essay(data['content'])
    return jsonify(result)