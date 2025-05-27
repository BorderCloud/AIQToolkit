import asyncio

from aiq.plugins.eccenca.client_eccenca_memory import ClientEccencaMemory
from aiq.plugins.eccenca.cmem_memory_config import CMEMMemoryConfig
from aiq.memory.interfaces import MemoryEditor, MemoryItem

import logging

logger = logging.getLogger(__name__)

class CMEMMemoryEditor(MemoryEditor):

    def __init__(self, config: CMEMMemoryConfig):
        self._conn_url = config.connection_url

    async def add_items(self, items: list[MemoryItem]) -> None:
        # logger.info(f"CMEMMemoryEditor: add_items")
        # logger.info(items)

        client = ClientEccencaMemory()
    
        # Content of items:
        # [MemoryItem(conversation=[{'role': 'user', 'content': 'My dog is red'}], tags=['dog', 'color'], metadata={'context': 'user statement'}, user_id='12345', memory='My dog is red')]
        for memory_item in items:
            memory = memory_item.memory
            if memory is None:
                continue

            # logger.info("memory")
            # logger.info(memory)
            client.send(f"{memory}")

    async def search(self, query: str, top_k: int = 5, **kwargs) -> list[MemoryItem]:
        # logger.info(f"CMEMMemoryEditor: search")
        # logger.info("query")
        # logger.info(query)
        # logger.info("top_k")
        # logger.info(top_k)
        # logger.info("kwargs")
        # logger.info(kwargs)
        
        # TODO: adapt the prompt according to the orchestrator. ? is probably not enough to explicit a research.
        response = ClientEccencaMemory().send(f"{query}?")
        
        # logger.info("response")
        # logger.info(response)

        user_id = kwargs.pop("user_id")  # Ensure user ID is in keyword arguments

        # Construct MemoryItem instances
        memories = []
        memories.append(
            MemoryItem(conversation=[{"text": response}],
                        user_id=user_id,
                        memory=None,
                        tags=[],
                        metadata={}))

        # logger.info("memories")
        # logger.info(memories)

        return memories

    async def remove_items(self, **kwargs):
        # NOT IMPLEMENTED
        logger.info(f"CMEMMemoryEditor:remove_items:NOT IMPLEMENTED")
        # logger.debug("kwargs")
        # logger.debug(kwargs)
        return