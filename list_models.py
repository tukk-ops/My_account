import urllib.request
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode("utf-8"))
        models = [m["name"] for m in result.get("models", [])]
        for m in models:
            print(m)
except Exception as e:
    print(e)
