import os
import importlib
import importlib.resources
import inspect
import logging
from pathlib import Path

import pytest
# from eccenca_memory.register import WebQueryToolConfig

from aiq.runtime.loader import load_workflow

from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../.env_key")

# # @pytest.mark.e2e
# async def test_workflow_eccenca_memory_current_date():

#     # package_name = inspect.getmodule(WebQueryToolConfig).__package__

#     config_file: Path = Path(TEST_DIR + "/../src/eccenca_memory/configs/config.yml")

#     async with load_workflow(config_file) as workflow:
#         # message = "I have a black cat."
#         message = "What is the current date?"
#         responseWaited = "current date"
#         logger.debug(f"Message:{message}")
#         async with workflow.run(message) as runner:

#             result = await runner.result(to_type=str)
#             logger.debug(f"Response:{result}")

#         assert responseWaited.lower() in result.lower()

async def test_simple():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_memory/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        # message = "I have a black cat."
        message = "I have a black cat."
        responseWaited = "is saved"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert responseWaited.lower() in result.lower()

async def test_workflow_eccenca_memory_sparql2text_complexe():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_memory/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        # message = "I have a black cat."
        message = "I have a black cat and I like the chocolat. What is the color of my cat?"
        responseWaited = "black"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert responseWaited.lower() in result.lower()


async def test2_fact():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_memory/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        # message = "I have a black cat."
        message = "My horse is white."
        responseWaited = "white"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert responseWaited.lower() in result.lower()

async def test2_question():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_memory/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        # message = "I have a black cat."
        message = "What is the color of my horse?"
        responseWaited = "white"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert responseWaited.lower() in result.lower()
