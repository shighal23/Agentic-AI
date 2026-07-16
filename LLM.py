from openai import OpenAI
from Config import API_KEY, BASE_URL, MODEL_NAME

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL if BASE_URL else None,
)

def chat(messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Provide a clearer error when authentication fails so deployment logs
        # point the developer to secrets / BASE_URL issues.
        err_text = str(e)
        if "Authentication" in err_text or "401" in err_text or "invalid" in err_text.lower():
            raise RuntimeError(
                "Authentication failed while calling the model provider.\n"
                "Check that `OPENAI_API_KEY` is set in Streamlit Secrets (or environment),\n"
                "and that `BASE_URL` is correct for your provider.\n"
                "If you are using OpenAI, set `BASE_URL` to 'https://api.openai.com/v1' or leave it empty."
            ) from e

        # Re-raise the original exception for other errors
        raise


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "say hello"}
    ]

    print(chat(messages))