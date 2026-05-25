import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

def test_llm():
    print("Sending request to Groq...")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello! How are you.",
            }
        ],
       model="llama-3.3-70b-versatile", 
    )
    
    print("\nResponse from Agent:")
    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    test_llm()