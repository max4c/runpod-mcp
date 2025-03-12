"""
Configuration module for RunPod MCP.
Handles loading and managing API keys, endpoints, and other configuration.
"""

import os
from typing import Optional, Dict, Any
import json
import logging
from dataclasses import dataclass

@dataclass
class RunPodConfig:
    """Configuration for RunPod API access."""
    api_key: str
    api_url: str = "https://api.runpod.io/v1"
    
    @classmethod
    def from_env(cls) -> 'RunPodConfig':
        """Load configuration from environment variables."""
        api_key = os.environ.get("RUNPOD_API_KEY")
        if not api_key:
            raise ValueError("RUNPOD_API_KEY environment variable is required")
        
        api_url = os.environ.get("RUNPOD_API_URL", "https://api.runpod.io/v1")
        
        return cls(api_key=api_key, api_url=api_url)
    
    @classmethod
    def from_file(cls, config_path: str) -> 'RunPodConfig':
        """Load configuration from a JSON file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        api_key = config_data.get("api_key")
        if not api_key:
            raise ValueError("api_key is required in config file")
        
        api_url = config_data.get("api_url", "https://api.runpod.io/v1")
        
        return cls(api_key=api_key, api_url=api_url)

def get_config() -> RunPodConfig:
    """Get RunPod configuration from environment or config file."""
    # First try to load from environment
    try:
        return RunPodConfig.from_env()
    except ValueError:
        pass
    
    # Then try to load from default locations
    config_locations = [
        os.path.expanduser("~/.runpod/config.json"),
        os.path.join(os.getcwd(), "runpod_config.json"),
    ]
    
    for config_path in config_locations:
        if os.path.exists(config_path):
            try:
                return RunPodConfig.from_file(config_path)
            except Exception as e:
                logging.warning(f"Failed to load config from {config_path}: {e}")
    
    raise ValueError(
        "RunPod API key not found. Please set the RUNPOD_API_KEY environment variable "
        "or create a config file at ~/.runpod/config.json or ./runpod_config.json"
    ) 