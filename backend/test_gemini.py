# # backend/test_gemini.py

# import os
# from google.genai import Client
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# client = Client(api_key=api_key)

# # print("--- 檢查可用模型列表 ---")
# # try:
# #     for m in client.models.list():
# #         print(f"可用模型: {m.name}")
# # except Exception as e:
# #     print(f"無法列出模型: {e}")

# print("\n--- 嘗試發送請求 ---")
# essay_content = "I goes to school everyday and I feels happy."
# prompt = f"你是一位專業英文老師。請修正語法錯誤並給予鼓勵：{essay_content}"

# # 1. 嘗試你清單中的 gemini-flash-latest (這通常對應 1.5 Flash)
# try:
#     print("正在連線至 gemini-flash-latest...")
#     response = client.models.generate_content(
#         model="gemini-flash-latest", 
#         contents=prompt
#     )
#     print("成功！AI 回覆：", response.text)
# except Exception as e:
#     print(f"Flash Latest 失敗：{e}")

# # 2. 嘗試你清單中更高級的 gemini-2.5-flash
# try:
#     print("\n正在連線至 Gemini 2.5 Flash...")
#     response = client.models.generate_content(
#         model="gemini-2.5-flash", 
#         contents=prompt
#     )
#     print("成功！AI 回覆：", response.text)
# except Exception as e:
#     print(f"2.5 Flash 失敗：{e}")

import os
import pytest
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

def test_gemini_grading_logic():

    api_key = os.getenv("GEMINI_API_KEY")
    client = Client(api_key=api_key)
    if not api_key:
        pytest.skip("跳過測試：未設定 GEMINI_API_KEY")

    # 關鍵：強制指定使用 v1 版本，避免 SDK 亂跑去 v1beta
    # client = Client(
    #     api_key=api_key,
    #     http_options={'api_version': 'v1'}
    # )
    
    essay_content = "I goes to school everyday."
    prompt = f"你是一位專業英文老師。請修正語法錯誤：{essay_content}"

    try:
        # 使用最標準的名稱
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt
        )
        
        assert response.text is not None
        # 只要 AI 有回覆且長度大於 0 就算連線成功
        assert len(response.text) > 0
        
    except Exception as e:
        pytest.fail(f"連線依舊失敗。錯誤詳情：{e}")
