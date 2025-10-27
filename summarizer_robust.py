import requests
import textstat
import os

# Use your Hugging Face API token (store safely)
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HF_TOKEN = os.getenv("HF_TOKEN")  # safer: use environment variable
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def summarize_text(text, max_words=130):
    if not text.strip():
        return {"error": "⚠️ Empty text provided!"}

    payload = {
        "inputs": text,
        "parameters": {"max_length": max_words},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            summary = data[0]["summary_text"]
        else:
            return {"error": "Unexpected response from API."}

        return {
            "summary": summary,
            "original_length": len(text.split()),
            "summary_length": len(summary.split()),
            "readability": round(textstat.flesch_reading_ease(summary), 2)
        }

    except Exception as e:
        return {"error": str(e)}
