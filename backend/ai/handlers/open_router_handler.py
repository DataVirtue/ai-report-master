import requests
from dotenv import load_dotenv
import os
import logging


load_dotenv()


class OpenRouterHandler:
    def __init__(self) -> None:
        self.url = os.getenv("OPEN_ROUTER_URL")
        self.embedding_url = os.getenv("OPEN_ROUTER_EMBEDDINGS_URL")
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
        
        if "error" in result:
            raise Exception(str(result["error"]))

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
            
        raise Exception(f"Unexpected LLM response: {result}")

    def get_response_with_message_list(
        self,
        messages,
        llm_model="openrouter/hunter-alpha",
        return_json=False,
        tools=None,
    ):
        if self.url is None or self.headers is None:
            raise Exception("Open routrer credentials not found")
        logging.debug("sending request to llm")
        response = requests.post(
            url=self.url,
            headers=self.headers,
            json={
                "model": llm_model,  # Optional
                "messages": messages,
                **({"response_format": {"type": "json_object"}} if return_json else {}),
                **({"tools": tools} if tools else {}),
            },
        )

        result = response.json()
        print(result)

        if "error" in result:
            raise Exception(result["error"])

        if "choices" in result:
            return result["choices"][0]["message"]

        # fallback (some providers use different format)
        if "output" in result:
            return result["output"]

        raise Exception(f"Unexpected LLM response: {result}")

    def get_embeddings(
        self,
        input,
        llm_model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
        embedding_dimension=1532,
    ):
        if self.embedding_url is None or self.api_key is None:
            raise Exception("Open routrer credentials not found")

        data_input = input if isinstance(input, list) else [input]

        data = {"model": llm_model, "input": data_input}
        if "openai" in llm_model:
            data["dimensions"] = embedding_dimension
        res = requests.post(self.embedding_url, headers=self.headers, json=data)
        logging.debug(res)
        payload = res.json()
        logging.debug(type(res.json()["data"][0]["embedding"][0]))

        embeddings = [item["embedding"] for item in payload["data"]]
        return embeddings
