"""
Tests for the RunPod MCP server.
"""

import sys
import os
import unittest
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestRunPodMCPServer(unittest.TestCase):
    """Test cases for the RunPod MCP server."""

    def test_version_resource(self):
        """Test that the version resource returns the correct version."""
        from src.runpod_mcp.server import get_version
        
        # We expect the version to be in the format "RunPod MCP Server vX.Y.Z"
        version_str = get_version()
        self.assertTrue(version_str.startswith("RunPod MCP Server v"))
        self.assertIn(".", version_str)  # Should contain at least one dot for version number

if __name__ == "__main__":
    unittest.main() 