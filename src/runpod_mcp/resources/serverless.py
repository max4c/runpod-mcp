"""
Serverless-related resources for the RunPod MCP server.

This module provides resources for querying serverless endpoints,
their configurations, and status.
"""

from typing import Dict, Any, List, Optional
import json

from ..logging_config import get_logger

logger = get_logger(__name__)

def register_serverless_resources(mcp_server):
    """Register serverless-related resources with the MCP server."""
    
    @mcp_server.resource("serverless://endpoints")
    async def list_endpoints() -> str:
        """
        Get a list of serverless endpoints in the user's account.
        
        Returns information about each endpoint including:
        - ID
        - Name
        - Status
        - Worker count
        - GPU type
        - Cost
        
        Example:
        ```
        Endpoint ID: abc123def
        Name: stable-diffusion-endpoint
        Status: READY
        Workers: 2
        GPU: RTX 4090
        Cost: $1.20/hr
        ```
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get endpoints from RunPod
            endpoints = await client.get_endpoints()
            
            if not endpoints:
                return "No serverless endpoints found in your account."
            
            # Format the endpoint information
            formatted_results = []
            for endpoint in endpoints:
                endpoint_id = endpoint.get("id", "Unknown ID")
                name = endpoint.get("name", "Unnamed Endpoint")
                status = endpoint.get("status", "UNKNOWN")
                workers = endpoint.get("workersRunning", 0)
                workers_max = endpoint.get("workersMax", 0)
                gpu_type = endpoint.get("gpuIds", ["Unknown"])[0] if endpoint.get("gpuIds") else "Unknown"
                cost_per_hour = endpoint.get("costPerHour", 0)
                
                formatted_results.append(
                    f"Endpoint ID: {endpoint_id}\n"
                    f"Name: {name}\n"
                    f"Status: {status}\n"
                    f"Workers: {workers}/{workers_max}\n"
                    f"GPU: {gpu_type}\n"
                    f"Cost: ${cost_per_hour:.2f}/hr\n"
                )
            
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Error fetching serverless endpoints: {e}")
            return f"Error fetching serverless endpoints: {str(e)}"
    
    @mcp_server.resource("serverless://endpoint/{endpoint_id}")
    async def endpoint_details(endpoint_id: str) -> str:
        """
        Get detailed information about a specific serverless endpoint.
        
        Parameters:
        - endpoint_id: The ID of the endpoint to retrieve details for
        
        Returns detailed information about the endpoint including:
        - Configuration details
        - Worker settings
        - Runtime statistics
        - Cost details
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get endpoint details
            endpoint = await client.get_endpoint(endpoint_id)
            
            if not endpoint:
                return f"Endpoint with ID '{endpoint_id}' not found."
            
            # Format detailed endpoint information
            name = endpoint.get("name", "Unnamed Endpoint")
            status = endpoint.get("status", "UNKNOWN")
            workers_running = endpoint.get("workersRunning", 0)
            workers_max = endpoint.get("workersMax", 0)
            workers_idle = endpoint.get("idleTimeout", 0)
            workers_scaling = endpoint.get("scalerType", "Unknown")
            gpu_types = endpoint.get("gpuIds", ["Unknown"])
            gpu_count = endpoint.get("gpuCount", 1)
            container_disk = endpoint.get("containerDisk", 0)
            container_memory = endpoint.get("containerMemory", 0)
            network_volume = endpoint.get("networkVolumeId", "None")
            cost_per_hour = endpoint.get("costPerHour", 0)
            
            # Container info
            template = endpoint.get("template", {})
            container = template.get("container", {})
            image = container.get("image", "Unknown")
            env = template.get("env", [])
            
            # Queue info
            queue_type = endpoint.get("queueType", "Unknown")
            queue_size = endpoint.get("queueSize", 0)
            
            # Format the details
            details = [
                f"# Endpoint: {name} ({endpoint_id})",
                f"",
                f"## Status",
                f"- Current Status: {status}",
                f"- Workers Running: {workers_running}/{workers_max}",
                f"- Worker Idle Timeout: {workers_idle} seconds",
                f"- Scaling Strategy: {workers_scaling}",
                f"- Queue Type: {queue_type}",
                f"- Queue Size: {queue_size}",
                f"",
                f"## Hardware Configuration",
                f"- GPU Type: {', '.join(gpu_types)}",
                f"- GPU Count per Worker: {gpu_count}",
                f"- Container Disk: {container_disk} GB",
                f"- Container Memory: {container_memory} GB",
            ]
            
            if network_volume and network_volume != "None":
                details.append(f"- Network Volume: {network_volume}")
            
            details.extend([
                f"",
                f"## Container Configuration",
                f"- Image: {image}",
            ])
            
            if env:
                details.append("")
                details.append("## Environment Variables")
                for e in env:
                    if isinstance(e, dict) and "key" in e:
                        # Don't display API keys or sensitive information
                        if "api_key" in e.get("key", "").lower() or "password" in e.get("key", "").lower() or "secret" in e.get("key", "").lower():
                            details.append(f"- {e.get('key')}: ******")
                        else:
                            details.append(f"- {e.get('key')}: {e.get('value', 'Not set')}")
            
            details.extend([
                f"",
                f"## Cost",
                f"- Cost per Hour: ${cost_per_hour:.2f}/hr",
                f"- Estimated Daily Cost (at max workers): ${cost_per_hour * 24 * workers_max:.2f}",
            ])
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching endpoint details for {endpoint_id}: {e}")
            return f"Error fetching endpoint details: {str(e)}"
    
    @mcp_server.resource("serverless://endpoint/{endpoint_id}/metrics")
    async def endpoint_metrics(endpoint_id: str) -> str:
        """
        Get metrics for a specific serverless endpoint.
        
        Parameters:
        - endpoint_id: The ID of the endpoint to retrieve metrics for
        
        Returns metrics information about the endpoint including:
        - Request count
        - Success/failure rates
        - Average response time
        - Worker utilization
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get endpoint metrics
            metrics = await client.get_endpoint_metrics(endpoint_id)
            
            if not metrics:
                return f"No metrics available for endpoint with ID '{endpoint_id}'."
            
            # Format metrics information
            name = metrics.get("name", "Unnamed Endpoint")
            total_requests = metrics.get("totalRequests", 0)
            success_count = metrics.get("successCount", 0)
            failure_count = metrics.get("failureCount", 0)
            avg_response_time = metrics.get("averageResponseTime", 0)
            utilization = metrics.get("utilization", 0) * 100  # Convert to percentage
            
            # Calculate success rate
            success_rate = 0
            if total_requests > 0:
                success_rate = (success_count / total_requests) * 100
            
            # Format the metrics
            details = [
                f"# Metrics for Endpoint: {name} ({endpoint_id})",
                f"",
                f"## Request Statistics (Last 24 Hours)",
                f"- Total Requests: {total_requests}",
                f"- Successful Requests: {success_count}",
                f"- Failed Requests: {failure_count}",
                f"- Success Rate: {success_rate:.2f}%",
                f"",
                f"## Performance",
                f"- Average Response Time: {avg_response_time:.2f} seconds",
                f"- Worker Utilization: {utilization:.2f}%",
            ]
            
            # Include any additional metrics
            credit_spent = metrics.get("creditSpent", 0)
            if credit_spent > 0:
                details.extend([
                    f"",
                    f"## Cost",
                    f"- Credit Spent: ${credit_spent:.2f}",
                ])
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching endpoint metrics for {endpoint_id}: {e}")
            return f"Error fetching endpoint metrics: {str(e)}"
    
    @mcp_server.resource("serverless://templates")
    async def serverless_templates() -> str:
        """
        Get a list of available serverless templates.
        
        Templates are pre-configured endpoint settings that can be used
        to quickly deploy endpoints with common configurations.
        
        Returns:
        A list of available serverless templates with their name, description, and key features.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get serverless templates from RunPod
            templates = await client.get_serverless_templates()
            
            if not templates:
                return "No serverless templates found."
            
            # Format the template information
            formatted_results = []
            formatted_results.append("# Available Serverless Templates\n")
            
            for template in templates:
                template_id = template.get("id", "Unknown ID")
                name = template.get("name", "Unnamed Template")
                container = template.get("container", {})
                image = container.get("image", "Unknown")
                description = template.get("description", "No description available")
                
                formatted_results.extend([
                    f"## {name} (ID: {template_id})",
                    f"- Image: {image}",
                    f"- Description: {description}",
                    ""
                ])
            
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Error fetching serverless templates: {e}")
            return f"Error fetching serverless templates: {str(e)}" 