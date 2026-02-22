# backend/app/adapters/web_api.py (Flask 入口)

from flask import Flask, request, jsonify
from app.adapters.gemini_adapter import GeminiAdapter

app = Flask(__name__)

# 初始化時不傳入字串，讓 Adapter 自己去抓環境變數
ai_service = GeminiAdapter() 

@app.route('/api/grade', methods=['POST'])
def grade():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Missing content"}), 400
    result = ai_service.grade_essay(data['content'])
    return jsonify(result)