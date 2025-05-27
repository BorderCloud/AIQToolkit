from wikidata_ontologist.wikidata_api_tools import WikidataTools
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

class WikidataTypeLookupConfig(FunctionBaseConfig, name="wikidata_type_lookup"):
    description: str = ("Finds the Wikidata IRI for a concept (entity/type)")

@register_function(config_type=WikidataTypeLookupConfig)
async def wikidata_type_lookup(config: WikidataTypeLookupConfig, builder):
    async def _inner(label: str, lang: str) -> str:
        # Appel à Wikidata ou implémentation maison ici
        return WikidataTools.format_results(WikidataTools.type_lookup(label,lang))
    yield FunctionInfo.from_fn(_inner, description=config.description)
