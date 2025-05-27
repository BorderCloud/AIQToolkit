import os
import logging
from pathlib import Path
import pytest

from aiq.runtime.loader import load_workflow
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=TEST_DIR + "/../../../../.env_key")

async def test_workflow_eccenca_agent_demo():

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_agent_demo/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        message = "What is the color of my cat ?"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert "black" in result.lower()


async def test2_workflow_eccenca_agent_demo():

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_agent_demo/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        message = "My horse is white."
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")
        
async def test3_workflow_eccenca_agent_demo():

    # package_name = inspect.getmodule(WebQueryToolConfig).__package__

    config_file: Path = Path(TEST_DIR + "/../src/eccenca_agent_demo/configs/config.yml")

    async with load_workflow(config_file) as workflow:
        message = "What is the color of my horse ?"
        logger.debug(f"Message:{message}")
        async with workflow.run(message) as runner:

            result = await runner.result(to_type=str)
            logger.debug(f"Response:{result}")

        assert "white" in result.lower()