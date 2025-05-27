```bash
aiq workflow create --workflow-dir examples/eccenca eccenca_memory

aiq workflow reinstall eccenca_memory

uv pip install -e examples/eccenca/eccenca_memory --verbose

source .venv/bin/activate
export $(cat .env_key | egrep -v "(^#.*|^$)" | xargs)

aiq run --config_file examples/eccenca/eccenca_memory/src/eccenca_memory/configs/config.yml --input "I have a black cat and I like the chocolate."
aiq run --config_file examples/eccenca/eccenca_memory/src/eccenca_memory/configs/config.yml --input "My horse is white."

aiq serve --config_file=examples/eccenca/eccenca_memory/src/eccenca_memory/configs/config.yml
aiq serve --config_file=examples/eccenca/eccenca_memory/src/eccenca_memory/configs/config.yml  --port 8002

aiq validate --config_file=examples/eccenca/eccenca_memory/src/eccenca_memory/configs/config.yml

uv pip install -e examples/eccenca/eccenca_memory --verbose
cd examples/eccenca/eccenca_memory/test
pytest
```