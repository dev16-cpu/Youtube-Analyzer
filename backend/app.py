from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from analyzer import detect_genre, extract_keywords, format_duration
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="backend/.env")

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Check your .env file")

app = Flask(__name__)
CORS(app)

youtube = build('youtube', 'v3', developerKey=API_KEY)

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return None
@app.route("/")
def home():
    return "YouTube Analyzer API is running 🚀"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    url = data.get("url")

    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid URL"})

    request_api = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )

    response = request_api.execute()

    if len(response['items']) == 0:
        return jsonify({"error": "Video not found"})

    video = response['items'][0]

    title = video['snippet']['title']
    description = video['snippet']['description']
    raw_duration = video['contentDetails']['duration']

    duration = format_duration(raw_duration)

    text = title + " " + description

    genre = detect_genre(text)
    keywords = extract_keywords(text)

    return jsonify({
        "title": title,
        "genre": genre,
        "keywords": keywords,
        "duration": duration
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)