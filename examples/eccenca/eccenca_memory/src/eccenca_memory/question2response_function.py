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

class Question2ResponseConfig(FunctionBaseConfig, name="question2response"):
    """
    Simple tool that resolves a question in the input.
    """
    llm_name: LLMRef
    verbose: bool = False
    # programming_language: str = "Python"
    description: str = ("Simple tool that resolves a question in the input.")


@register_function(config_type=Question2ResponseConfig)
async def question2response_function(config: Question2ResponseConfig, builder: Builder):
    from langchain_core.prompts.chat import ChatPromptTemplate

    async def _inner(query: str) -> str:
        log.info('Running code generation tool2')
        querySPARQL = ClientOntologist().text2sparql(query)
        responseSPARQL = ""
        error = ""
        if config.verbose:
            log.info('Tool input was: %s\nTool output is: \n%s', query, querySPARQL)
        if querySPARQL is not None:
            clientSPARQL = ClientSPARQL()
            result= "" 
            
            try:
                clientSPARQL.refresh_token()
                # Read the fact via the question
                responseSPARQL = clientSPARQL.execute_query(querySPARQL)


                log.info(responseSPARQL)
                nbResult = ClientSPARQL.len(responseSPARQL)
                if nbResult == 0:
                    result= "I don't know."
                else:
                    result = ClientSPARQL.result(responseSPARQL)
                    # for i in range(0, nbResult-1):
                    #     result = responseSPARQL["results"]["bindings"][i]["result"]["value"] # type: ignore
                    #     result += f"'{responseSPARQL["results"]["bindings"][i]["result"]["value"]}' is the response in the named graph {responseSPARQL["results"]["bindings"][i]["graph"]["value"]}."
            except Exception as e:
                log.info(f"Error: {str(e)} ")
                
                error = str(e)
                result= f"""
                The query:
                ```sparql
                {querySPARQL}
                ```
                returns this error:
                ```
                {str(e)}
                ```
    """
            finally:
                del clientSPARQL
        else:
           result = "None"

        # Save the result in the golden dataset
        asyncio.run(Event.save_memory_event(query, querySPARQL, sparql_response=responseSPARQL, sparql_error=error))
        return result

    yield FunctionInfo.from_fn(_inner, description=config.description)

