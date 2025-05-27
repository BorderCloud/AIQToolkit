import requests
import json

class ClientEccencaMemory:

    def __init__(self):
        self.endpoint = "http://localhost:8002"

    def send(self, message: str):
        url = f"{self.endpoint}/generate"
        headers = {"Content-Type": "application/json"}

        try:
            payload = {"input_message": message}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Throw error if HTTP != 200
        except requests.exceptions.RequestException as e:
            return f"ClientEccencaMemory Error: {e}"

        try:
            data = response.json()
            raw_response = data.get("value", "")
        except (ValueError, KeyError) as e:
            return f"ClientEccencaMemory JSON Error : {e}"

        return raw_response
