"""
FreshService Service Items API interface.

This module provides low-level API functions for interacting with FreshService service items.
"""

import httpx
import urllib.parse
from typing import Dict, Any, List, Optional


class ServiceItemsAPI:
    """API interface for FreshService service items."""
    
    def __init__(self, freshservice_domain: str, get_auth_headers_func):
        self.freshservice_domain = freshservice_domain
        self.get_auth_headers = get_auth_headers_func
        self.base_url = f"https://{freshservice_domain}/api/v2/service_catalog/items"
    
    async def list_service_items(self, page: int = 1, per_page: int = 30) -> Dict[str, Any]:
        """List service items with pagination.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 30, max: 100)
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}?page={page}&per_page={per_page}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_all_service_items(self, per_page: int = 100) -> List[Dict[str, Any]]:
        """Fetch all service items across all pages.
        
        Args:
            per_page: Items per page (default: 30, max: 100)
            
        Returns:
            List of all service items with pagination metadata
        """
        all_items = []
        page = 1
        
        while True:
            data = await self.list_service_items(page=page, per_page=per_page)
            all_items.append(data)
            
            # Check for pagination - if there's a Link header with 'next', continue
            # This would need to be handled based on response structure
            # For now, we'll check if we got fewer items than requested
            items_in_page = data.get("service_items", [])
            if len(items_in_page) < per_page:
                break
            
            page += 1
        
        return all_items
    
    async def search_service_items(self, query: str) -> Dict[str, Any]:
        """Search service items using a query string.
        
        Args:
            query: Search query string (can include filters like name, description, etc.)
            
        Returns:
            Dictionary containing API response with matching service items
            
        Example queries:
            - "name:'laptop'" - Search for items with 'laptop' in the name
            - "description:'software'" - Search for items with 'software' in description
        """
        # Encode the query parameter
        encoded_query = urllib.parse.quote(query)
        url = f"{self.base_url}?query=\"{encoded_query}\""
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_service_item_by_id(self, display_id: int) -> Dict[str, Any]:
        """Get service item by display ID.
        
        Args:
            display_id: Service item display ID
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}/{display_id}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

