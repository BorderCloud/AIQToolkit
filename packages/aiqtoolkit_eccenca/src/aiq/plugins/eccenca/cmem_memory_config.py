from aiq.builder.builder import Builder
from aiq.cli.register_workflow import register_memory
from aiq.data_models.memory import MemoryBaseConfig


class CMEMMemoryConfig(MemoryBaseConfig, name="eccenca_memory"):
    connection_url: str


@register_memory(config_type=CMEMMemoryConfig)
async def cmem_memory_client(config: CMEMMemoryConfig, builder: Builder):

    from aiq.plugins.eccenca.cmem_editor import CMEMMemoryEditor

    memory_editor = CMEMMemoryEditor(config=config)

    yield memory_editor
