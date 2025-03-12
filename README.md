# RunPod MCP

An implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) for [RunPod](https://runpod.io), allowing AI models to interact with RunPod cloud compute services.

## Overview

RunPod MCP creates a bridge between AI models like Claude and RunPod's GPU cloud compute services. It enables AI assistants to:

- Query available GPU types and their specifications
- Create, manage, and monitor compute instances (pods)
- Deploy and interact with serverless endpoints
- View and manage billing and credits

## Installation

```bash
# Clone the repository
git clone https://github.com/max4c/runpod-mcp.git
cd runpod-mcp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The RunPod MCP server requires an API key to access RunPod services. You can configure this in several ways:

### Environment Variables

```bash
export RUNPOD_API_KEY="your-api-key-here"
export RUNPOD_API_URL="https://api.runpod.io/v1"  # Optional, defaults to this URL
```

### Configuration File

Create a JSON file at `~/.runpod/config.json` or `./runpod_config.json`:

```json
{
  "api_key": "your-api-key-here",
  "api_url": "https://api.runpod.io/v1"
}
```

### Command-line Arguments

```bash
python -m src.runpod_mcp.server --api-key "your-api-key-here"
```

## Usage

### Development Mode

For testing with the MCP Inspector:

```bash
mcp dev src/runpod_mcp/server.py
```

### Claude Desktop Integration

To use with Claude:

```bash
mcp install src/runpod_mcp/server.py --name "RunPod MCP"
```

## Features

- **Resources**: Access information about available GPUs, pod configurations, and account status
- **Tools**: Create and manage RunPod compute instances
- **Prompts**: Get guidance on optimal GPU selection and configurations

## Development

### Running Tests

```bash
python -m unittest discover tests
```

## License

MIT

## Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [RunPod API Documentation](https://rest.runpod.io/v1/docs)
- [RunPod Python SDK Documentation](https://docs.runpod.io/tutorials/sdks/python/get-started/introduction) 