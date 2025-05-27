```bash
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa

source .venv/bin/activate
uv pip install -e packages/agentiq_eccenca --verbose
```