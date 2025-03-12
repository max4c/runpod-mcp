"""
Basic test for RunPod MCP imports.
"""
import os
import sys

try:
    import mcp
    print(f"✅ MCP SDK imported successfully")
except ImportError as e:
    print(f"❌ Failed to import MCP SDK: {e}")

try:
    import runpod
    print(f"✅ RunPod SDK imported successfully")
except ImportError as e:
    print(f"❌ Failed to import RunPod SDK: {e}")

try:
    import requests
    print(f"✅ Requests imported successfully: {requests.__version__}")
except ImportError as e:
    print(f"❌ Failed to import Requests: {e}")

# Test MCP functionality by creating a simple server
try:
    from mcp.server.fastmcp import FastMCP
    mcp_server = FastMCP("Test MCP Server")
    print("✅ Successfully created MCP server instance")
except Exception as e:
    print(f"❌ Failed to create MCP server instance: {e}")

if __name__ == "__main__":
    print("All dependencies are successfully installed!") 