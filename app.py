import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# جلب البيانات من البيئة (Render Environment Variables)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def trigger_build():
    data = request.get_json()
    desc = data.get('description')
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/worker.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "ref": "main",
        "inputs": {"app_description": desc}
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        return jsonify({"message": "✅ بدأ المصنع بالعمل! سيتم إرسال رابط التحميل لبريدك المرتبط بـ GitHub فور الجاهزية."})
    else:
        return jsonify({"message": f"❌ خطأ في السيرفر: {response.status_code}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
