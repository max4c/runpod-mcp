"""
Main MCP server implementation for RunPod integration.
"""

import os
import sys
import argparse
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from .config import get_config, RunPodConfig
from .client import RunPodClient
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)

# Create MCP server
mcp = FastMCP("RunPod MCP")

# Server context for maintaining a RunPod client instance
@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Server lifespan context manager for initializing resources."""
    try:
        # Set up logging
        configure_logging()
        logger.info("Starting RunPod MCP server")
        
        # Initialize RunPod client
        try:
            config = get_config()
            client = RunPodClient(config)
            logger.info("RunPod client initialized successfully")
            yield {"runpod_client": client, "config": config}
        except Exception as e:
            logger.error(f"Failed to initialize RunPod client: {e}")
            # We still yield an empty context to allow the server to start
            # even if the RunPod client fails to initialize
            yield {}
    finally:
        logger.info("Shutting down RunPod MCP server")

# Set the server lifespan
mcp.lifespan = server_lifespan

@mcp.resource("status://version")
def get_version() -> str:
    """Return the version of the RunPod MCP server."""
    from runpod_mcp import __version__
    return f"RunPod MCP Server v{__version__}"

@mcp.resource("status://config")
def get_config_status() -> str:
    """Return the configuration status of the RunPod MCP server."""
    try:
        config = get_config()
        return (
            f"RunPod MCP Server is configured with API URL: {config.api_url}\n"
            f"API Key: {'configured' if config.api_key else 'not configured'}"
        )
    except Exception as e:
        return f"RunPod MCP Server configuration error: {e}"

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="RunPod MCP Server")
    parser.add_argument(
        "--api-key", 
        help="RunPod API key (can also be set via RUNPOD_API_KEY environment variable)"
    )
    parser.add_argument(
        "--api-url", 
        help="RunPod API URL (default: https://api.runpod.io/v1)"
    )
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        help="Log file path (default: logs to stderr only)"
    )
    return parser.parse_args()

def main():
    """Run the MCP server."""
    args = parse_args()
    
    # Set environment variables from command-line arguments
    if args.api_key:
        os.environ["RUNPOD_API_KEY"] = args.api_key
    if args.api_url:
        os.environ["RUNPOD_API_URL"] = args.api_url
        
    # Configure logging
    log_level = getattr(logging, args.log_level.upper())
    configure_logging(level=log_level, log_file=args.log_file)
    
    # Run the server
    mcp.run()

if __name__ == "__main__":
    main() 