import os
from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url, format="best"):
    ydl_opts = {
        "format": format,
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path
    except Exception as e:
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    format = data.get("format", "best")

    if not url:
        return jsonify({"error": "URL diperlukan"}), 400

    file_path = download_video(url, format)
    if file_path:
        return jsonify({"status": "success", "file_path": file_path})
    else:
        return jsonify({"error": "Gagal mengunduh video"}), 500

@app.route("/download_file/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)