"""
GPU-related resources for the RunPod MCP server.

This module provides resources for querying available GPU types,
their specifications, and current availability on RunPod.
"""

import json
from typing import Dict, Any, List, Optional

from ..logging_config import get_logger

logger = get_logger(__name__)

def register_gpu_resources(mcp_server):
    """Register GPU-related resources with the MCP server."""
    
    @mcp_server.resource("gpus://available")
    async def available_gpus() -> str:
        """
        Get a list of all available GPU types on RunPod.
        
        Returns information about GPU models, their specifications,
        pricing, and current availability.
        
        Example:
        ```
        A100 80GB: 8x GPUs, 80GB VRAM each, $2.79/hr
        RTX 4090: 4x GPUs, 24GB VRAM each, $0.79/hr
        ...
        ```
        """
        try:
            # Get the RunPod client from the server context
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get GPU types from RunPod
            gpu_types = await client.get_gpu_types()
            
            if not gpu_types:
                return "No GPU types found or unable to retrieve GPU information."
            
            # Format the GPU information for human readability
            formatted_results = []
            for gpu in gpu_types:
                name = gpu.get("displayName", "Unknown GPU")
                vram = gpu.get("memoryInGb", "unknown")
                price = gpu.get("price", {}).get("minimumBidPrice", "N/A")
                availability = "Available" if gpu.get("available", False) else "Not available"
                
                formatted_results.append(
                    f"{name}: {vram}GB VRAM, ${price}/hr - {availability}"
                )
            
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Error fetching available GPUs: {e}")
            return f"Error fetching available GPUs: {str(e)}"
    
    @mcp_server.resource("gpus://details/{gpu_id}")
    async def gpu_details(gpu_id: str) -> str:
        """
        Get detailed information about a specific GPU type.
        
        Parameters:
        - gpu_id: The ID or name of the GPU to retrieve details for
        
        Returns detailed specifications, pricing, availability, and
        any special features of the specified GPU type.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get all GPU types first
            gpu_types = await client.get_gpu_types()
            
            if not gpu_types:
                return "No GPU types found or unable to retrieve GPU information."
            
            # Find the requested GPU
            gpu = None
            for g in gpu_types:
                if g.get("id") == gpu_id or g.get("displayName").lower() == gpu_id.lower():
                    gpu = g
                    break
            
            if not gpu:
                return f"GPU type '{gpu_id}' not found. Use 'gpus://available' to see all available types."
            
            # Format detailed GPU information
            name = gpu.get("displayName", "Unknown GPU")
            vram = gpu.get("memoryInGb", "unknown")
            price = gpu.get("price", {}).get("minimumBidPrice", "N/A")
            on_demand_price = gpu.get("price", {}).get("onDemandPrice", "N/A")
            secure_cloud = gpu.get("secureCloud", False)
            datacenter = gpu.get("datacenter", "Unknown")
            reliability = gpu.get("reliability", "Unknown")
            
            details = [
                f"# {name} Detailed Specifications",
                f"- Memory: {vram}GB VRAM",
                f"- Minimum Bid Price: ${price}/hr",
                f"- On-Demand Price: ${on_demand_price}/hr",
                f"- Secure Cloud: {'Yes' if secure_cloud else 'No'}",
                f"- Datacenter: {datacenter}",
                f"- Reliability: {reliability}",
            ]
            
            # Add availability info
            if gpu.get("available", False):
                details.append("- Status: Currently Available")
            else:
                details.append("- Status: Not Currently Available")
            
            return "\n".join(details)
        except Exception as e:
            logger.error(f"Error fetching GPU details for {gpu_id}: {e}")
            return f"Error fetching GPU details: {str(e)}"
    
    @mcp_server.resource("gpus://recommended/{workload_type}")
    async def recommended_gpus(workload_type: str) -> str:
        """
        Get GPU recommendations for specific workload types.
        
        Parameters:
        - workload_type: Type of workload (training, inference, rendering, etc.)
        
        Returns a list of recommended GPUs for the specified workload type,
        along with rationale for each recommendation.
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get all GPU types
            gpu_types = await client.get_gpu_types()
            
            if not gpu_types:
                return "No GPU types found or unable to retrieve GPU information."
            
            # Filter and sort based on workload type
            workload_type = workload_type.lower()
            
            # Define workload-specific recommendations
            if workload_type == "training":
                # For training, prioritize GPUs with more VRAM and compute power
                recommendations = [
                    "# Recommended GPUs for Training Workloads",
                    "",
                    "## High Performance (Large Models)",
                    "1. **A100 80GB** - Ideal for large language models and deep learning with extensive memory requirements",
                    "2. **H100** - Best for training at scale with exceptional performance and Tensor Cores",
                    "3. **A100 40GB** - Excellent for most training needs with good price/performance ratio",
                    "",
                    "## Mid-Range (Medium Models)",
                    "1. **RTX 4090** - Great balance of price and performance for medium-sized models",
                    "2. **RTX A6000** - Professional GPU with 48GB VRAM for memory-intensive tasks",
                    "3. **RTX 3090** - Cost-effective option for training medium models",
                    "",
                    "## Budget (Small Models)",
                    "1. **RTX 3080** - Affordable option for smaller models and experimentation",
                    "2. **RTX 2080 Ti** - Cost-effective for small dataset training"
                ]
            elif workload_type == "inference":
                # For inference, balance between VRAM and cost
                recommendations = [
                    "# Recommended GPUs for Inference Workloads",
                    "",
                    "## High Performance (Production)",
                    "1. **A100 40GB** - Best for high-volume inference with multiple large models loaded simultaneously",
                    "2. **RTX A6000** - Excellent for production inference with multiple models",
                    "",
                    "## Mid-Range (Development/Testing)",
                    "1. **RTX 4090** - Great for most inference tasks with excellent throughput",
                    "2. **RTX 3090** - Good balance of price and performance for development",
                    "",
                    "## Budget (Light Inference)",
                    "1. **RTX 3080** - Cost-effective for standard inference workloads",
                    "2. **RTX 3060** - Affordable option for lightweight inference"
                ]
            elif workload_type == "rendering":
                # For rendering, prioritize CUDA cores and compute power
                recommendations = [
                    "# Recommended GPUs for Rendering Workloads",
                    "",
                    "## High Performance (Professional)",
                    "1. **RTX A6000** - Professional-grade rendering with 48GB VRAM for complex scenes",
                    "2. **RTX 4090** - Excellent ray-tracing performance for high-quality renders",
                    "",
                    "## Mid-Range",
                    "1. **RTX 3090** - Strong rendering capabilities at a more affordable price",
                    "2. **RTX 3080** - Good performance for most standard rendering tasks",
                    "",
                    "## Budget",
                    "1. **RTX 3070** - Capable of quality rendering at a lower price point",
                    "2. **RTX 3060** - Entry-level GPU for basic rendering needs"
                ]
            else:
                return f"Unknown workload type: {workload_type}. Available types: training, inference, rendering"
            
            return "\n".join(recommendations)
        except Exception as e:
            logger.error(f"Error getting recommended GPUs for {workload_type}: {e}")
            return f"Error retrieving GPU recommendations: {str(e)}" 