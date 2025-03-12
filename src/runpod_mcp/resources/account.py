"""
Account-related resources for the RunPod MCP server.

This module provides resources for querying account information,
credits, and usage statistics.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta

from ..logging_config import get_logger

logger = get_logger(__name__)

def register_account_resources(mcp_server):
    """Register account-related resources with the MCP server."""
    
    @mcp_server.resource("account://info")
    async def account_info() -> str:
        """
        Get basic information about the user's RunPod account.
        
        Returns information about the account including:
        - Account ID
        - Username
        - Email
        - Account type
        - Account status
        - Credits balance
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get account info from RunPod
            account = await client.get_account_info()
            
            if not account:
                return "Failed to retrieve account information."
            
            # Format the account information
            account_id = account.get("id", "Unknown")
            username = account.get("username", "Unknown")
            email = account.get("email", "Unknown")
            account_type = account.get("accountType", "Standard")
            status = account.get("status", "Unknown")
            credits = account.get("credits", 0)
            
            formatted_info = [
                f"Account ID: {account_id}",
                f"Username: {username}",
                f"Email: {email}",
                f"Account Type: {account_type}",
                f"Account Status: {status}",
                f"Credits Balance: ${credits:.2f}",
            ]
            
            return "\n".join(formatted_info)
        except Exception as e:
            logger.error(f"Error fetching account info: {e}")
            return f"Error fetching account information: {str(e)}"
    
    @mcp_server.resource("account://credits")
    async def account_credits() -> str:
        """
        Get information about the user's RunPod credits.
        
        Returns:
        - Current credit balance
        - Credit usage history
        - Estimated burn rate
        - Upcoming charges
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get credit info from RunPod
            credits_info = await client.get_credits_info()
            
            if not credits_info:
                return "Failed to retrieve credits information."
            
            # Format the credits information
            current_balance = credits_info.get("currentBalance", 0)
            last_month_usage = credits_info.get("lastMonthUsage", 0)
            current_month_usage = credits_info.get("currentMonthUsage", 0)
            estimated_monthly_burn = credits_info.get("estimatedMonthlyBurn", 0)
            
            # Calculate days until credits are depleted
            days_until_empty = "N/A"
            if estimated_monthly_burn > 0:
                days_until_empty = int((current_balance / estimated_monthly_burn) * 30)
            
            # Get active resources that are consuming credits
            active_pods = credits_info.get("activePods", [])
            active_endpoints = credits_info.get("activeEndpoints", [])
            active_volumes = credits_info.get("activeVolumes", [])
            
            # Calculate total hourly burn rate
            hourly_burn = 0
            for pod in active_pods:
                hourly_burn += pod.get("costPerHr", 0)
            for endpoint in active_endpoints:
                hourly_burn += endpoint.get("costPerHour", 0)
            for volume in active_volumes:
                hourly_burn += volume.get("costPerHr", 0)
            
            # Format the response
            formatted_info = [
                "# RunPod Credits Information",
                "",
                f"## Balance and Usage",
                f"- Current Balance: ${current_balance:.2f}",
                f"- Last Month Usage: ${last_month_usage:.2f}",
                f"- Current Month Usage: ${current_month_usage:.2f}",
                f"- Estimated Monthly Burn Rate: ${estimated_monthly_burn:.2f}",
                "",
                f"## Current Consumption",
                f"- Current Hourly Burn Rate: ${hourly_burn:.2f}/hr",
                f"- Estimated Daily Cost: ${hourly_burn * 24:.2f}/day",
                f"- Days Until Credits Depleted: {days_until_empty}",
            ]
            
            # Add active resources if available
            if active_pods:
                formatted_info.append("")
                formatted_info.append("## Active Pods")
                for pod in active_pods:
                    name = pod.get("name", "Unnamed Pod")
                    cost = pod.get("costPerHr", 0)
                    formatted_info.append(f"- {name}: ${cost:.2f}/hr")
            
            if active_endpoints:
                formatted_info.append("")
                formatted_info.append("## Active Serverless Endpoints")
                for endpoint in active_endpoints:
                    name = endpoint.get("name", "Unnamed Endpoint")
                    cost = endpoint.get("costPerHour", 0)
                    formatted_info.append(f"- {name}: ${cost:.2f}/hr")
            
            if active_volumes:
                formatted_info.append("")
                formatted_info.append("## Active Storage Volumes")
                for volume in active_volumes:
                    name = volume.get("name", "Unnamed Volume")
                    cost = volume.get("costPerHr", 0)
                    formatted_info.append(f"- {name}: ${cost:.2f}/hr")
            
            return "\n".join(formatted_info)
        except Exception as e:
            logger.error(f"Error fetching credits info: {e}")
            return f"Error fetching credits information: {str(e)}"
    
    @mcp_server.resource("account://billing")
    async def billing_history() -> str:
        """
        Get the user's billing history on RunPod.
        
        Returns:
        - Billing history for the past 3 months
        - Breakdown by resource type
        - Payment methods
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get billing history from RunPod
            billing_history = await client.get_billing_history()
            
            if not billing_history:
                return "Failed to retrieve billing history."
            
            # Format the billing history
            current_month = billing_history.get("currentMonth", {})
            last_month = billing_history.get("lastMonth", {})
            two_months_ago = billing_history.get("twoMonthsAgo", {})
            payment_methods = billing_history.get("paymentMethods", [])
            
            # Format month data
            def format_month_data(month_data, title):
                total = month_data.get("total", 0)
                
                result = [
                    f"## {title}",
                    f"- Total: ${total:.2f}",
                ]
                
                # Breakdown by type
                pods_cost = month_data.get("pods", 0)
                serverless_cost = month_data.get("serverless", 0)
                storage_cost = month_data.get("storage", 0)
                other_cost = month_data.get("other", 0)
                
                result.extend([
                    f"- Pods: ${pods_cost:.2f}",
                    f"- Serverless: ${serverless_cost:.2f}",
                    f"- Storage: ${storage_cost:.2f}",
                    f"- Other: ${other_cost:.2f}",
                ])
                
                return result
            
            # Current month date range
            now = datetime.now()
            current_month_start = datetime(now.year, now.month, 1)
            current_month_end = now
            
            # Last month date range
            last_month_date = now - timedelta(days=30)
            last_month_start = datetime(last_month_date.year, last_month_date.month, 1)
            last_month_end = datetime(now.year, now.month, 1) - timedelta(days=1)
            
            # Two months ago date range
            two_months_ago_date = now - timedelta(days=60)
            two_months_ago_start = datetime(two_months_ago_date.year, two_months_ago_date.month, 1)
            two_months_ago_end = datetime(last_month_date.year, last_month_date.month, 1) - timedelta(days=1)
            
            # Format the response
            formatted_info = [
                "# RunPod Billing History",
                "",
            ]
            
            # Add current month
            formatted_info.extend(format_month_data(
                current_month,
                f"Current Month ({current_month_start.strftime('%Y-%m-%d')} to {current_month_end.strftime('%Y-%m-%d')})"
            ))
            formatted_info.append("")
            
            # Add last month
            formatted_info.extend(format_month_data(
                last_month,
                f"Last Month ({last_month_start.strftime('%Y-%m-%d')} to {last_month_end.strftime('%Y-%m-%d')})"
            ))
            formatted_info.append("")
            
            # Add two months ago
            formatted_info.extend(format_month_data(
                two_months_ago,
                f"Two Months Ago ({two_months_ago_start.strftime('%Y-%m-%d')} to {two_months_ago_end.strftime('%Y-%m-%d')})"
            ))
            
            # Add payment methods if available
            if payment_methods:
                formatted_info.append("")
                formatted_info.append("## Payment Methods")
                for method in payment_methods:
                    method_type = method.get("type", "Unknown")
                    last_four = method.get("lastFour", "****")
                    is_default = method.get("isDefault", False)
                    
                    formatted_info.append(f"- {method_type} ending in {last_four}{' (Default)' if is_default else ''}")
            
            return "\n".join(formatted_info)
        except Exception as e:
            logger.error(f"Error fetching billing history: {e}")
            return f"Error fetching billing history: {str(e)}"
    
    @mcp_server.resource("account://usage")
    async def usage_statistics() -> str:
        """
        Get detailed usage statistics for the user's account.
        
        Returns:
        - Compute usage (GPU hours)
        - Resource utilization
        - Usage trends
        """
        try:
            context = mcp_server.get_run_context()
            client = context.get("runpod_client")
            
            if not client:
                return "Error: RunPod client not available. Please check API key configuration."
            
            # Get usage statistics from RunPod
            usage_stats = await client.get_usage_statistics()
            
            if not usage_stats:
                return "Failed to retrieve usage statistics."
            
            # Format the usage statistics
            current_month = usage_stats.get("currentMonth", {})
            last_month = usage_stats.get("lastMonth", {})
            
            # Format GPU usage
            current_gpu_hours = current_month.get("gpuHours", 0)
            last_month_gpu_hours = last_month.get("gpuHours", 0)
            
            # GPU types usage breakdown
            current_gpu_breakdown = current_month.get("gpuBreakdown", {})
            last_month_gpu_breakdown = last_month.get("gpuBreakdown", {})
            
            # Format the response
            formatted_info = [
                "# RunPod Usage Statistics",
                "",
                "## Current Month Usage",
                f"- Total GPU Hours: {current_gpu_hours:.2f}",
            ]
            
            # Add current month GPU breakdown
            if current_gpu_breakdown:
                formatted_info.append("- GPU Usage Breakdown:")
                for gpu_type, hours in current_gpu_breakdown.items():
                    formatted_info.append(f"  - {gpu_type}: {hours:.2f} hours")
            
            formatted_info.extend([
                "",
                "## Last Month Usage",
                f"- Total GPU Hours: {last_month_gpu_hours:.2f}",
            ])
            
            # Add last month GPU breakdown
            if last_month_gpu_breakdown:
                formatted_info.append("- GPU Usage Breakdown:")
                for gpu_type, hours in last_month_gpu_breakdown.items():
                    formatted_info.append(f"  - {gpu_type}: {hours:.2f} hours")
            
            # Add usage comparison if available
            if last_month_gpu_hours > 0:
                percent_change = ((current_gpu_hours - last_month_gpu_hours) / last_month_gpu_hours) * 100
                formatted_info.extend([
                    "",
                    "## Usage Trends",
                    f"- Month-over-Month Change: {percent_change:.1f}% {'increase' if percent_change >= 0 else 'decrease'}",
                ])
            
            return "\n".join(formatted_info)
        except Exception as e:
            logger.error(f"Error fetching usage statistics: {e}")
            return f"Error fetching usage statistics: {str(e)}" 