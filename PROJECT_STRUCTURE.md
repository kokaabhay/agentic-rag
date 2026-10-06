# Project Architecture

Automatically generated project structure and Python architecture information.

## Directory Tree

```text
agentic-rag/
├── .git
│   └── [contents excluded]
├── __pycache__
│   └── [contents excluded]
├── api
│   ├── __pycache__
│   │   └── [contents excluded]
│   ├── __init__.py
│   ├── response_object.py
│   └── routes.py
├── app
│   ├── __pycache__
│   │   └── [contents excluded]
│   ├── agents
│   │   ├── __pycache__
│   │   │   └── [contents excluded]
│   │   ├── __init__.py
│   │   ├── decide_retrieval.py
│   │   └── orchestrator.py
│   ├── llm
│   │   ├── __pycache__
│   │   │   └── [contents excluded]
│   │   ├── __init__.py
│   │   ├── hyde.py
│   │   ├── prompt.py
│   │   ├── query_rewriter.py
│   │   └── service.py
│   ├── retrieval
│   │   ├── __pycache__
│   │   │   └── [contents excluded]
│   │   ├── __init__.py
│   │   ├── hybrid_search.py
│   │   └── reranker.py
│   └── __init__.py
├── scripts
│   ├── __init__.py
│   └── generate_structure.py
├── streamlit
│   └── s.py
├── venv
│   └── [contents excluded]
├── .env
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── PROJECT_STRUCTURE.md
├── readme.md
└── requirements.txt
```

## Python Architecture

### `api\__init__.py`

No classes, functions, or imports detected.

### `api\response_object.py`

**Classes:**
- `Response_Object`

**Imports:**
- `pydantic`

### `api\routes.py`

**Functions:**
- `response()`

**Imports:**
- `fastapi`
- `api.response_object`
- `pydantic`
- `app.llm.query_rewriter`
- `app.llm.prompt`
- `app.llm.service`
- `app.retrieval.hybrid_search`
- `app.retrieval.reranker`
- `app.llm.hyde`
- `app.agents.decide_retrieval`
- `app.agents.orchestrator`

### `app\__init__.py`

No classes, functions, or imports detected.

### `app\agents\__init__.py`

No classes, functions, or imports detected.

### `app\agents\decide_retrieval.py`

**Functions:**
- `decide_retrieve()`

**Imports:**
- `openai`
- `config`

### `app\agents\orchestrator.py`

**Classes:**
- `Orchestrator`

**Functions:**
- `__init__()`
- `orchestrate()`

**Imports:**
- `openai`
- `json`
- `config`

### `app\llm\__init__.py`

No classes, functions, or imports detected.

### `app\llm\hyde.py`

**Functions:**
- `generate_hypothetical_answer()`

**Imports:**
- `openai`
- `config`

### `app\llm\prompt.py`

**Functions:**
- `build_context()`
- `build_prompt()`

**Imports:**
- `tiktoken`
- `typing`
- `config`

### `app\llm\query_rewriter.py`

**Functions:**
- `rewrite_query()`

**Imports:**
- `openai`
- `config`

### `app\llm\service.py`

**Functions:**
- `generate_answer()`

**Imports:**
- `openai`
- `config`

### `app\retrieval\__init__.py`

No classes, functions, or imports detected.

### `app\retrieval\hybrid_search.py`

**Functions:**
- `generate_query_embedding()`
- `format_search_results()`
- `hybrid_search()`
- `hyde_retrieval()`

**Imports:**
- `azure.core.credentials`
- `azure.search.documents`
- `azure.search.documents.models`
- `openai`
- `app.agents.orchestrator`
- `config`

### `app\retrieval\reranker.py`

**Functions:**
- `rerank_documents()`

**Imports:**
- `certifi`
- `httpx`
- `config`

### `config.py`

**Imports:**
- `os`
- `dotenv`

### `main.py`

**Functions:**
- `get_health()`

**Imports:**
- `fastapi`
- `api.routes`

### `scripts\__init__.py`

No classes, functions, or imports detected.

### `scripts\generate_structure.py`

**Functions:**
- `should_hide()`
- `should_collapse()`
- `generate_tree()`
- `analyze_python_file()`
- `find_python_files()`
- `generate_markdown()`
- `main()`

**Imports:**
- `pathlib`
- `ast`

### `streamlit\s.py`

**Imports:**
- `streamlit`
- `requests`

## Collapsed Directories

The following directories are intentionally shown in the tree but their contents are not expanded:

- `.env/`
- `.git/`
- `.idea/`
- `.venv/`
- `.vscode/`
- `__pycache__/`
- `env/`
- `node_modules/`
- `venv/`

## Hidden Directories

The following directories are completely excluded from the generated architecture:

- `.coverage/`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.tox/`
- `build/`
- `dist/`
