import requests
import json
from dotenv import load_dotenv
import os
import logging


load_dotenv()


class OpenRouterHandler:
    def __init__(self) -> None:
        self.url = os.getenv("OPEN_ROUTER_URL")
        self.api_key = os.getenv("OPEN_ROUTER_API_KEY")
        if self.url is None or self.api_key is None:
            raise Exception("Open routrer credentials not found")
        self.headers = {}
        self.headers["Authorization"] = f"Bearer {self.api_key}"
        self.headers["Content-Type"] = "application/json"

    def get_response(self, context, llm_model="openrouter/hunter-alpha"):
        if self.url is None or self.headers is None:
            raise Exception("Open routrer credentials not found")
        logging.debug("sending request to llm")
        response = requests.post(
            url=self.url,
            headers=self.headers,
            json={
                "model": llm_model,  # Optional
                "messages": [{"role": "user", "content": str(context)}],
            },
        )

        result = response.json()
        return result["choices"][0]["message"]["content"]
