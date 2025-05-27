```bash
cd git/AgentIQ/

aiq workflow create --workflow-dir examples/eccenca wikidata_ontologist

aiq workflow reinstall wikidata_ontologist

source ~/git/AgentIQ/.venv/bin/activate
export $(cat .env_key | egrep -v "(^#.*|^$)" | xargs)

uv pip install -e examples/eccenca/wikidata_ontologist --verbose

aiq run --config_file examples/eccenca/wikidata_ontologist/src/wikidata_ontologist/configs/config.yml --input "I have a black cat."

aiq serve --config_file=examples/eccenca/wikidata_ontologist/src/wikidata_ontologist/configs/config.yml 
aiq serve --config_file=examples/eccenca/wikidata_ontologist/src/wikidata_ontologist/configs/config.yml --port 8001

aiq validate --config_file=examples/eccenca/wikidata_ontologist/src/wikidata_ontologist/configs/config.yml

uv pip install -e examples/eccenca/wikidata_ontologist --verbose
cd examples/eccenca/wikidata_ontologist/test
pytest
```