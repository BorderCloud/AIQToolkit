import pytest
import requests
from eccenca_memory.client_ontologist import ClientOntologist 

import logging

@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog):
    yield
    errors = [record for record in caplog.get_records('call') if record.levelno >= logging.ERROR]
    assert not errors

@pytest.mark.parametrize("message, expected_key", [
    # ("Hello", "None"),  # ajuster selon le workflow réel
    # ("De quel couleur est mon chat ?", "SELECT"),  # ajuster selon le workflow réel
    # ("J'ai un chat noir.", "INSERT"),  # ajuster selon le workflow réel
    ("The user's dog's name is Bob.", "INSERT"),  # ajuster selon le workflow réel
])
def test_local_workflow(message, expected_key):

    data = ClientOntologist().text2sparql(message)

    # assert any(expected_key in value for value in data.values()), f"Expected key '{expected_key}' not found in response: {data}"
    # print("Response data:", data)
