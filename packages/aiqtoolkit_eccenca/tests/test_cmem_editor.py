from unittest.mock import AsyncMock

import pytest
# from cmem import AsyncMemoryClient

from aiq.memory.models import MemoryItem
from aiq.plugins.eccenca.cmem_editor import CMEMMemoryEditor

import logging

@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog):
    yield
    errors = [record for record in caplog.get_records('call') if record.levelno >= logging.ERROR]
    assert not errors

@pytest.fixture(name="mock_cmem_memory_config")
def mock_cmem_client_fixture() -> AsyncMock:
    """Fixture to provide a mocked AsyncMemoryClient."""
    return AsyncMock()


@pytest.fixture(name="cmem_editor")
def cmem_editor_fixture(mock_cmem_memory_config: AsyncMock):
    """Fixture to provide an instance of CMEMMemoryEditor with a mocked client."""
    return CMEMMemoryEditor(config=mock_cmem_memory_config)


@pytest.fixture(name="sample_memory_item")
def sample_memory_item_fixture():
    """Fixture to provide a sample MemoryItem."""

    conversation = [
        {
            "role": "user",
            "content": "My dog has the name Bob.",
        }
    ]

    return MemoryItem(conversation=conversation,
                      user_id="user123",
                      memory="The user's dog's name is Bob.",
                      metadata={},
                      tags=[]
                    #   metadata={"key1": "value1"},
                    #   tags=["tag1", "tag2"]
                      )

@pytest.fixture(name="sample_memory_item2")
def sample_memory_item_fixture2():
    """Fixture to provide a sample MemoryItem."""
#  {"conversation": [{"role": "user", "content": "J'ai aussi un chat."}], "tags": [], "metadata": {}, "user_id": "user123", "memory": "The user has a cat."}
    conversation = [
        {
            "role": "user",
            "content": "J'ai aussi un chat.",
        }
    ]

    return MemoryItem(conversation=conversation,
                      user_id="user123",
                      memory="The user has a cat.",
                      metadata={},
                      tags=[]
                    #   metadata={"key1": "value1"},
                    #   tags=["tag1", "tag2"]
                      )


async def test_add_item1(cmem_editor: CMEMMemoryEditor,
                                #  , mock_cmem_client: AsyncMock, 
                                sample_memory_item: MemoryItem
                                 ):
   items= [sample_memory_item]
   
   await cmem_editor.add_items(items)

async def test_add_item2(cmem_editor: CMEMMemoryEditor,
                                #  , mock_cmem_client: AsyncMock, 
                                sample_memory_item2: MemoryItem
                                 ):
   items= [sample_memory_item2]
   
   await cmem_editor.add_items(items)

async def test_search_success(cmem_editor: CMEMMemoryEditor
                            #   , mock_cmem_client: AsyncMock
                              ):
    result = await cmem_editor.search(query="test query", user_id="user123", top_k=1)


async def test_remove_items_by_memory_id(cmem_editor: CMEMMemoryEditor
                                        #  , mock_cmem_client: AsyncMock
                                         ):
    """Test removing items by memory ID."""
    await cmem_editor.remove_items(memory_id="memory123")

    # mock_cmem_client.delete.assert_called_once_with("memory123")


async def test_remove_items_by_user_id(cmem_editor: CMEMMemoryEditor
                                    #    , mock_cmem_client: AsyncMock
                                       ):
    """Test removing all items for a specific user ID."""
    await cmem_editor.remove_items(user_id="user123")

    # mock_cmem_client.delete_all.assert_called_once_with(user_id="user123")


async def test_remove_items_missing_arguments(cmem_editor: CMEMMemoryEditor):
    """Test removing items with missing required arguments."""
    result = await cmem_editor.remove_items()

    assert result is None
