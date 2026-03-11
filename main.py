import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No Gemini API key found!")

# Load a model from the api_key
client = genai.Client(api_key=api_key)

# Prompt the model
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

# Makes sure the usage_metadata exists
if response.usage_metadata is None:
    raise RuntimeError("The API response appears malformed...")

# Create variables of the prompt and response
prompt_count = response.usage_metadata.prompt_token_count
response_count = response.usage_metadata.candidates_token_count

# Print those variables
print(f"User prompt: {prompt}")
print(f"Prompt tokens: {prompt_count}")
print(f"Response tokens: {response_count}")
print(f"Response:\n{response.text}")
