import requests
import os
from django.conf import settings


def summarize_with_groq(text: str, tone: str, length: str) -> str:
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        prompt = f"Give a {length}, {tone} summary of the following:\n\n{text}"

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful summarizer."},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.5,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error: {str(e)}"
