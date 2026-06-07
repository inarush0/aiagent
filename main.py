import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("No Gemini API Key provided.")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="AI Agent")
    _ = parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    response = generate_content(client, messages)

    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata found.")

    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
    print("Response:")
    print(response.text)


def generate_content(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )


if __name__ == "__main__":
    main()
