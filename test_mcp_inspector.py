#!/usr/bin/env python3
"""
Test script to verify the RunPod MCP implementation using the MCP Inspector tool.
This allows for interactive testing of the MCP server implementation.
"""

import asyncio
import logging
import sys
from mcp.inspector import Inspector

async def main():
    """Run the MCP Inspector against our RunPod MCP server."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create an inspector instance
    inspector = Inspector("RunPod MCP Test")
    
    # Start the server process
    server_process = await inspector.start_subprocess(
        [sys.executable, "-m", "src.runpod_mcp.server", "--log-level", "DEBUG"]
    )
    
    try:
        # Test basic server functionality
        print("Testing basic server functionality...")
        version = await inspector.call_resource("status://version")
        print(f"Server version: {version}")
        
        config_status = await inspector.call_resource("status://config")
        print(f"Config status: {config_status}")
        
        # Add more tests here as needed
        
        print("\nRunPod MCP server implementation verification completed successfully!")
        
    finally:
        # Clean up
        if server_process and server_process.returncode is None:
            server_process.terminate()
            await server_process.wait()

if __name__ == "__main__":
    asyncio.run(main()) 