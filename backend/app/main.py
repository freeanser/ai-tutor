# backend/app/main.py

import os
from dotenv import load_dotenv

# 1. 必須在 import app.adapters 之前執行
load_dotenv()
# 2. 現在環境變數已經載入，可以安全地 import 了
from app.adapters.web_api import app as flask_app
from flask import Flask


if __name__ == "__main__":
    # 你可以從環境變數讀取配置
    port = int(os.environ.get("PORT", 5000))
    
    print(f"AI Tutor 後端已啟動，監聽埠口: {port}")
    
    # 啟動 Flask
    # debug=True 在開發階段非常有幫助，會自動重新載入代碼
    flask_app.run(host="0.0.0.0", port=port, debug=True)