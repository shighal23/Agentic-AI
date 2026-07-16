import os

API_KEY = os.getenv("OPENAI_API_KEY", "NU7ntP7psr76QcHeWODG0DPBxdDwb5jF")

BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")