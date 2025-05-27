<!--
SPDX-FileCopyrightText: Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

![NVIDIA Agent Intelligence Toolkit](https://media.githubusercontent.com/media/NVIDIA/AIQToolkit/refs/heads/main/docs/source/_static/aiqtoolkit_banner.png "AIQ toolkit banner image")

# NVIDIA Agent Intelligence Toolkit Subpackage
This is a subpackage for eccenca memory integration in AIQ toolkit.

For more information about AIQ toolkit, please visit the [AIQ toolkit package](https://pypi.org/project/aiqtoolkit/).

For testing the eccenca solution, please visit the [eccenca sandbox](https://eccenca.my/).

# How to install this package?
```
uv pip install -e '.[eccenca]'
```

# How to use this package in your AIQ workflow?

This package implement only the followed functions:
-

Example of config file with this package:
```yaml
general:
  use_uvloop: true
  logging:
    console:
      _type: console
      level: DEBUG
  front_end:
    _type: fastapi

memory:
  knowledge_graph:
    _type: eccenca_memory
    # Not implemented but necessary for the interfaces 
    # TODO: add parameters to support security of the private memory
    connection_url: "http://localhost:8002"
    
functions:
  current_datetime:
    _type: current_datetime
  add_memory:
    _type: add_memory
    memory: knowledge_graph
    description: |
      Add  information shared during the conversation by the user. Only consider information about the user if it is explicitly stated by them. 
      The input to this tool should be a string that describes the shared information by the user, not the question or answer.
  get_memory:
    _type: get_memory
    memory: knowledge_graph
    description: |
      Call this tool only if the user ask you a question.
      Use the same question that the user asked you with exactly the same syntax.

llms:
  nim_llm:
    _type: nim
    model_name: meta/llama-3.1-70b-instruct
    temperature: 0.0
    max_tokens: 1024

workflow:
  _type: react_agent
  tool_names: 
      - current_datetime
      - add_memory
      - get_memory
  llm_name: nim_llm
  verbose: true
  retry_parsing_errors: true
  max_retries: 3
```