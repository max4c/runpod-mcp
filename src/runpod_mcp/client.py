"""
RunPod API client module.
Provides authenticated access to the RunPod API.
"""

import logging
from typing import Dict, List, Any, Optional, Union
import requests
from .config import RunPodConfig

logger = logging.getLogger(__name__)

class RunPodClient:
    """Client for interacting with RunPod API.
    
    This class uses direct REST API calls to interact with RunPod services.
    """
    
    def __init__(self, config: RunPodConfig):
        """Initialize the RunPod client.
        
        Args:
            config: RunPod configuration with API key and URL
        """
        self.config = config
        
        # Initialize direct REST client
        self.api_base = config.api_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        })
        
        logger.info(f"RunPod client initialized with API URL: {self.api_base}")
    
    def get_gpus(self) -> List[Dict[str, Any]]:
        """Get available GPUs from RunPod.
        
        Returns:
            List of GPU objects with details
        """
        response = self.session.get(f"{self.api_base}/gpus")
        response.raise_for_status()
        return response.json()
    
    def get_pods(self) -> List[Dict[str, Any]]:
        """Get all pods for the current user.
        
        Returns:
            List of pod objects with details
        """
        response = self.session.get(f"{self.api_base}/pods")
        response.raise_for_status()
        return response.json()
    
    def get_pod(self, pod_id: str) -> Dict[str, Any]:
        """Get details for a specific pod.
        
        Args:
            pod_id: The ID of the pod to retrieve
            
        Returns:
            Pod details object
        """
        response = self.session.get(f"{self.api_base}/pods/{pod_id}")
        response.raise_for_status()
        return response.json()
    
    def create_pod(self, pod_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new pod with the given configuration.
        
        Args:
            pod_config: Configuration for the new pod
            
        Returns:
            Created pod details
        """
        response = self.session.post(
            f"{self.api_base}/pods",
            json=pod_config
        )
        response.raise_for_status()
        return response.json()
    
    def start_pod(self, pod_id: str) -> Dict[str, Any]:
        """Start a stopped pod.
        
        Args:
            pod_id: The ID of the pod to start
            
        Returns:
            Response data
        """
        response = self.session.post(f"{self.api_base}/pods/{pod_id}/start")
        response.raise_for_status()
        return response.json()
    
    def stop_pod(self, pod_id: str) -> Dict[str, Any]:
        """Stop a running pod.
        
        Args:
            pod_id: The ID of the pod to stop
            
        Returns:
            Response data
        """
        response = self.session.post(f"{self.api_base}/pods/{pod_id}/stop")
        response.raise_for_status()
        return response.json()
    
    def terminate_pod(self, pod_id: str) -> Dict[str, Any]:
        """Terminate a pod.
        
        Args:
            pod_id: The ID of the pod to terminate
            
        Returns:
            Response data
        """
        response = self.session.post(f"{self.api_base}/pods/{pod_id}/terminate")
        response.raise_for_status()
        return response.json()
    
    def get_credit_balance(self) -> float:
        """Get the current credit balance.
        
        Returns:
            Credit balance as a float
        """
        response = self.session.get(f"{self.api_base}/me")
        response.raise_for_status()
        return response.json().get("credits", 0.0) 