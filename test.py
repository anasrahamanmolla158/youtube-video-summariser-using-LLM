import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available models for your API key:")
for m in genai.list_models():
    print(m.name)
