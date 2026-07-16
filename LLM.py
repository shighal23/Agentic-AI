import os
import sys
import traceback
from openai import OpenAI
import requests


def _log(msg: str) -> None:
    # Print to stderr so Streamlit captures it in logs without exposing secrets
    print(f"[LLM] {msg}", file=sys.stderr)


# Try to import config; if it fails (Config may raise on missing key),
# perform a masked diagnostic by reading env and Streamlit secrets directly.
try:
    from Config import API_KEY, BASE_URL, MODEL_NAME
    _from_config = True
except Exception as import_exc:
    _log("Config import failed — falling back to masked diagnostics.")
    # Attempt to read key from environment or Streamlit secrets without exposing it
    API_KEY = os.getenv("OPENAI_API_KEY") or ""
    try:
        import streamlit as _st
        if not API_KEY:
            API_KEY = _st.secrets.get("OPENAI_API_KEY") or ""
        BASE_URL = os.getenv("BASE_URL") or _st.secrets.get("BASE_URL") or ""
        MODEL_NAME = os.getenv("MODEL_NAME") or _st.secrets.get("MODEL_NAME") or ""
    except Exception:
        # Streamlit not available in this context; just use env-derived values
        BASE_URL = os.getenv("BASE_URL") or ""
        MODEL_NAME = os.getenv("MODEL_NAME") or ""
    _from_config = False


def _mask_diagnostics(key: str, base_url: str) -> None:
    present = bool(key)
    looks_like_openai = bool(key and key.startswith("sk-"))
    _log(f"Masked diagnostic — OPENAI_API_KEY present: {'Yes' if present else 'No'}; "
         f"Looks like OpenAI key: {'Yes' if looks_like_openai else 'No'}; "
         f"BASE_URL set: {'Yes' if base_url else 'No'}")


# Run masked diagnostics so it's visible in Streamlit logs without showing the key
_mask_diagnostics(API_KEY, BASE_URL)


def _auth_check(key: str, base_url: str) -> None:
    """Perform a single masked HTTP request to check authentication status.

    Logs only the HTTP status and a short, non-sensitive snippet of the response.
    Does not log the API key itself.
    """
    if not key:
        _log("Auth check skipped: no API key present.")
        return

    # Build endpoint — prefer explicit BASE_URL if provided, otherwise OpenAI
    if base_url:
        endpoint = base_url.rstrip("/")
        # If user provided a base like https://api.provider.com, append /v1/models
        if not endpoint.endswith("/v1/models"):
            endpoint = endpoint + "/v1/models"
    else:
        endpoint = "https://api.openai.com/v1/models"

    headers = {"Authorization": f"Bearer {key}"}
    try:
        resp = requests.get(endpoint, headers=headers, timeout=10)
        status = resp.status_code
        # Keep only a short snippet of the body for logs
        snippet = (resp.text or "").replace("\n", " ")[:400]
        _log(f"Auth check to {endpoint} returned status={status}; resp_snippet='{snippet}'")
    except Exception as e:
        _log(f"Auth check request failed: {e}")


# Run an auth check once at import to help debug deployed auth issues.
_auth_check(API_KEY, BASE_URL)


# Create OpenAI client (if no API key, client creation will likely fail downstream)
client = OpenAI(
    api_key=API_KEY or None,
    base_url=BASE_URL if BASE_URL else None,
)


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