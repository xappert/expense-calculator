from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Just say 'API connection successful'"}],
        max_tokens=20,
    )
    print("Validation successful:", response.choices[0].message.content)
except Exception as e:
    print("Validation failed:", str(e))
