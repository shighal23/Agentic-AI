from openai import OpenAI
import sys
import traceback
from Config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL if BASE_URL else None,
)

def _log(msg: str) -> None:
    # Print to stderr so Streamlit captures it in logs without exposing secrets
    print(f"[LLM] {msg}", file=sys.stderr)


def chat(messages: list) -> str:
    _log(f"Using BASE_URL={'<empty>' if not BASE_URL else BASE_URL}; MODEL={MODEL_NAME}")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Log the full traceback to stderr (will be available in Streamlit logs)
        _log("Exception while calling model provider:")
        traceback.print_exc(file=sys.stderr)

        # Provide a clearer error message to users while keeping logs for debugging
        err_text = str(e)
        if "Authentication" in err_text or "401" in err_text or "invalid" in err_text.lower():
            raise RuntimeError(
                "Authentication failed while calling the model provider.\n"
                "Please check:\n"
                " - Streamlit Secrets: OPENAI_API_KEY\n"
                " - That the key is valid for the selected provider\n"
                " - BASE_URL: leave blank for official OpenAI, or set your provider's URL.\n"
                "Full traceback has been logged for debugging."
            ) from e

        # If it's another error, raise a generic runtime error and keep traceback in logs
        raise RuntimeError("Model provider error occurred; see logs for details.") from e


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "say hello"}
    ]

    print(chat(messages))