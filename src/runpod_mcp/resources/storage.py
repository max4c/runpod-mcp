"""
Storage-related resources for the RunPod MCP server.

This module provides resources for querying network storage volumes
and their configurations.
"""

from typing import Dict, Any, List, Optional
import json

from ..logging_config import get_logger

logger = get_logger(__name__)

def register_storage_resources(mcp_server):
    """Register storage-related resources with the MCP server."""
    
    @mcp_server.resource("storage://volumes")
    async def list_volumes() -> str:
        """
        Get a list of network storage volumes in the user's account.
        
        Returns information about each volume including:
        - ID
        - Name
        - Size
        - Type
        - Status
        - Cost
        
        Example:
        ```
        Volume ID: vol-abc123
        Name: training-data
        Size: 100GB
        Type: Network Storage
        Status: READY
        Cost: $0.10/hr
        ```
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get volumes from RunPod
            volumes = await client.get_network_volumes()
            
            if not volumes:
                return "No network storage volumes found in your account."
            
            # Format the volume information
            formatted_results = []
            for volume in volumes:
                volume_id = volume.get("id", "Unknown ID")
                name = volume.get("name", "Unnamed Volume")
                size_gb = volume.get("sizeGB", 0)
                status = volume.get("status", "UNKNOWN")
                storage_type = volume.get("storageType", "Network Storage")
                cost = volume.get("costPerHr", 0)
                
                formatted_results.append(
                    f"Volume ID: {volume_id}\n"
                    f"Name: {name}\n"
                    f"Size: {size_gb} GB\n"
                    f"Type: {storage_type}\n"
                    f"Status: {status}\n"
                    f"Cost: ${cost:.2f}/hr\n"
                )
            
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Error fetching network volumes: {e}")
            return f"Error fetching network volumes: {str(e)}"
    
    @mcp_server.resource("storage://volume/{volume_id}")
    async def volume_details(volume_id: str) -> str:
        """
        Get detailed information about a specific network storage volume.
        
        Parameters:
        - volume_id: The ID of the volume to retrieve details for
        
        Returns detailed information about the volume including:
        - Configuration details
        - Attached pods
        - Usage statistics
        - Cost details
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get volume details
            volume = await client.get_network_volume(volume_id)
            
            if not volume:
                return f"Volume with ID '{volume_id}' not found."
            
            # Format detailed volume information
            name = volume.get("name", "Unnamed Volume")
            size_gb = volume.get("sizeGB", 0)
            status = volume.get("status", "UNKNOWN")
            storage_type = volume.get("storageType", "Network Storage")
            cost = volume.get("costPerHr", 0)
            region = volume.get("region", "Unknown")
            created_at = volume.get("createdAt", "Unknown")
            attached_pods = volume.get("pods", [])
            attached_endpoints = volume.get("endpoints", [])
            
            # Format the details
            details = [
                f"# Volume: {name} ({volume_id})",
                f"",
                f"## Configuration",
                f"- Status: {status}",
                f"- Size: {size_gb} GB",
                f"- Type: {storage_type}",
                f"- Region: {region}",
                f"- Created: {created_at}",
                f"",
                f"## Cost",
                f"- Cost per Hour: ${cost:.2f}/hr",
                f"- Estimated Monthly Cost: ${cost * 24 * 30:.2f}",
            ]
            
            # Add attached pods
            if attached_pods:
                details.append("")
                details.append("## Attached Pods")
                for pod in attached_pods:
                    pod_id = pod.get("id", "Unknown")
                    pod_name = pod.get("name", "Unnamed Pod")
                    details.append(f"- {pod_name} (ID: {pod_id})")
            
            # Add attached endpoints
            if attached_endpoints:
                details.append("")
                details.append("## Attached Serverless Endpoints")
                for endpoint in attached_endpoints:
                    endpoint_id = endpoint.get("id", "Unknown")
                    endpoint_name = endpoint.get("name", "Unnamed Endpoint")
                    details.append(f"- {endpoint_name} (ID: {endpoint_id})")
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching volume details for {volume_id}: {e}")
            return f"Error fetching volume details: {str(e)}"
    
    @mcp_server.resource("storage://types")
    async def storage_types() -> str:
        """
        Get information about available storage types on RunPod.
        
        Returns:
        A list of available storage types with their specifications,
        pricing, and use cases.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # In a real implementation, we'd fetch this from the RunPod API
            # For now, we'll return static information about storage types
            storage_types_info = [
                "# RunPod Storage Types",
                "",
                "## Network Storage Volumes",
                "- **Description**: Persistent storage volumes that can be attached to pods and serverless endpoints",
                "- **Use Cases**: Storing datasets, model checkpoints, and shared resources",
                "- **Features**:",
                "  - Can be attached to multiple pods",
                "  - Persists data between pod restarts",
                "  - Available in multiple regions",
                "- **Pricing**: $0.10/GB per month",
                "",
                "## Container Disk",
                "- **Description**: Temporary storage allocated to each pod or serverless endpoint container",
                "- **Use Cases**: Temporary storage during execution, caching, scratch space",
                "- **Features**:",
                "  - Fast local access",
                "  - Data does not persist when pod is terminated",
                "- **Sizing**: Can be specified during pod creation (default: 10GB)",
                "",
                "## Secure Cloud Storage",
                "- **Description**: Secure cloud storage for sensitive workloads",
                "- **Use Cases**: Financial data, healthcare applications, proprietary models",
                "- **Features**:",
                "  - Enhanced security controls",
                "  - Encryption at rest and in transit",
                "  - Compliance with security standards",
                "- **Availability**: Only in secure cloud regions",
            ]
            
            return "\n".join(storage_types_info)
        except Exception as e:
            logger.error(f"Error fetching storage types: {e}")
            return f"Error fetching storage types: {str(e)}" 