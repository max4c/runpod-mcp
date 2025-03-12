"""
Tests for the RunPod client module.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.runpod_mcp.config import RunPodConfig
from src.runpod_mcp.client import RunPodClient

class TestRunPodClient(unittest.TestCase):
    """Test cases for the RunPodClient class."""

    def setUp(self):
        """Set up the test environment."""
        self.config = RunPodConfig(api_key="test-api-key")
        
        # Create patcher for requests.Session
        self.session_patcher = patch('requests.Session')
        self.mock_session_class = self.session_patcher.start()
        self.mock_session = MagicMock()
        self.mock_session_class.return_value = self.mock_session
        
        # Create client for testing
        self.client = RunPodClient(self.config)

    def tearDown(self):
        """Tear down the test environment."""
        self.session_patcher.stop()

    def test_init(self):
        """Test client initialization."""
        # Check that the session was initialized with correct headers
        self.mock_session.headers.update.assert_called_once()
        update_args = self.mock_session.headers.update.call_args[0][0]
        self.assertEqual(update_args["Authorization"], "Bearer test-api-key")
        self.assertEqual(update_args["Content-Type"], "application/json")

    def test_get_gpus(self):
        """Test getting GPUs."""
        expected_result = [{"id": "gpu1", "name": "Test GPU"}]
        
        # Setup REST API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_session.get.return_value = mock_response
        
        result = self.client.get_gpus()
        
        # Verify REST API was called
        self.mock_session.get.assert_called_once_with(f"{self.config.api_url}/gpus")
        
        # Verify result
        self.assertEqual(result, expected_result)

    def test_create_pod(self):
        """Test creating a pod."""
        pod_config = {
            "gpu_id": "gpu1",
            "cloud_type": "SECURE",
            "image_name": "test/image:latest",
            "name": "test-pod"
        }
        expected_result = {"id": "pod1", "name": "test-pod", "status": "CREATED"}
        
        # Setup REST API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_session.post.return_value = mock_response
        
        result = self.client.create_pod(pod_config)
        
        # Verify REST API was called
        self.mock_session.post.assert_called_once_with(
            f"{self.config.api_url}/pods",
            json=pod_config
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
    
    def test_start_pod(self):
        """Test starting a pod."""
        pod_id = "pod1"
        expected_result = {"id": "pod1", "status": "STARTING"}
        
        # Setup REST API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_session.post.return_value = mock_response
        
        result = self.client.start_pod(pod_id)
        
        # Verify REST API was called
        self.mock_session.post.assert_called_once_with(
            f"{self.config.api_url}/pods/{pod_id}/start"
        )
        
        # Verify result
        self.assertEqual(result, expected_result)
        
    def test_stop_pod(self):
        """Test stopping a pod."""
        pod_id = "pod1"
        expected_result = {"id": "pod1", "status": "STOPPING"}
        
        # Setup REST API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.mock_session.post.return_value = mock_response
        
        result = self.client.stop_pod(pod_id)
        
        # Verify REST API was called
        self.mock_session.post.assert_called_once_with(
            f"{self.config.api_url}/pods/{pod_id}/stop"
        )
        
        # Verify result
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main() 