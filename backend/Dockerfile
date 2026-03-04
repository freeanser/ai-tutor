# 作用： 宣告「基底映像檔 (Base Image)」。
# 白話文：這行程式碼告訴 Docker 使用 Python 3.11 的版本，且作業系統是超輕量級 Slim Linux 的乾淨環境作為基礎映像檔，這樣我們就可以在這個環境中安裝我們的應用程式所需的依賴項。
FROM python:3.11-slim

# 作用： 設定工作目錄。
# 白話文：這行程式碼告訴 Docker 在容器內部建立一個名為 /app 的目錄，並將其設置為工作目錄。這意味著接下來的指令（如安裝依賴項和複製應用程式代碼）都將在這個目錄下執行。
WORKDIR /app

# 先「單獨」複製環境依賴定義檔
# 這是為了利用 Docker 快取！只要 requirements.txt 沒變，就不會重新執行下一步的安裝
COPY requirements.txt .

# 作用： 安裝 Python 依賴項。
# 白話文：這行程式碼使用 pip 安裝 requirements.txt 文件中列出的所有 Python 依賴項。這些依賴項是我們的應用程式運行所需的庫和模組，安裝完成後我們的應用程式就可以正常運行了。
# 使用 --no-cache-dir 不保留下載的安裝包，縮小鏡像體積
RUN pip install --no-cache-dir -r requirements.txt

# 作用： 複製檔案到容器內部。
# 白話文：這行程式碼將當前目錄下的所有檔案（包括子目錄）複製到容器內部的 /app 目錄中。這樣我們的應用程式代碼和相關檔案就會被放置在容器內部的工作目錄中，準備進行後續的安裝和執行。
COPY . .

# 明確告訴 Flask 你的主程式在哪裡
# 如果你的檔案是 app 資料夾下的 main.py，就寫 app.main
# 如果你的檔案是 app 資料夾下的 __init__.py，通常寫 app 即可
ENV FLASK_APP=app.main

# 作用： 定義容器啟動時執行的命令。
# 白話文：這行程式碼告訴 Docker 當容器啟動時要執行的命令。在這裡，我們要啟動 Flask，所以我們使用 flask run 命令來啟動 Flask 應用程式。
# --host=0.0.0.0 讓 Flask 接受來自外部的連線請求。確保外部（你的實體電腦）可以連進這個容器的 Web Server。
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "-m", "app.main"]

# 在 backend 資料夾下，新增一個名為 .dockerignore 的檔案（就跟 .gitignore 的概念一樣）。在裡面寫入 .env 之類的內容（不希望被打包進 Image 的東西。）

# 在 backend 資料夾下，執行以下指令來建構 Docker 映像檔：
# docker build -t ai-tutor-backend .
# -t：是 --tag 的縮寫。意思是「我要幫這個做好的 Image 貼上一個標籤（命名）」。

# 在 backend 資料夾下，執行以下指令來啟動 Docker 容器：
# docker run -p 5001:5001 --env-file .env ai-tutor-backend
# 啟動並「注入」 .env 檔案
# 把外面的 .env 檔案讀取進去當作環境變數，讓容器內部的應用程式可以使用這些環境變數。
# -p：是 --publish 的縮寫。意思是「我要把這個容器內部的 5000 埠口，對外開放到我的實體電腦的 5000 埠口」。
# --env-file：是用來指定一個環境變數檔案的。這樣 Docker 就會從這個檔案中讀取環境變數，並將它們設置在容器內部，讓你的應用程式可以使用這些環境變數。