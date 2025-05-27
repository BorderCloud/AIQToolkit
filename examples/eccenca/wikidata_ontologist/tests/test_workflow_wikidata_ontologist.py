import os
import importlib
import importlib.resources
import inspect
import logging
from pathlib import Path

import pytest
# from wikidata_ontologist.register import WebQueryToolConfig

from aiq.runtime.loader import load_workflow

from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../../.env_key")

async def test_simple():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/wikidata_ontologist/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        # message = "I have a black cat."
        message = "I have a black cat."
        responseWaited = "is saved"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert responseWaited.lower() in result.lower()
