import os
import argparse

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No Gemini API key found!")

# Load a model from the api_key
client = genai.Client(api_key=api_key)

# Check for arguments in the main.py command
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

# Prompt the model
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=args.user_prompt
)

# Makes sure the usage_metadata exists
if response.usage_metadata is None:
    raise RuntimeError("The API response appears malformed, it probably failed!")

# Create variables of the prompt and response
prompt_count = response.usage_metadata.prompt_token_count
response_count = response.usage_metadata.candidates_token_count

# Print those variables
print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {prompt_count}")
print(f"Response tokens: {response_count}")
print(f"Response:\n{response.text}")
