from groq import Groq
import os

client = Groq(api_key=os.getenv("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"))

def generate_quiz(topic):
    prompt = f"""
Create 3 explanatory questions with bullet-point answers based on:
{topic}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
