```bash
aiq workflow create --workflow-dir examples/eccenca eccenca_agent_demo

aiq workflow reinstall eccenca_agent_demo


source .venv/bin/activate

eval `ssh-agent`
ssh-add ~/.ssh/id_rsa

uv pip install -e examples/eccenca/eccenca_agent_demo --verbose

source .venv/bin/activate
export $(cat .env_key | egrep -v "(^#.*|^$)" | xargs)

aiq run --config_file examples/eccenca/eccenca_agent_demo/src/eccenca_agent_demo/configs/config.yml --input "Hello?"

aiq serve --config_file=examples/eccenca/eccenca_agent_demo/src/eccenca_agent_demo/configs/config.yml

cd external/demo-eccenca-memory
npm run dev

uv pip install -e examples/eccenca/eccenca_agent_demo --verbose
cd examples/eccenca/eccenca_agent_demo/test
pytest
```