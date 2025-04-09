from openai import OpenAI
import os

# Initialize client with API key from .env
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_generation():
    """Generate text from a prompt"""
    response = client.responses.create(
        model="gpt-4o",
        input="Write a one-sentence bedtime story about a unicorn."
    )
    print("\nText Generation:")
    print(response.output_text)

def image_analysis():
    """Analyze image content"""
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "user", "content": "What two teams are playing in this photo?"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                    }
                ]
            }
        ]
    )
    print("\nImage Analysis:")
    print(response.output_text)

def web_search():
    """Use web search tool"""
    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input="What was a positive news story from today?"
    )
    print("\nWeb Search:")
    print(response.output_text)

def streaming():
    """Stream server-sent events"""
    stream = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": "Say 'double bubble bath' ten times fast.",
            },
        ],
        stream=True,
    )
    print("\nStreaming:")
    for event in stream:
        print(event)

if __name__ == "__main__":
    text_generation()
    image_analysis()
    web_search()
    streaming()
