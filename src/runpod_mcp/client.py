"""
RunPod API client module.
Provides authenticated access to the RunPod API.
"""

import logging
import asyncio
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
    
    # GPU related methods
    
    def get_gpus(self) -> List[Dict[str, Any]]:
        """Get available GPUs from RunPod.
        
        Returns:
            List of GPU objects with details
        """
        response = self.session.get(f"{self.api_base}/gpus")
        response.raise_for_status()
        return response.json()
    
    async def get_gpu_types(self) -> List[Dict[str, Any]]:
        """Get available GPU types from RunPod (async).
        
        Returns:
            List of GPU type objects with details
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_gpus)
    
    # Pod related methods
    
    def get_pods(self) -> List[Dict[str, Any]]:
        """Get all pods for the current user.
        
        Returns:
            List of pod objects with details
        """
        response = self.session.get(f"{self.api_base}/pods")
        response.raise_for_status()
        return response.json()
    
    async def get_pods(self) -> List[Dict[str, Any]]:
        """Get all pods for the current user (async).
        
        Returns:
            List of pod objects with details
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.get_pods())
    
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
    
    async def get_pod(self, pod_id: str) -> Dict[str, Any]:
        """Get details for a specific pod (async).
        
        Args:
            pod_id: The ID of the pod to retrieve
            
        Returns:
            Pod details object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.get_pod(pod_id))
    
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
    
    async def create_pod(self, pod_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new pod with the given configuration (async).
        
        Args:
            pod_config: Configuration for the new pod
            
        Returns:
            Created pod details
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.create_pod(pod_config))
    
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
    
    async def start_pod(self, pod_id: str) -> Dict[str, Any]:
        """Start a stopped pod (async).
        
        Args:
            pod_id: The ID of the pod to start
            
        Returns:
            Response data
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.start_pod(pod_id))
    
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
    
    async def stop_pod(self, pod_id: str) -> Dict[str, Any]:
        """Stop a running pod (async).
        
        Args:
            pod_id: The ID of the pod to stop
            
        Returns:
            Response data
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.stop_pod(pod_id))
    
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
    
    async def terminate_pod(self, pod_id: str) -> Dict[str, Any]:
        """Terminate a pod (async).
        
        Args:
            pod_id: The ID of the pod to terminate
            
        Returns:
            Response data
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.terminate_pod(pod_id))
    
    # Pod templates
    
    def get_pod_templates(self) -> List[Dict[str, Any]]:
        """Get available pod templates.
        
        Returns:
            List of pod template objects
        """
        response = self.session.get(f"{self.api_base}/templates")
        response.raise_for_status()
        return response.json()
    
    async def get_pod_templates(self) -> List[Dict[str, Any]]:
        """Get available pod templates (async).
        
        Returns:
            List of pod template objects
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_pod_templates)
    
    # Serverless endpoints
    
    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get all serverless endpoints for the current user.
        
        Returns:
            List of endpoint objects with details
        """
        response = self.session.get(f"{self.api_base}/endpoints")
        response.raise_for_status()
        return response.json()
    
    async def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get all serverless endpoints for the current user (async).
        
        Returns:
            List of endpoint objects with details
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_endpoints)
    
    def get_endpoint(self, endpoint_id: str) -> Dict[str, Any]:
        """Get details for a specific serverless endpoint.
        
        Args:
            endpoint_id: The ID of the endpoint to retrieve
            
        Returns:
            Endpoint details object
        """
        response = self.session.get(f"{self.api_base}/endpoints/{endpoint_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_endpoint(self, endpoint_id: str) -> Dict[str, Any]:
        """Get details for a specific serverless endpoint (async).
        
        Args:
            endpoint_id: The ID of the endpoint to retrieve
            
        Returns:
            Endpoint details object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.get_endpoint(endpoint_id))
    
    def get_endpoint_metrics(self, endpoint_id: str) -> Dict[str, Any]:
        """Get metrics for a specific serverless endpoint.
        
        Args:
            endpoint_id: The ID of the endpoint to retrieve metrics for
            
        Returns:
            Endpoint metrics object
        """
        response = self.session.get(f"{self.api_base}/endpoints/{endpoint_id}/metrics")
        response.raise_for_status()
        return response.json()
    
    async def get_endpoint_metrics(self, endpoint_id: str) -> Dict[str, Any]:
        """Get metrics for a specific serverless endpoint (async).
        
        Args:
            endpoint_id: The ID of the endpoint to retrieve metrics for
            
        Returns:
            Endpoint metrics object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.get_endpoint_metrics(endpoint_id))
    
    def get_serverless_templates(self) -> List[Dict[str, Any]]:
        """Get available serverless templates.
        
        Returns:
            List of serverless template objects
        """
        response = self.session.get(f"{self.api_base}/serverless/templates")
        response.raise_for_status()
        return response.json()
    
    async def get_serverless_templates(self) -> List[Dict[str, Any]]:
        """Get available serverless templates (async).
        
        Returns:
            List of serverless template objects
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_serverless_templates)
    
    # Network storage
    
    def get_network_volumes(self) -> List[Dict[str, Any]]:
        """Get all network storage volumes for the current user.
        
        Returns:
            List of network volume objects with details
        """
        response = self.session.get(f"{self.api_base}/network-volumes")
        response.raise_for_status()
        return response.json()
    
    async def get_network_volumes(self) -> List[Dict[str, Any]]:
        """Get all network storage volumes for the current user (async).
        
        Returns:
            List of network volume objects with details
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_network_volumes)
    
    def get_network_volume(self, volume_id: str) -> Dict[str, Any]:
        """Get details for a specific network storage volume.
        
        Args:
            volume_id: The ID of the volume to retrieve
            
        Returns:
            Network volume details object
        """
        response = self.session.get(f"{self.api_base}/network-volumes/{volume_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_network_volume(self, volume_id: str) -> Dict[str, Any]:
        """Get details for a specific network storage volume (async).
        
        Args:
            volume_id: The ID of the volume to retrieve
            
        Returns:
            Network volume details object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.get_network_volume(volume_id))
    
    # Account information
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get user account information.
        
        Returns:
            Account information object
        """
        response = self.session.get(f"{self.api_base}/me")
        response.raise_for_status()
        return response.json()
    
    async def get_account_info(self) -> Dict[str, Any]:
        """Get user account information (async).
        
        Returns:
            Account information object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_account_info)
    
    def get_credit_balance(self) -> float:
        """Get the current credit balance.
        
        Returns:
            Credit balance as a float
        """
        response = self.session.get(f"{self.api_base}/me")
        response.raise_for_status()
        return response.json().get("credits", 0.0)
    
    async def get_credit_balance(self) -> float:
        """Get the current credit balance (async).
        
        Returns:
            Credit balance as a float
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_credit_balance)
    
    def get_credits_info(self) -> Dict[str, Any]:
        """Get detailed credit usage information.
        
        Returns:
            Credit usage information object
        """
        # This is a placeholder - in a real implementation, this would
        # call the RunPod API to get detailed credit information
        account_info = self.get_account_info()
        balance = account_info.get("credits", 0.0)
        
        # Get active pods and their costs
        pods = self.get_pods()
        active_pods = [p for p in pods if p.get("desiredStatus") == "RUNNING"]
        
        # Get active endpoints and their costs
        endpoints = self.get_endpoints()
        
        # Mock detailed credit info
        return {
            "currentBalance": balance,
            "lastMonthUsage": balance * 0.2,  # Mock value
            "currentMonthUsage": balance * 0.1,  # Mock value
            "estimatedMonthlyBurn": sum(p.get("runtime", {}).get("costPerHr", 0) for p in active_pods) * 24 * 30,
            "activePods": active_pods,
            "activeEndpoints": endpoints,
            "activeVolumes": []
        }
    
    async def get_credits_info(self) -> Dict[str, Any]:
        """Get detailed credit usage information (async).
        
        Returns:
            Credit usage information object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_credits_info)
    
    def get_billing_history(self) -> Dict[str, Any]:
        """Get billing history for the user.
        
        Returns:
            Billing history object
        """
        # This is a placeholder - in a real implementation, this would
        # call the RunPod API to get billing history
        balance = self.get_credit_balance()
        
        # Mock billing history
        return {
            "currentMonth": {
                "total": balance * 0.1,
                "pods": balance * 0.05,
                "serverless": balance * 0.03,
                "storage": balance * 0.02,
                "other": 0
            },
            "lastMonth": {
                "total": balance * 0.2,
                "pods": balance * 0.1,
                "serverless": balance * 0.06,
                "storage": balance * 0.04,
                "other": 0
            },
            "twoMonthsAgo": {
                "total": balance * 0.15,
                "pods": balance * 0.08,
                "serverless": balance * 0.05,
                "storage": balance * 0.02,
                "other": 0
            },
            "paymentMethods": [
                {
                    "type": "Credit Card",
                    "lastFour": "1234",
                    "isDefault": True
                }
            ]
        }
    
    async def get_billing_history(self) -> Dict[str, Any]:
        """Get billing history for the user (async).
        
        Returns:
            Billing history object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_billing_history)
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics for the user.
        
        Returns:
            Usage statistics object
        """
        # This is a placeholder - in a real implementation, this would
        # call the RunPod API to get usage statistics
        
        # Mock usage statistics
        return {
            "currentMonth": {
                "gpuHours": 120.5,
                "gpuBreakdown": {
                    "A100": 50.2,
                    "RTX 4090": 40.1,
                    "RTX 3090": 30.2
                }
            },
            "lastMonth": {
                "gpuHours": 100.3,
                "gpuBreakdown": {
                    "A100": 40.1,
                    "RTX 4090": 35.0,
                    "RTX 3090": 25.2
                }
            }
        }
    
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics for the user (async).
        
        Returns:
            Usage statistics object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_usage_statistics) 