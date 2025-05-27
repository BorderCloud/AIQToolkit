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

@pytest.mark.parametrize("insertQuery", [
    (
        """PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX ns: <http://example.org/ns#>
INSERT DATA
{ GRAPH <http://example.com/text2sparqlTEST1> { <http://example/book1>  ns:price  42 } }"""),
       ("""
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX instance: <http://example.com/instance/>
PREFIX llm: <http://example.com/llm/>
PREFIX user: <http://example.com/user/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Insert the fact that the user has a black cat
INSERT DATA {
  GRAPH <http://example.com/text2sparqlTEST1> {
    instance:myCat wdt:P31 wd:Q146 ;         # myCat is an instance of house cat
                    wdt:P462 wd:Q23445 ;     # myCat has color black
                    wdt:P127 instance:theUser . # myCat is owned by the user

    # Optionally, define the user entity for clarity
    instance:theUser a user:Person ;
      rdfs:label "The user who made this statement" ;
      llm:comment "This entity represents the user who claims to own a black cat." .
  }
}
""")

])
def test_execute_update(insertQuery):
    clientSPARQL = ClientSPARQL()
    clientSPARQL.refresh_token()
    clientSPARQL.execute_update(insertQuery)


@pytest.mark.parametrize("response", [
    ({'head': {'vars': ['result', 'graph']}, 'results': {'bindings': [{'result': {'type': 'literal', 'xml:lang': 'en', 'value': 'white'}, 'graph': {'type': 'uri', 'value': 'http://example.com/text2sparqlTEST1'}}]}})
])
def test_result(response):
    logger.debug(ClientSPARQL.len(response))
    logger.debug(ClientSPARQL.result(response))
    assert ClientSPARQL.len(response) == 1
    assert ClientSPARQL.result(response) == "'white' is the response in the named graph http://example.com/text2sparqlTEST1."

