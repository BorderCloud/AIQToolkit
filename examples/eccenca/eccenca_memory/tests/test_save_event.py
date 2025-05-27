import os
import pytest
from eccenca_memory.event import Event

import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../../.env_key")

def test_config_files_exist_and_readable():
    assert os.path.isfile(Event.CONFIG_ORCHESTRATOR_PATH), f"File did not find: {Event.CONFIG_ORCHESTRATOR_PATH}"
    assert os.access(Event.CONFIG_ORCHESTRATOR_PATH, os.R_OK), f"File not readable: {Event.CONFIG_ORCHESTRATOR_PATH}"

    assert os.path.isfile(Event.CONFIG_ONTOLOGIST_PATH), f"File did not find: {Event.CONFIG_ONTOLOGIST_PATH}"
    assert os.access(Event.CONFIG_ONTOLOGIST_PATH, os.R_OK), f"File not readable: {Event.CONFIG_ONTOLOGIST_PATH}"

    orchestrator_content = Event.load_config_file(Event.CONFIG_ORCHESTRATOR_PATH)
    ontologist_content = Event.load_config_file(Event.CONFIG_ONTOLOGIST_PATH)

    assert orchestrator_content.strip() != "", "configOrchestrator is empty."
    assert ontologist_content.strip() != "", "configOntologist is empty."

def test_generate_event_uri_format():
    """
    Vérifie que l'URI générée commence bien par l'URL de base et contient un timestamp transformé.
    """
    uri, timestamp = Event.generate_event_uri()
    assert uri.startswith(f"<{Event.BASE_EVENT_URI}")
    assert uri.endswith(">")

    # Vérifie que le timestamp est bien dans l'URI et formaté sans ":"
    safe_timestamp = timestamp.replace(":", "-").replace(".", "-")
    assert safe_timestamp in uri

@pytest.mark.asyncio
async def test_save_memory_event_real_call():
    """
    Test d'intégration : envoie un événement réel à un endpoint SPARQL (doit être configuré dans l'env).
    Ce test est ignoré par défaut.
    """
    response = await Event.save_memory_event(
        prompt_user="Quel est le capital de la France ?",
        sparql_generated="SELECT ?capital WHERE { wd:Q142 wdt:P36 ?capital . }",
        sparql_response="Paris"
    )

    logger.debug(response)
