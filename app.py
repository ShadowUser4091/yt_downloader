from flask import Flask, render_template, request
import yt_dlp
from settings import FEATURES, FAQS
import json

app = Flask(__name__)

def extract_format_data(format_data):
    extension = format_data["ext"]
    format_name = format_data["format"]
    url = format_data.get("url", "")
    return {
        "extension": extension,
        "format_name": format_name,
        "url": url
    }

def extract_video_data_from_url(url):
    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'noplaylist': True,
        'dumpjson': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_data = ydl.extract_info(url, download=False)
    
    title = video_data.get("title", "Unknown Title")
    thumbnail = video_data.get("thumbnail", "")
    formats = [extract_format_data(f) for f in video_data.get("formats", [])]
    
    return {
        "title": title,
        "formats": formats,
        "thumbnail": thumbnail
    }

@app.route("/")
def home():
    return render_template("index.html", features=FEATURES, faqs=FAQS)

@app.route("/download", methods=["POST"])
def download():
    video_url = request.form["video_url"]
    video_data = extract_video_data_from_url(video_url)
    return render_template("download.html", 
                           title=video_data["title"],
                           thumbnail=video_data["thumbnail"],
                           formats=video_data["formats"],
                           features=FEATURES,
                           faqs=FAQS)

if __name__ == "__main__":
    app.run()
