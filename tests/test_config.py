"""
Tests for the configuration module.
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.runpod_mcp.config import RunPodConfig, get_config

class TestRunPodConfig(unittest.TestCase):
    """Test cases for the RunPodConfig class."""

    def setUp(self):
        """Set up the test environment."""
        # Save any existing environment variables
        self.original_env = os.environ.copy()
        
        # Clear environment variables that might affect tests
        if "RUNPOD_API_KEY" in os.environ:
            del os.environ["RUNPOD_API_KEY"]
        if "RUNPOD_API_URL" in os.environ:
            del os.environ["RUNPOD_API_URL"]

    def tearDown(self):
        """Tear down the test environment."""
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_from_env_with_api_key(self):
        """Test loading config from environment with API key."""
        os.environ["RUNPOD_API_KEY"] = "test-api-key"
        config = RunPodConfig.from_env()
        self.assertEqual(config.api_key, "test-api-key")
        self.assertEqual(config.api_url, "https://api.runpod.io/v1")

    def test_from_env_with_api_key_and_url(self):
        """Test loading config from environment with API key and URL."""
        os.environ["RUNPOD_API_KEY"] = "test-api-key"
        os.environ["RUNPOD_API_URL"] = "https://custom-api.runpod.io/v1"
        config = RunPodConfig.from_env()
        self.assertEqual(config.api_key, "test-api-key")
        self.assertEqual(config.api_url, "https://custom-api.runpod.io/v1")

    def test_from_env_no_api_key(self):
        """Test that loading config from environment fails without API key."""
        with self.assertRaises(ValueError):
            RunPodConfig.from_env()

    def test_from_file(self):
        """Test loading config from file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            json.dump({
                "api_key": "test-api-key-from-file",
                "api_url": "https://custom-api-from-file.runpod.io/v1"
            }, temp)
            temp_path = temp.name

        try:
            config = RunPodConfig.from_file(temp_path)
            self.assertEqual(config.api_key, "test-api-key-from-file")
            self.assertEqual(config.api_url, "https://custom-api-from-file.runpod.io/v1")
        finally:
            os.unlink(temp_path)

    def test_from_file_no_api_key(self):
        """Test that loading config from file fails without API key."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            json.dump({
                "api_url": "https://custom-api-from-file.runpod.io/v1"
            }, temp)
            temp_path = temp.name

        try:
            with self.assertRaises(ValueError):
                RunPodConfig.from_file(temp_path)
        finally:
            os.unlink(temp_path)

    def test_from_file_not_found(self):
        """Test that loading config from nonexistent file fails."""
        with self.assertRaises(FileNotFoundError):
            RunPodConfig.from_file("/nonexistent/file.json")

    @patch('os.path.exists')
    def test_get_config_from_env(self, mock_exists):
        """Test that get_config() loads from environment variables if available."""
        # Make sure no config files are found
        mock_exists.return_value = False
        
        # Set up environment
        os.environ["RUNPOD_API_KEY"] = "test-api-key"
        
        config = get_config()
        self.assertEqual(config.api_key, "test-api-key")
        self.assertEqual(config.api_url, "https://api.runpod.io/v1")

if __name__ == "__main__":
    unittest.main() 