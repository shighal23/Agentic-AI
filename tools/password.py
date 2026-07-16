import random
import string

def execute(arguments: dict):
    length = arguments.get("length", 8)

    try:
        length = int(length)

        characters = string.ascii_letters + string.digits + "!@#$%&*"

        password = "".join(random.choice(characters) for _ in range(length))

        return f"Generated Password: {password}"

    except Exception as e:
        return f"Password Error: {e}"


if __name__ == "__main__":
    print(execute({"length": 12}))