from wikidata_ontologist.wikidata_api_tools import WikidataTools
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

class WikidataPropertyLookupConfig(FunctionBaseConfig, name="wikidata_property_lookup"):
    description: str = ("Finds the Wikidata IRI for a property (predicate/qualifier).")

@register_function(config_type=WikidataPropertyLookupConfig)
async def wikidata_type_lookup(config: WikidataPropertyLookupConfig, builder):
    async def _inner(label: str, lang: str) -> str:
        # Appel à Wikidata ou implémentation maison ici
        return WikidataTools.format_results(WikidataTools.property_lookup(label,lang))
    yield FunctionInfo.from_fn(_inner, description=config.description)
