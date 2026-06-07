import argparse
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No Gemini API Key provided.")

client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="AI Agent")
_ = parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

prompt: str = args.user_prompt

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

if response.usage_metadata is None:
    raise RuntimeError("No usage metadata found.")

prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count

print(f"User prompt: {prompt}")
print(f"Prompt tokens: {prompt_token_count}")
print(f"Response tokens: {candidates_token_count}")
print("Response:")
print(response.text)
