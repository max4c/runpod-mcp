"""
Pod-related resources for the RunPod MCP server.

This module provides resources for querying pod configurations,
templates, and running pod instances.
"""

from typing import Dict, Any, List, Optional
import json

from ..logging_config import get_logger

logger = get_logger(__name__)

def register_pod_resources(mcp_server):
    """Register pod-related resources with the MCP server."""
    
    @mcp_server.resource("pods://list")
    async def list_pods() -> str:
        """
        Get a list of all pods in the user's account.
        
        Returns information about each pod including:
        - ID
        - Name
        - GPU type
        - Status
        - Runtime
        - Cost
        
        Example:
        ```
        Pod ID: v6abc123def
        Name: stable-diffusion-pod
        GPU: RTX 4090
        Status: RUNNING
        Uptime: 3h 24m
        Cost: $2.70
        ```
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get pods from RunPod
            pods = await client.get_pods()
            
            if not pods:
                return "No pods found in your account."
            
            # Format the pod information
            formatted_results = []
            for pod in pods:
                pod_id = pod.get("id", "Unknown ID")
                name = pod.get("name", "Unnamed Pod")
                gpu_name = pod.get("gpuDisplayName", "Unknown GPU")
                status = pod.get("desiredStatus", "UNKNOWN")
                runtime = pod.get("runtime", {}).get("uptimeInSeconds", 0)
                cost = pod.get("runtime", {}).get("costPerHr", 0)
                
                # Convert runtime to human-readable format
                hours = runtime // 3600
                minutes = (runtime % 3600) // 60
                runtime_str = f"{hours}h {minutes}m"
                
                # Format the pod information
                formatted_results.append(
                    f"Pod ID: {pod_id}\n"
                    f"Name: {name}\n"
                    f"GPU: {gpu_name}\n"
                    f"Status: {status}\n"
                    f"Uptime: {runtime_str}\n"
                    f"Cost: ${cost:.2f}/hr\n"
                )
            
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Error fetching pods: {e}")
            return f"Error fetching pods: {str(e)}"
    
    @mcp_server.resource("pods://details/{pod_id}")
    async def pod_details(pod_id: str) -> str:
        """
        Get detailed information about a specific pod.
        
        Parameters:
        - pod_id: The ID of the pod to retrieve details for
        
        Returns detailed information about the pod including:
        - Configuration details
        - Volume information
        - Network settings
        - Runtime statistics
        - Cost details
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get pod details
            pod = await client.get_pod(pod_id)
            
            if not pod:
                return f"Pod with ID '{pod_id}' not found."
            
            # Format detailed pod information
            name = pod.get("name", "Unnamed Pod")
            gpu_name = pod.get("gpuDisplayName", "Unknown GPU")
            gpu_count = pod.get("gpuCount", 1)
            status = pod.get("desiredStatus", "UNKNOWN")
            machine_id = pod.get("machineId", "Unknown")
            env = pod.get("env", [])
            
            # Networking info
            networks = pod.get("ports", [])
            network_info = []
            for network in networks:
                network_info.append(f"- {network.get('name', 'Unknown')}: {network.get('ip', 'Unknown')}:{network.get('publicPort', 'Unknown')}")
            
            # Storage volumes
            volumes = pod.get("volumeMounts", [])
            volume_info = []
            for volume in volumes:
                volume_info.append(f"- {volume.get('name', 'Unknown')}: {volume.get('mountPath', 'Unknown')}")
            
            # Runtime info
            runtime = pod.get("runtime", {})
            uptime = runtime.get("uptimeInSeconds", 0)
            hours = uptime // 3600
            minutes = (uptime % 3600) // 60
            uptime_str = f"{hours}h {minutes}m"
            cost_per_hr = runtime.get("costPerHr", 0)
            
            # Container info
            container = pod.get("container", {})
            image = container.get("image", "Unknown")
            disk_in_gb = container.get("diskInGb", 0)
            memory_in_gb = container.get("memoryInGb", 0)
            
            # Assemble the details
            details = [
                f"# Pod: {name} ({pod_id})",
                f"## Configuration",
                f"- Status: {status}",
                f"- GPU: {gpu_count}x {gpu_name}",
                f"- Machine ID: {machine_id}",
                f"- Container Image: {image}",
                f"- Disk: {disk_in_gb} GB",
                f"- Memory: {memory_in_gb} GB",
                f"",
                f"## Networking",
            ]
            
            if network_info:
                details.extend(network_info)
            else:
                details.append("- No network information available")
            
            details.append("")
            details.append("## Storage")
            if volume_info:
                details.extend(volume_info)
            else:
                details.append("- No storage volumes attached")
            
            details.append("")
            details.append("## Runtime")
            details.append(f"- Uptime: {uptime_str}")
            details.append(f"- Cost: ${cost_per_hr:.2f}/hr")
            
            if env:
                details.append("")
                details.append("## Environment Variables")
                for e in env:
                    if isinstance(e, dict) and "key" in e:
                        details.append(f"- {e.get('key')}: {e.get('value', '******') if e.get('key', '').lower() != 'runpod_api_key' else '******'}")
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching pod details for {pod_id}: {e}")
            return f"Error fetching pod details: {str(e)}"
    
    @mcp_server.resource("pods://templates")
    async def pod_templates() -> str:
        """
        Get a list of available pod templates.
        
        Templates are pre-configured pod settings that can be used
        to quickly deploy pods with common configurations.
        
        Returns:
        A list of available templates with their name, description, and key features.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get templates from RunPod
            templates = await client.get_pod_templates()
            
            if not templates:
                return "No pod templates found."
            
            # Format the template information
            formatted_results = []
            for template in templates:
                template_id = template.get("id", "Unknown ID")
                name = template.get("name", "Unnamed Template")
                container = template.get("container", {})
                image = container.get("image", "Unknown")
                description = template.get("description", "No description available")
                
                formatted_results.append(
                    f"## {name} (ID: {template_id})",
                    f"- Image: {image}",
                    f"- Description: {description}",
                    ""
                )
            
            if formatted_results:
                return "# Available Pod Templates\n\n" + "\n".join(formatted_results)
            else:
                return "No pod templates found."
        except Exception as e:
            logger.error(f"Error fetching pod templates: {e}")
            return f"Error fetching pod templates: {str(e)}"
    
    @mcp_server.resource("pods://template/{template_id}")
    async def template_details(template_id: str) -> str:
        """
        Get detailed information about a specific pod template.
        
        Parameters:
        - template_id: The ID of the template to retrieve details for
        
        Returns:
        Detailed information about the template including container settings,
        environment variables, and recommended usage.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get templates from RunPod
            templates = await client.get_pod_templates()
            
            if not templates:
                return "No pod templates found."
            
            # Find the requested template
            template = None
            for t in templates:
                if t.get("id") == template_id:
                    template = t
                    break
            
            if not template:
                return f"Template with ID '{template_id}' not found. Use 'pods://templates' to see available templates."
            
            # Format detailed template information
            name = template.get("name", "Unnamed Template")
            description = template.get("description", "No description available")
            container = template.get("container", {})
            image = container.get("image", "Unknown")
            cmd = container.get("command", "")
            env = template.get("env", [])
            volumes = template.get("volumeMounts", [])
            ports = template.get("ports", [])
            
            details = [
                f"# Template: {name} ({template_id})",
                f"",
                f"## Description",
                f"{description}",
                f"",
                f"## Container Configuration",
                f"- Image: {image}",
                f"- Command: {cmd}" if cmd else "- Command: None specified",
            ]
            
            if ports:
                details.append("")
                details.append("## Network Ports")
                for port in ports:
                    details.append(f"- {port.get('name', 'Unknown')}: {port.get('containerPort', 'Unknown')}")
            
            if volumes:
                details.append("")
                details.append("## Volume Mounts")
                for volume in volumes:
                    details.append(f"- {volume.get('name', 'Unknown')}: {volume.get('mountPath', 'Unknown')}")
            
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
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching template details for {template_id}: {e}")
            return f"Error fetching template details: {str(e)}" 