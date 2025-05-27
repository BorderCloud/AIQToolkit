import {
  IconRefresh,
  IconEraser,
  IconTrash,
  IconBug,
  IconRobot,
} from '@tabler/icons-react';
import React, { useEffect, useState, useRef } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';

import { CodeBlock } from '@/components/Markdown/CodeBlock';

import { Network } from 'vis-network/standalone/umd/vis-network.min';

export const Memorybar = () => {
  const NAMED_GRAPH = 'http://example.com/text2sparqlTEST1';
  const [isMemoryDialogOpen, setIsMemoryDialog] = useState(false);
  const [chatLog, setChatLog] = useState([]);
  const [input, setInput] = useState('');
  const [activeProject, setActiveProject] = useState('all');
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [events, setEvents] = useState([]);
  const [highlightedTriples, setHighlightedTriples] = useState([]);
  const [promptMessage, setPromptMessage] = useState('');
  const [language, setLanguage] = useState('en');
  const networkRef = useRef(null);

  // function SparqlViewer({ query }) {
  //   return (
  //     <div className="codeblock relative font-sans text-[16px]">
  //     <div className="flex items-center justify-between py-1.5 px-4">
  //       <span className="text-xs lowercase text-white">{language}</span>

  //       <div className="flex items-center">
  //         <button
  //           className="flex gap-1.5 items-center rounded bg-none p-1 text-xs text-white"
  //           onClick={(e) => copyToClipboard(e)}
  //         >
  //           {isCopied ? <IconCheck size={18} /> : <IconClipboard size={18} />}
  //           {isCopied ? t('Copied!') : t('Copy code')}
  //         </button>
  //         <button
  //           className="flex items-center rounded bg-none p-1 text-xs text-white"
  //           onClick={(e) => downloadAsFile(e)}
  //         >
  //           <IconDownload size={18} />
  //         </button>
  //       </div>
  //     </div>
  //     <SyntaxHighlighter language="sparql" style={oneDark} customStyle={{ borderRadius: '0.5rem', fontSize: '0.85rem' }}
  //       wrapLongLines={true} // Ensures long lines wrap instead of forcing width expansion
  //     >
  //       {query}
  //     </SyntaxHighlighter>
  //   </div>
  //   );
  // }

  function SparqlResultViewer({ result }) {
    return (
      <SyntaxHighlighter
        language="json"
        style={oneDark}
        customStyle={{ borderRadius: '0.5rem', fontSize: '0.85rem' }}
      >
        {JSON.stringify(result, null, 2)}
      </SyntaxHighlighter>
    );
  }

  function YamlViewer({ yaml }) {
    return (
      <SyntaxHighlighter
        language="yaml"
        style={oneDark}
        customStyle={{ borderRadius: '0.5rem', fontSize: '0.85rem' }}
      >
        {yaml}
      </SyntaxHighlighter>
    );
  }

  let token: String | undefined;
  async function getToken() {
    if (!token) {
      const responseToken = await fetch('/api/cmem/token', {
        method: 'POST',
      });
      const data = await responseToken.json();
      return data.access_token;
    }
    return token;
  }

  const clearGraph = async () => {
    const response = await fetch('/api/cmem/clear', {
      method: 'POST',
      body: new URLSearchParams({
        token: await getToken(),
      }),
    });
    fetchGraph();
    fetchMemoryEvents();
  };

  const fetchGraph = async () => {
    const query = `
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  SELECT DISTINCT 
      ?subject (GROUP_CONCAT(DISTINCT ?subjectLabel ; separator="\\n") as ?subjectLabels) 
      ?predicate (GROUP_CONCAT(DISTINCT ?predicateLabel ; separator="\\n") as ?predicateLabels)
      ?object (GROUP_CONCAT(DISTINCT ?objectLabel ; separator="\\n") as ?objectLabels)
  FROM NAMED <${NAMED_GRAPH}>
  FROM <${NAMED_GRAPH}>
  FROM <${NAMED_GRAPH}/ontology>
  WHERE {
          GRAPH <${NAMED_GRAPH}> {
            ?subject ?predicate ?object .
          FILTER ( ?predicate != rdfs:label )
          }
   
        OPTIONAL {
            ?subject rdfs:label ?subjectLabel .
        }
        OPTIONAL {
            ?predicate rdfs:label ?predicateLabel .
        }
        OPTIONAL {
            ?object rdfs:label ?objectRdfsLabel .
        }
  
      BIND(
          IF(isLiteral(?object), 
             STR(?object), 
             ?objectRdfsLabel
          ) AS ?objectLabel
        )
  }
  GROUP BY ?subject ?predicate ?object
  #order by ?subject ?subjectLabels ?predicate ?predicateLabels ?object ?objectLabels
      `;

    const response = await fetch('/api/cmem/sparql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/sparql-query' },
      body: new URLSearchParams({
        token: await getToken(),
        query: query,
      }),
    });

    const json = await response.json();
    // const nodes = new Set();
    // const edges = [];

    // json.results.bindings.forEach(({ subjectLabel, predicateLabel, objectLabel }) => {
    //   nodes.add(subjectLabel.value);
    //   nodes.add(objectLabel.value);
    //   edges.push({
    //     from: subjectLabel.value,
    //     to: objectLabel.value,
    //     label: predicateLabel.value,
    //     id: `${subjectLabel.value}->${predicateLabel.value}->${objectLabel.value}`,
    //   });
    // });

    // setGraphData({
    //   nodes: Array.from(nodes).map((id) => ({ id, label: id })),
    //   edges,
    // });

    const nodesMap = new Map();
    const edges = [];

    json.results.bindings.forEach(
      ({
        subject,
        subjectLabels,
        predicate,
        predicateLabels,
        object,
        objectLabels,
      }) => {
        if (!nodesMap.has(subject.value)) {
          nodesMap.set(subject.value, {
            id: subject.value,
            label: subjectLabels ? subjectLabels.value : subject.value,
            title: subject.value,
          });
        }

        const objectValue = object['xml:lang']
          ? `${object.value}@${object['xml:lang']}`
          : object.value;
        if (!nodesMap.has(objectValue)) {
          if (object.type == 'literal') {
            nodesMap.set(objectValue, {
              id: objectValue,
              label: objectValue,
              shape: 'box',
              color: 'white',
              title: objectValue,
            });
          } else {
            nodesMap.set(objectValue, {
              id: objectValue,
              label: objectLabels ? objectLabels.value : object.value,
              title: object.value,
            });
          }
        }

        edges.push({
          from: subject.value,
          to: objectValue,
          label:
            predicateLabels && predicateLabels.value != ''
              ? predicateLabels.value
              : predicate.value ==
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
              ? 'a'
              : predicate.value,
          id: `${subject.value}->${predicate.value}->${objectValue}`,
          title: predicate.value,
        });
      },
    );

    setGraphData({
      nodes: Array.from(nodesMap.values()),
      edges,
    });
  };

  const fetchMemoryEvents = async () => {
    const query = `
        PREFIX aiq: <https://eccenca.com/research/agentic/aiq#>
        SELECT ?event ?timestamp ?promptUser ?configOrchestrator ?configOntologist ?sparqlGenerated ?sparqlResponse ?sparqlError
        WHERE {
          GRAPH <${NAMED_GRAPH}/goldendataset_demo> {
            ?event a aiq:MemoryEvent ;
                  aiq:promptUser ?promptUser ;
                  aiq:configAgentOrchestrator ?configOrchestrator ;
                  aiq:configAgentOntologist ?configOntologist ;
                  aiq:sparqlGenerated ?sparqlGenerated ;
                  aiq:generatedAtTime ?timestamp 
                  .
            OPTIONAL {
              ?event aiq:sparqlResponse ?sparqlResponse .
            }
            OPTIONAL {
              ?event aiq:sparqlError ?sparqlError. 
            }
          }
        }
        ORDER BY ASC(?timestamp)
      `;

    const response = await fetch('/api/cmem/sparql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/sparql-query' },
      body: new URLSearchParams({
        token: await getToken(),
        query: query,
      }),
    });

    const json = await response.json();

    const eventList = json.results.bindings.map((b) => ({
      event: b.event.value,
      id: b.event.value,
      time: b.timestamp.value,
      promptUser: b.promptUser.value,
      configOrchestrator: b.configOrchestrator.value,
      configOntologist: b.configOntologist.value,
      sparqlGenerated: b.sparqlGenerated.value,
      sparqlResponse: b.sparqlResponse ? b.sparqlResponse.value : 'no response',
      sparqlError: b.sparqlError ? b.sparqlError.value : 'no error',
      summary: b.sparqlError ? 'ERROR' : 'no error',
      expected: '',
    }));
    setEvents(eventList);
  };

  // const fetchEventTriples = async (eventURI) => {
  //   const query = `
  //     PREFIX aiq: <http://example.org/aiq#>
  //     PREFIX prov: <http://www.w3.org/ns/prov#>
  //     SELECT ?subject ?predicate ?object
  //     WHERE {
  //       GRAPH <${NAMED_GRAPH}> {
  //         <${eventURI}> a aiq:MemoryEvent ;
  //                       aiq:introducedTriple [
  //                         rdf:subject ?subject ;
  //                         rdf:predicate ?predicate ;
  //                         rdf:object ?object
  //                       ] .
  //       }
  //     }
  //   `;

  //   const response = await fetch('/api/cmem/sparql', {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/sparql-query' },
  //     body: new URLSearchParams({
  //       token: await getToken(),
  //       query: query,
  //     }),
  //   });

  //   const json = await response.json();
  //   const nodes = new Set();
  //   const edges = [];
  //   const highlightIds = [];

  //   json.results.bindings.forEach(({ subject, predicate, object }) => {
  //     nodes.add(subject.value);
  //     nodes.add(object.value);
  //     const edgeId = `${subject.value}->${predicate.value}->${object.value}`;
  //     edges.push({
  //       from: subject.value,
  //       to: object.value,
  //       label: predicate.value,
  //       id: edgeId,
  //     });
  //     highlightIds.push(edgeId);
  //   });

  //   setGraphData({
  //     nodes: Array.from(nodes).map((id) => ({ id, label: id })),
  //     edges,
  //   });
  //   setHighlightedTriples(highlightIds);
  // };

  const openSandbox = async (eventURI) => {};

  const clearHighlights = () => {
    setHighlightedTriples([]);
    fetchGraph();
  };

  const refreshGraph = async () => {
    fetchGraph();
    fetchMemoryEvents();
  };

  useEffect(() => {
    fetchGraph();
    fetchMemoryEvents();
  }, []);

  useEffect(() => {
    const container = document.getElementById('memory-graph');
    if (container && graphData.nodes) {
      const network = new Network(container, graphData, {
        edges: {
          color: {
            color: '#848484',
            highlight: '#ff0000',
          },
          arrows: {
            to: {
              enabled: true,
              type: 'arrow', // ou 'triangle', 'bar', etc.
            },
          },
          // smooth: {
          //   enabled: true,
          //   type: 'cubicBezier',
          //   roundness: 0.4,
          // },
        },
        nodes: {
          shape: 'dot',
          size: 16,
        },
        interaction: {
          hover: true,
          tooltipDelay: 50,
        },
        physics: {
          enabled: true,
        },
      });

      networkRef.current = network;

      network.on('oncontext', function (params) {
        params.event.preventDefault();
        const pointer = params.pointer.DOM;
        const nodeId = network.getNodeAt(pointer);
        const edgeId = network.getEdgeAt(pointer);
        let id = nodeId || edgeId;
        if (id) {
          const label =
            graphData.nodes.find((n) => n.id === id)?.label ||
            graphData.edges.find((e) => e.id === id)?.label;
          const shape =
            graphData.nodes.find((n) => n.id === id)?.shape ||
            graphData.edges.find((e) => e.id === id)?.shape;
          const title =
            graphData.nodes.find((n) => n.id === id)?.title ||
            graphData.edges.find((e) => e.id === id)?.title;

          const menu = document.createElement('div');
          menu.style.position = 'absolute';
          const containerRect = container.getBoundingClientRect();
          menu.style.top = `${pointer.y + containerRect.top}px`;
          menu.style.left = `${pointer.x + containerRect.left}px`;

          menu.style.background = '#fff';
          menu.style.border = '1px solid #ccc';
          menu.style.padding = '6px';
          menu.style.zIndex = '1000';

          //copy iri
          const itemMenu = document.createElement('div');
          itemMenu.innerText = `Copy`;
          itemMenu.style.cursor = 'pointer';
          itemMenu.onclick = () => {
            navigator.clipboard.writeText(title);
            document.body.removeChild(menu);
          };
          menu.appendChild(itemMenu);

          if (shape != 'box' && !title.includes('example.com')) {
            const url = title;
            const itemMenu = document.createElement('div');
            itemMenu.innerText = `🔗 What is it?`;
            itemMenu.style.cursor = 'pointer';
            itemMenu.onclick = () => {
              window.open(url, '_blank');
              document.body.removeChild(menu);
            };
            menu.appendChild(itemMenu);
          }

          document.body.appendChild(menu);
          document.addEventListener(
            'click',
            () => {
              if (document.body.contains(menu)) {
                document.body.removeChild(menu);
              }
            },
            { once: true },
          );
        }
      });

      if (highlightedTriples.length > 0) {
        const updateEdges = graphData.edges.map((edge) => ({
          ...edge,
          color: highlightedTriples.includes(edge.id) ? '#ff0000' : '#848484',
          width: highlightedTriples.includes(edge.id) ? 3 : 1,
        }));
        network.setData({ nodes: graphData.nodes, edges: updateEdges });
      }
    }
  }, [graphData, highlightedTriples]);

  const classesButton =
    'flex items-center justify-center bg-neutral-100 dark:bg-zinc-700 border border-neutral-300 dark:border-zinc-600 rounded p-1 text-[12px] shadow transition duration-300';

  const classesDetails =
    'm-2 bg-neutral-100 dark:bg-zinc-700 shadow border border-neutral-300 dark:border-zinc-600 rounded-lg p-2 transition-[max-height,opacity,scale] duration-500 ease-in-out overflow-auto opacity-100 h-auto scale-100';

  const deleteEvent = async (eventId) => {
    const response = await fetch('/api/cmem/deleteEvent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ eventId, token: await getToken() }),
    });

    if (response.ok) {
      setEvents((prev) => prev.filter((event) => event.id !== eventId));
    } else {
      console.error('Failed to delete event:', await response.text());
    }
  };

  const openChatGPT = async (eventId) => {
    const event = events.find((e) => e.id === eventId);

    //     const basePrompt = `
    // Contexte :
    // Tu es un agent expert en systèmes d'IA multi-agents, SPARQL, triplestore, et en orchestration LLM avec le framework Agent AIQ de NVIDIA.
    // Un LLM a généré une requête SPARQL et un autre l’a exécutée. Cette requête a produit un résultat inattendu ou incorrect.
    // Ta tâche est d’identifier l’origine du problème et de proposer une version corrigée de la requête.

    // 1. Configuration de l'agent exécutant (Executor LLM)
    // \`\`\`yaml
    // ${event.configOrchestrator}
    // \`\`\`

    // 2. Configuration de l'agent générateur (SPARQL Builder LLM)
    // \`\`\`yaml
    // ${event.configOntologist}
    // \`\`\`

    // 3. Requête SPARQL générée
    // \`\`\`sparql
    // ${event.sparqlGenerated}
    // \`\`\`

    // 4. Résultat de la requête (output brut ou formaté)
    // \`\`\`json
    // ${JSON.stringify(event.sparqlResponse, null, 2)}
    // \`\`\`

    // 5. Ce que l'utilisateur attendait comme résultat ou requête au vue du graphe de connaissances existant en mémoire :
    // \`\`\`
    // ${event.expected || "(non précisé)"}
    // \`\`\`

    // Tâches à réaliser :
    // 1. Analyse le contexte technique et les configurations des deux LLM.
    // 2. Compare le résultat obtenu avec ce qu’on pourrait attendre logiquement selon la structure de la requête.
    // 3. Identifie précisément les erreurs (sémantiques, syntaxiques, ou de logique métier).
    // 4. Propose une ou plusieurs versions corrigées de la configuration des LLM avec si nécessaire un exemple d'implémentation des nouveaux outils à fournir aux LLM
    // `
    const basePrompt = `
Context:
You are an expert agent in multi-agent AI systems, SPARQL, triplestore, and LLM orchestration with NVIDIA's Agent AIQ framework.
An LLM generated a SPARQL query and another executed it. This query produced an unexpected or incorrect result.
Your task is to identify the source of the problem.
1. Executor agent configuration (LLM Executor)
\`\`\`yaml
${event.configOrchestrator}
\`\`\`
2. Generator agent configuration (LLM SPARQL Builder)
\`\`\`yaml
${event.configOntologist}
\`\`\`
3. Generated SPARQL query
\`\`\`sparql
${event.sparqlGenerated}
\`\`\`
4. Query result (raw or formatted output)
\`\`\`json
${JSON.stringify(event.sparqlResponse, null, 2)}
\`\`\`
5. Query error:
\`\`\`json
${JSON.stringify(event.sparqlError, null, 2)}
\`\`\`
6. What the user expected as a result or query based on the existing knowledge graph in memory:
\`\`\`
${event.expected || '(not specified)'}
\`\`\`
Tasks to be performed:
1. Analyze the technical context and configurations of the two LLM.
2. Compare the result obtained with what could be logically expected based on the structure of the query.
3. Identify the errors precisely (semantic, syntactic, or business logic errors).
4. Propose one or more corrected versions of the LLM configuration with, if necessary, an example of implementation of the new tools to be provided to the LLMs.
`;
    setPromptMessage(basePrompt);
    setIsMemoryDialog(true);
  };

  //   const [expectedMap, setExpectedMap] = useState({});

  // const handleExpectedChange = useCallback((id, value) => {
  //   setExpectedMap((prev) => ({ ...prev, [id]: value }));
  // }, []);

  return (
    <div className="flex flex-1 text-gray-800 dark:text-white">
      <div className="w-full">
        <div className="flex items-center">
          <div className="ml-auto flex gap-2">
            <button
              className={classesButton}
              onClick={refreshGraph}
              aria-label="refresh"
            >
              <IconRefresh className="text-black dark:text-white" size={18} />
            </button>
            <button
              className={classesButton}
              onClick={clearGraph}
              aria-label="clean"
            >
              <IconEraser className="text-black dark:text-white" size={18} />
            </button>
          </div>
        </div>

        <h2 className="mt-[25px] text-lg font-semibold text-center">
          Your memory
        </h2>
        <div id="memory-graph" className="h-[calc(100vh-400px)]"></div>

        <h2 className="mt-[25px] text-lg font-semibold text-center">
          Memory replay
        </h2>

        <ul className="mx-auto p-2">
          {events.reverse().map((e) => (
            <li key={e.id}>
              {' '}
              <div className="flex items-center">
                <span>
                  {new Date(e.time).toLocaleString()} — {e.promptUser}
                </span>
                <div className="ml-auto flex gap-2">
                  <button
                    title="Delete"
                    className={classesButton}
                    onClick={() => deleteEvent(e.id)}
                  >
                    <IconTrash className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <details className={classesDetails}>
                <summary>{e.summary}</summary>

                <div className="flex items-center">
                  <span>
                    <strong>SPARQL query:</strong>
                  </span>
                  <div className="ml-auto flex gap-2">
                    <div className="ml-auto flex gap-2">
                      {/* <button title="Debug" className={classesButton} onClick={() => openSandbox(e.id)}>
                      <IconBug className="w-4 h-4" />
                    </button> */}
                    </div>
                  </div>
                </div>
                <div className="bg-black rounded">
                  <CodeBlock
                    key={Math.random()}
                    language="sparql"
                    value={e.sparqlGenerated}
                  />
                </div>

                <strong>SPARQL response:</strong>
                <div className="bg-black rounded">
                  <CodeBlock
                    key={Math.random()}
                    language="json"
                    value={e.sparqlResponse}
                  />
                </div>

                <strong>SPARQL error:</strong>
                <div className="bg-black rounded">
                  <CodeBlock
                    key={Math.random()}
                    language="bash"
                    value={e.sparqlError}
                  />
                </div>

                <div className="mt-2">
                  <label
                    htmlFor={`expected-${e.id}`}
                    className="block font-medium mb-1"
                  >
                    <div className="flex items-center">
                      <span>What you expected as query or result:</span>
                      <div className="ml-auto flex gap-2">
                        <button
                          title="Ask ChatGPT"
                          className={classesButton}
                          onClick={() => {
                            const eventsN = events.map((event) => {
                              if (event.id === `${e.id}`) {
                                event.expected = document.getElementById(
                                  `expected-${e.id}`,
                                ).value;
                              }
                              return event;
                            });
                            setEvents(eventsN);
                            openChatGPT(e.id);
                          }}
                        >
                          <IconRobot className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </label>
                  <textarea
                    id={`expected-${e.id}`}
                    className="w-full p-2 border rounded bg-white dark:bg-gray-800 dark:text-white"
                    rows={3}
                    // value={expectedMap[e.id] || ""}
                    // onChange={(e) => handleExpectedChange(e.id, e.target.value)}
                    placeholder="Describe here the intention or the expected result or SPARQL query..."
                  />
                </div>

                <details className={classesDetails}>
                  <summary>Ontologist configuration</summary>
                  <div className="bg-black rounded">
                    <CodeBlock
                      key={Math.random()}
                      language="bash"
                      value={e.configOntologist}
                    />
                  </div>
                </details>
                <details className={classesDetails}>
                  <summary>Orchestrator configuration</summary>
                  <div className="bg-black rounded">
                    <CodeBlock
                      key={Math.random()}
                      language="bash"
                      value={e.configOrchestrator}
                    />
                  </div>
                </details>
              </details>
            </li>
          ))}
        </ul>

        {isMemoryDialogOpen && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white dark:bg-zinc-800 text-black dark:text-white rounded-lg p-4 w-[500px]">
              <h3 className="text-lg font-semibold mb-2">ChatGPT prompt</h3>
              <textarea
                className="w-full h-40 border rounded p-2 dark:bg-zinc-700"
                value={promptMessage}
                onChange={(e) => setPromptMessage(e.target.value)}
              />
              <div className="mb-4 flex items-center gap-2 p-2">
                <label htmlFor="lang">Prompt language:</label>
                <select
                  id="lang"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="border rounded p-1 text-sm bg-white dark:bg-zinc-800 dark:text-white"
                >
                  <option value="en">English</option>
                  <option value="fr">Français</option>
                  <option value="de">Deutsch</option>
                </select>
              </div>
              <div className="flex justify-end gap-2 mt-2">
                <button
                  className="px-4 py-1 bg-gray-300 dark:bg-zinc-600 rounded"
                  onClick={() => setIsMemoryDialog(false)}
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-1 bg-blue-600 text-white rounded"
                  onClick={() => {
                    // window.open(`https://chatgpt.com/?model=gpt-4.1&temporary-chat=true`, '_blank');
                    window.open(
                      `https://chatgpt.com/?temporary-chat=true`,
                      '_blank',
                    );
                  }}
                >
                  Open ChatGPT
                </button>
                <button
                  className="px-4 py-1 bg-blue-600 text-white rounded"
                  onClick={() => {
                    navigator.clipboard.writeText(
                      promptMessage +
                        `\n Respond with this language: ${language}`,
                    );
                  }}
                >
                  Copy this prompt
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
