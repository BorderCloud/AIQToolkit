import logging

from wikidata_ontologist.client_sparql import ClientSPARQL
from wikidata_ontologist.wikidata_api_tools import WikidataTools

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

log = logging.getLogger(__name__)

class LocalWikidataLookupConfig(FunctionBaseConfig, name="local_wikidata_lookup"):
    """
    Tool to search in the local ontology graph for a concept label, returning its IRI, type and description if available.
    """
    verbose: bool = False
    description: str = (
        "Lookup in the local ontology graph (<.../ontology>) for a concept label and language. "
        "Returns the concept IRI, rdf:type, rdfs:label, and rdfs:comment (if available)."
    )


@register_function(config_type=LocalWikidataLookupConfig)
async def local_wikidata_lookup(config: LocalWikidataLookupConfig, builder: Builder):
    async def _inner(label: str, lang: str) -> str:
        return WikidataTools.format_local_results(WikidataTools.local_lookup(label,lang,config.verbose))
    

    yield FunctionInfo.from_fn(_inner, description=config.description)
