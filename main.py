import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="Prompt to send to Gemini",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    # Load environment variables from .env (for API key)
    load_dotenv()

    # Retrieve the Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No Gemini API key found. Set GEMINI_API_KEY first.")

    # Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # Create the initial message list with the user's prompt
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    # Start the generation process
    generate_content(client, messages, args.user_prompt, args.verbose)


def is_quota_exhausted_error(error):
    # Gemini quota errors can arrive as structured status data or only as text.
    status = (error.status or "").upper()
    message = (error.message or "").lower()
    details = str(getattr(error, "details", "")).lower()

    if status == "RESOURCE_EXHAUSTED":
        return True

    return "quota" in message or "quota" in details


def generate_content(client, messages, user_prompt, verbose):
    # Send the current conversation to Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
    except errors.ClientError as error:
        if is_quota_exhausted_error(error):
            # Print a clean CLI error when the account is out of quota.
            print(
                "Gemini API quota is exhausted. Check billing/quota limits or "
                "wait for your usage window to reset.",
                file=sys.stderr,
            )
            if verbose and error.message:
                print(f"Gemini details: {error.message}", file=sys.stderr)
            raise SystemExit(1)
        raise RuntimeError(f"Gemini API request failed: {error}") from error

    # Ensure the response is valid
    if response.usage_metadata is None:
        raise RuntimeError(
            "The API response appears malformed, it probably failed!"
        )

    # Extract token usage for debugging/monitoring
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    # This will store the tool results we send back to the model later
    function_response_parts = []

    # Check if the model requested any function calls
    if response.function_calls is not None:
        for function_call in response.function_calls:
            # Execute the requested function using our dispatcher
            function_call_result = call_function(function_call, verbose)

            # Validate that the function returned a proper Content object
            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts.")

            # Extract the FunctionResponse object from the first part
            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError(
                    "Function call result did not include a function response."
                )

            # Ensure the function actually returned data
            if function_response.response is None:
                raise RuntimeError(
                    "Function response did not include a response payload."
                )

            # Store this part so we can send it back to Gemini later
            function_response_parts.append(function_call_result.parts[0])

            # Optional debug output showing what the function returned
            if verbose:
                print(f"-> {function_response.response}")

    # Print the model's text response (may be None if only function calls were returned)
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
