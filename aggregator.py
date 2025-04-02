import requests
import time
import random
from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

API_ENDPOINTS = {
    "api-python": "http://api-python:5001/",
    "api-js": "http://api-js:5002/",
    "api-go": "http://api-go:5003/",
}

executor = ThreadPoolExecutor(max_workers=3)

def call_api(url):
    try:
        response = requests.get(url, timeout=2)
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": f"Failed to reach {url}"}

@app.route('/aggregate', methods=['GET'])
def aggregate():
    with executor:
        results = list(executor.map(call_api, API_ENDPOINTS.values()))
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
