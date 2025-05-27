import os
import datetime
from eccenca_memory.client_sparql import ClientSPARQL
from pathlib import Path

import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class Event:
    BASE_EVENT_URI = "https://example.com/events/"
    CONFIG_ORCHESTRATOR_PATH = os.path.abspath(Path(__file__).parent /  "configs/config.yml")
    CONFIG_ONTOLOGIST_PATH = os.path.abspath(Path(__file__).parent /  "../../../wikidata_ontologist/src/wikidata_ontologist/configs/config.yml")

    @staticmethod
    def load_config_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def generate_event_uri():
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        safe_timestamp = timestamp.replace(":", "-").replace(".", "-")
        return f"<{Event.BASE_EVENT_URI}{safe_timestamp}>", timestamp
    
    @staticmethod
    def check(text):
        result =  str(text).replace("'''", "\\'\\'\\'").replace('"""', '\\"\\"\\"')
        return result

    @staticmethod
    async def save_memory_event(prompt_user, sparql_generated, sparql_response=None, sparql_error=None):
        config_orchestrator = Event.load_config_file(Event.CONFIG_ORCHESTRATOR_PATH)
        config_ontologist = Event.load_config_file(Event.CONFIG_ONTOLOGIST_PATH)

        event_uri, timestamp = Event.generate_event_uri()

        update_query = f"""
        PREFIX aiq: <https://eccenca.com/research/agentic/aiq#>
        INSERT DATA {{
          GRAPH <http://example.com/REPLACE_BY_NAMED_GRAPH_FOR_THIS_SESSION/goldendataset_demo> {{
            {event_uri} a aiq:MemoryEvent ;
              aiq:promptUser \"\"\"{Event.check(prompt_user)}\"\"\" ;
              aiq:configAgentOrchestrator \"\"\"{Event.check(config_orchestrator)}\"\"\" ;
              aiq:configAgentOntologist \"\"\"{Event.check(config_ontologist)}\"\"\" ;
              aiq:sparqlGenerated \"\"\"{Event.check(sparql_generated)}\"\"\" ;
              aiq:generatedAtTime "{timestamp}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
        """

        if sparql_response:
            update_query += f'{event_uri} aiq:sparqlResponse \"\"\"{Event.check(sparql_response)}\"\"\" .\n'
        if sparql_error:
            update_query += f'{event_uri} aiq:sparqlError \"\"\"{Event.check(sparql_error)}\"\"\" .\n'

        update_query += "    }\n  }"
        
        # logger.info(update_query)
        clientSPARQL = ClientSPARQL()
        clientSPARQL.refresh_token()
        return clientSPARQL.execute_update(update_query)

