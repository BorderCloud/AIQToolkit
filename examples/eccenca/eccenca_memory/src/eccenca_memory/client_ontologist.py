import re
import requests
import json

class ClientOntologist:

    def __init__(self):
        self.endpoint = "http://localhost:8001"

    def text2sparql(self, message: str):
        url = f"{self.endpoint}/generate"
        headers = {"Content-Type": "application/json"}

        try:
            payload = {"input_message": message}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Throw error if HTTP != 200
        except requests.exceptions.RequestException as e:
            return f"Erreur de requête : {e}"

        try:
            data = response.json()
            raw_response = data["value"]
            match = re.search(r"```sparql\s+(.*?)```", raw_response, re.DOTALL)

            if match:
                sparql_query = match.group(1).strip()
            else:
                return None 

            return sparql_query
        except (ValueError, KeyError) as e:
            return f"Erreur lors du traitement de la réponse JSON : {e}"
