import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    timeout=20,
)

completion_args = {
    "model": "openrouter/free",
    "messages": [],
    #     "max_tokens": 300,
}

filter_keys = ["role", "content", "tool_calls"]


def get_message_from_response(resp, filterkeys):
    message = dict(resp.choices[0].message)
    return {k: v for k, v in message.items() if k in filterkeys and v is not None}


# ANSI Color Codes
USER = "\033[32m"
ASSISTANT = "\033[34m"
RESET = "\033[0m"

while True:
    user_input = input(f"{USER}User: {RESET}")
    if user_input.lower() in ["exit", "quit"]:
        break
    completion_args["messages"].append({"role": "user", "content": user_input})

    llm_response = client.chat.completions.create(**completion_args)
    completion_args["messages"].append(
        get_message_from_response(llm_response, filter_keys)
    )

    print(f"{ASSISTANT}Assistant: {RESET}{completion_args['messages'][-1]['content']}")
