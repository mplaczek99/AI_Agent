import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Load environment variables from .env
    load_dotenv()

    # Retrieve the Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No Gemini API key found!")

    # Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # Create the message list to send to the model
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Generate the response from the model
    generate_content(client, messages, args.user_prompt, args.verbose)


def generate_content(client, messages, user_prompt, verbose):
    # Send the prompt to the Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
        ),
    )

    # Verify the response contains usage metadata
    if response.usage_metadata is None:
        raise RuntimeError("The API response appears malformed, it probably failed!")

    # Extract token usage information
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    # Print additional debugging information if verbose mode is enabled
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    # Print the model's response
    print(f"Response:\n{response.text}")


# Run the program
if __name__ == "__main__":
    main()
