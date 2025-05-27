import logging
import requests

from wikidata_ontologist.client_sparql import ClientSPARQL

log = logging.getLogger(__name__)

class WikidataTools:

    @staticmethod
    def type_lookup(label: str, lang: str = "en"):
        response = requests.get(
            "https://www.wikidata.org/w/api.php",
            params={
                "action": "wbsearchentities",
                "language": lang,
                "format": "json",
                "search": label,
                "type": "item"
            }
        )
        return response.json().get("search", [])
    
    @staticmethod
    def property_lookup(label: str, lang: str = "en"):
        response = requests.get(
            "https://www.wikidata.org/w/api.php",
            params={
                "action": "wbsearchentities",
                "language": lang,
                "format": "json",
                "search": label,
                "type": "property"
            }
        )
        return response.json().get("search", [])

    @staticmethod
    def format_results(results):
        return "\n".join([
            f"{r['label']} → {r['concepturi']} ({r.get('description', '')})"
            for r in results
        ])
    
    @staticmethod
    def format_local_results(results):
        if not results or "results" not in results or "bindings" not in results["results"]:
            return "No results found."

        lines = []
        for binding in results["results"]["bindings"]:
            iri = binding.get("iri", {}).get("value", "")
            type_ = binding.get("type", {}).get("value", "")
            comment = binding.get("comment", {}).get("value", "")
            llm_comment = binding.get("llmComment", {}).get("value", "")
            combined_comment = f"{comment} | {llm_comment}" if comment and llm_comment else comment or llm_comment
            lines.append(f"{iri} → {type_} ({combined_comment})")
        return "\n".join(lines)
    
    @staticmethod
    def local_lookup(label: str, lang: str = "en", verbose:bool = False):
        log.info(f"Local lookup for label: {label} in lang: {lang}")


        # SPARQL query to match label in ontology graph
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX llm: <http://example.com/llm/>

        SELECT DISTINCT ?iri ?type ?comment ?llmComment WHERE {{
          GRAPH <http://example.com/REPLACE_BY_NAMED_GRAPH_FOR_THIS_SESSION/ontology> {{
            VALUES ?type {{ rdf:Property rdfs:Class }}
            ?iri a ?type ;
                 rdfs:label ?label .
            OPTIONAL {{ ?iri rdfs:comment ?comment . }}
            OPTIONAL {{ ?iri llm:comment ?llmComment . }}
            FILTER(LANG(?label) = "{lang}")
            FILTER(STR(?label) = "{label}")
          }}
        }}
        """

        clientSPARQL = ClientSPARQL()

        if clientSPARQL.named_graph is not None:
            query = query.replace("http://example.com/REPLACE_BY_NAMED_GRAPH_FOR_THIS_SESSION", clientSPARQL.named_graph)

        if verbose:
            log.info(f"query: {query}")

        try:
            clientSPARQL.refresh_token()
            results = clientSPARQL.execute_query(query)

            if verbose:
                log.info(f"SPARQL local lookup query:\n{query}")
                log.info(f"Query results: {results}")

            bindings = clientSPARQL.execute_query(query)

            if bindings is None or ClientSPARQL.len(bindings) == 0 :
                return "None"

            return bindings

        except Exception as e:
            log.error(f"SPARQL local lookup failed: {str(e)}")
            return f"Error: {str(e)}"

        finally:
            del clientSPARQL
    
    