from eccenca_memory.client_sparql import ClientSPARQL
import pytest
import requests
from eccenca_memory.client_ontologist import ClientOntologist 

import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../../.env_key")


def test_execute_update(insertQuery):
    clientSPARQL = ClientSPARQL()
    clientSPARQL.refresh_token()
    clientSPARQL.execute_update(insertQuery)