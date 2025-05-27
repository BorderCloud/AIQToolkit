import requests , json, re, os
from SPARQLWrapper import SPARQLWrapper, JSON

class ClientSPARQL:

    def __init__(self):
        self.eccenca_endpoint_read = os.getenv("ECCENCA_ENDPOINT_READ")
        self.eccenca_endpoint_write = os.getenv("ECCENCA_ENDPOINT_WRITE")
        self.eccenca_endpoint_token = os.getenv("ECCENCA_ENDPOINT_TOKEN")
        self.eccenca_oauth_user = os.getenv("ECCENCA_OAUTH_USER")
        self.eccenca_oauth_password = os.getenv("ECCENCA_OAUTH_PASSWORD")
        self.eccenca_oauth_password = os.getenv("ECCENCA_OAUTH_PASSWORD")
        self.named_graph = os.getenv("NAMED_GRAPH")

        ## TODO need to clean
        # replace johndo.eccenca.my by your sandbox
        self.endpointRead=self.eccenca_endpoint_read
        self.endpointWrite=self.eccenca_endpoint_write
        accessMethod="oauth2"
        # replace johndo.eccenca.my by your sandbox
        self.token_endpoint=self.eccenca_endpoint_token
        self.OAUTH_CLIENT_ID="cmemc"
        OAUTH_GRANT_TYPE="password"
        # replace johndo@example.com  by your email
        self.OAUTH_USER=self.eccenca_oauth_user
        # insert your password
        self.OAUTH_PASSWORD=self.eccenca_oauth_password

        self.token = None

        self.tempNamedGraph = 'http://example.com/REPLACE_BY_NAMED_GRAPH_FOR_THIS_SESSION'

    def refresh_token(self):
        token= ""
        accessData = {
            'grant_type': 'password',
            'client_id': self.OAUTH_CLIENT_ID,
            'username': self.OAUTH_USER,
            'password': self.OAUTH_PASSWORD
            }
        response = requests.post(self.token_endpoint, data=accessData) # type: ignore
        response_dict = json.loads(response.text)
        token = response_dict['access_token']
        self.token = token

    def execute_query(self, query, named_graph= None, token=None):
        queryWithNamedGraph = query

        newNamedGraph = str(named_graph if named_graph is not None else self.named_graph)

        if self.tempNamedGraph in query:
            queryWithNamedGraph = query.replace(self.tempNamedGraph, newNamedGraph)
        # else:
        #     regex = r"(.*WHERE {)(.*)(}.*)"
        #     subst = "\\1 GRAPH <"+newNamedGraph+"> { \\2 } \\3"
        #     queryWithNamedGraph = re.sub(regex, subst, query, 1, re.DOTALL)

        sparqlClient = SPARQLWrapper(self.endpointRead, agent='benchtext2sparql/0.1') # type: ignore
        if token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + token)
        elif self.token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + self.token)

        sparqlClient.setQuery(queryWithNamedGraph)
        sparqlClient.setReturnFormat(JSON)
        return sparqlClient.query().convert()

    def execute_update(self, query, named_graph=None, token=None):
        queryWithNamedGraph = query

        newNamedGraph = str(named_graph if named_graph is not None else self.named_graph)

        if self.tempNamedGraph in query:
            queryWithNamedGraph = query.replace(self.tempNamedGraph, newNamedGraph)
        # else:
        #     regex = r"(.*INSERT DATA {)(.*)(})"
        #     subst = "\\1 GRAPH <"+newNamedGraph+"> { \\2 } \\3"
        #     queryWithNamedGraph = re.sub(regex, subst, query, 1, re.DOTALL)

        sparqlClient = SPARQLWrapper(self.endpointRead,updateEndpoint = self.endpointWrite, agent='benchtext2sparql/0.1') # type: ignore
        sparqlClient.setMethod("POST")
        if token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + token)
        elif self.token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + self.token)

        sparqlClient.setQuery(queryWithNamedGraph)
        sparqlClient.setReturnFormat(JSON)
        return sparqlClient.query().convert()

    def execute_clear(self, named_graph, token=None):
        
        graph = str(named_graph if named_graph is not None else self.named_graph)
        queryWithNamedGraph = "CLEAR GRAPH <" + graph + ">"

        sparqlClient = SPARQLWrapper(self.endpointRead,updateEndpoint = self.endpointWrite, agent='benchtext2sparql/0.1') # type: ignore
        sparqlClient.setMethod("POST")
        if token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + token)
        elif self.token != None:
            sparqlClient.addCustomHttpHeader('Authorization', ' Bearer ' + self.token)

        sparqlClient.setQuery(queryWithNamedGraph)
        sparqlClient.setReturnFormat(JSON)
        return sparqlClient.query().convert()
    
    @staticmethod
    def len(responseSPARQL):
        return len(responseSPARQL["results"]["bindings"])
    
    @staticmethod
    def result(responseSPARQL):
        return f"'{responseSPARQL["results"]["bindings"][0]["result"]["value"]}' is the response in the named graph {responseSPARQL["results"]["bindings"][0]["graph"]["value"]}."
         