import asyncio
import logging

from eccenca_memory.client_ontologist import ClientOntologist
from eccenca_memory.event import Event

from aiq.builder.builder import Builder
from aiq.builder.framework_enum import LLMFrameworkEnum
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.component_ref import LLMRef
from aiq.data_models.function import FunctionBaseConfig

from eccenca_memory.client_sparql import ClientSPARQL

log = logging.getLogger(__name__)

class Fact2GraphConfig(FunctionBaseConfig, name="fact2graph"):
    """
    Simple tool that saves the fact of the input in a graph.
    """
    llm_name: LLMRef
    verbose: bool = False
    # programming_language: str = "Python"
    description: str = ("Simple tool that saves the fact of the input in a graph.")


@register_function(config_type=Fact2GraphConfig)
async def fact2graph_function(config: Fact2GraphConfig, builder: Builder):
    from langchain_core.prompts.chat import ChatPromptTemplate

    log.info('Initializing code generation tool\nGetting tool LLM from config')

    async def _inner(query: str) -> str:
        log.info('Running code generation tool')
        log.info(query)
        response = ClientOntologist().text2sparql(query)
        responseSparql = ""
        insertQuery = ""
        error = ""
        if response is not None:
            clientSPARQL = ClientSPARQL()
            result= "The fact is saved." 
            if clientSPARQL.named_graph is not None:
                insertQuery = response.replace("http://example.com/REPLACE_BY_NAMED_GRAPH_FOR_THIS_SESSION", clientSPARQL.named_graph)
                # if config.verbose:
                log.info(insertQuery)
                try:
                    clientSPARQL.refresh_token()
                    # Save the fact
                    responseSparql = clientSPARQL.execute_update(insertQuery)

                except Exception as e:
                    log.info(f"Error: {str(e)} ")
                    
                    error=str(e)
                    result= f"""
The fact is not saved.
The query:
```sparql
{insertQuery}
```
returns this error:
```
{str(e)}
```    """

                finally:
                    del clientSPARQL
            else:
                log.info(f"Query is not saved. The variable NAMED_GRAPH is not initialized in the env.")
        else:
           result = "None"


        # Save the result in the golden dataset
        asyncio.run(Event.save_memory_event(query, insertQuery,sparql_response=responseSparql, sparql_error=error))

        return result

    yield FunctionInfo.from_fn(_inner, description=config.description)
