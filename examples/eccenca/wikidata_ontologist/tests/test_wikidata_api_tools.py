from wikidata_ontologist.wikidata_api_tools import WikidataTools
import pytest

import logging


from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../../.env_key")

logger = logging.getLogger(__name__)

def test_search_entities():
    try:
        result = WikidataTools.type_lookup("animal","en")
        logger.debug(f"Result wikidata_type_lookup('animal'): {result}")
    except ValueError:
        assert False

def test_search_properties():
    try:
        result = WikidataTools.property_lookup("instance of","en")
        logger.debug(f"Result wikidata_property_lookup('instance of'):{result}")
    except ValueError:
        assert False

def test_format():
    try:
        result = WikidataTools.format_results(WikidataTools.property_lookup("instance of","en"))
        logger.debug(f"Result :{result}")
    except ValueError:
        assert False


def test_local_lookup1():
    try:
        result = WikidataTools.format_local_results(WikidataTools.local_lookup("cat","en",True))
        logger.debug(f"Result local_lookup('cat'): {result}")
    except ValueError:
        assert False
def test_local_lookup2():
    try:
        result = WikidataTools.format_local_results(WikidataTools.local_lookup("black","en",True))
        logger.debug(f"Result local_lookup('black'): {result}")
    except ValueError:
        assert False


def test_search_gpt1():
    try:
        result = WikidataTools.type_lookup("GPT1","en")
        logger.debug(f"Result wikidata_type_lookup('GPT1'): {result}")
    except ValueError:
        assert False

def test_search_local_gpt1():
    try:
        result = WikidataTools.format_local_results(WikidataTools.local_lookup("GPT1","en",True))
        logger.debug(f"Result local_lookup('GPT1'): {result}")
    except ValueError:
        assert False