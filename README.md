# Fast-MCP-Tools-Agent

A modular, fast, and extensible agent framework for Model Context Protocol (MCP) tools. This project is designed to help you quickly build, test, and deploy MCP-compatible tools and servers for analytics, finance, math, science, research, and more.

## Features
- Modular tool architecture (analytics, finance, math/science, research, etc.)
- Easy-to-extend with new tools and clients
- Configurable server with prompt registry
- Example client and server implementations

## Project Structure
```
Fast-MCP-Tools-Agent/
├── clients/           # Client implementations
│   ├── __init__.py
│   └── client.py
├── servers/           # Server and tool logic
│   ├── __init__.py
│   ├── config.py
│   ├── mcp_app.py
│   ├── prompt_registry.json
│   ├── server.py
│   └── tools/
│       ├── __init__.py
│       ├── analytics.py
│       ├── finance_tool.py
│       ├── math_science.py
│       ├── orchestrator.py
│       └── research_rag.py
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
python servers/server.py
```

### 3. Run the client (example)
```bash
python clients/client.py
```

## Adding New Tools
- Add your tool as a new Python file in `servers/tools/`.
- Register your tool in the orchestrator or main server logic as needed.

## Configuration
- Edit `servers/config.py` and `servers/prompt_registry.json` to customize prompts and server behavior.

## License
See [LICENSE](LICENSE) for details.
# Fast-MCP-Tools-Agent