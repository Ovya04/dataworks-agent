from flask import Flask, request, jsonify
import os
import json
import sqlite3
import requests
import markdown
import openai
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from git import Repo
from pydub import AudioSegment

app = Flask(__name__)

# API Key for AI Proxy
OPENAI_API_KEY = os.getenv("AIPROXY_TOKEN")

@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task')

    if not task:
        return jsonify({"error": "Task description required"}), 400

    try:
        result = execute_task(task)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')

    if not path.startswith("data/"):
        return jsonify({"error": "Access restricted to /data/"}), 403

    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    with open(path, 'r') as f:
        content = f.read()
    
    return jsonify({"content": content}), 200

def execute_task(task):
    if "fetch API data" in task:
        return fetch_api_data()
    elif "clone git repo" in task:
        return clone_git_repo()
    elif "execute SQL query" in task:
        return execute_sql_query(task)
    elif "scrape website" in task:
        return scrape_website()
    elif "resize image" in task:
        return resize_image()
    elif "transcribe audio" in task:
        return transcribe_audio()
    else:
        return "Task not recognized"

def fetch_api_data():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return response.json()

def clone_git_repo():
    repo_url = "https://github.com/your-username/sample-repo.git"
    Repo.clone_from(repo_url, "data/cloned-repo")
    return "Repository cloned."

def execute_sql_query(task):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    query = task.replace("execute SQL query ", "")
    cursor.execute(query)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def scrape_website():
    url = "https://example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.title.string

def resize_image():
    img = Image.open("data/sample.jpg")
    img_resized = img.resize((100, 100))
    img_resized.save("data/resized.jpg")
    return "Image resized."

def transcribe_audio():
    audio = AudioSegment.from_file("data/audio.mp3")
    audio.export("data/audio.wav", format="wav")
    return "Audio transcribed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
