import requests
import json
import os

# Get the API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("API key not set. Please set OPENROUTER_API_KEY environment variable.")

# Set the request payload
payload = {
    "model": "tngtech/deepseek-r1t2-chimera:free",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
}

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    #each message is appended to message payload which is sent to maintain history
    payload["messages"].append({"role": "user", "content": user_input})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print("Chimera:", reply)
        payload["messages"].append({"role": "assistant", "content": reply})
    else:
        print("Error:", response.status_code)
        print(response.text)

