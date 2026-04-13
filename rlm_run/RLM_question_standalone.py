import os

from dotenv import load_dotenv

from rlm import RLM
from rlm.logger import RLMLogger

load_dotenv()


def sanitize_for_cp1252(text):
    # Remove characters that CP1252 cannot encode
    return text.encode("cp1252", errors="ignore").decode("cp1252")


logger = RLMLogger(log_dir="./logs")

rlm = RLM(
    backend="azure_openai",  # "openai" or "portkey", etc.
    backend_kwargs={
        "model_name": "gpt-4o-2-gb",
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    environment="local",
    environment_kwargs={},
    max_depth=1,
    logger=logger,
    verbose=True,  # For printing to console with rich, disabled by default.
)

with open("example.txt", "r", encoding="utf-8") as f:
    user_input = f.read()
#print(user_input[:100])

# Sanitize before sending to RLM
user_input = sanitize_for_cp1252(user_input)

result = rlm.completion(user_input)
#print(result)
print("==================================="*10)
print(result.response)