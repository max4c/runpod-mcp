"""
Resources module for the RunPod MCP server.

This module contains implementations of MCP resources that provide
information about RunPod entities such as GPU types, pod configurations,
serverless endpoints, and more.
"""

from .gpus import register_gpu_resources
from .pods import register_pod_resources
from .serverless import register_serverless_resources
from .storage import register_storage_resources
from .account import register_account_resources

def register_all_resources(mcp_server):
    """Register all RunPod MCP resources with the MCP server."""
    register_gpu_resources(mcp_server)
    register_pod_resources(mcp_server)
    register_serverless_resources(mcp_server)
    register_storage_resources(mcp_server)
    register_account_resources(mcp_server) 