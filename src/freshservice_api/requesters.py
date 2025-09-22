"""
FreshService Requesters API interface.

This module provides low-level API functions for interacting with FreshService requesters.
"""

import httpx
import urllib.parse
from typing import Dict, Any, List, Optional


class RequestersAPI:
    """API interface for FreshService requesters."""
    
    def __init__(self, freshservice_domain: str, get_auth_headers_func):
        self.freshservice_domain = freshservice_domain
        self.get_auth_headers = get_auth_headers_func
        self.base_url = f"https://{freshservice_domain}/api/v2/requesters"
    
    async def search_requesters_by_name(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict[str, Any]:
        """Search requesters by first name and/or last name.
        
        Args:
            first_name: Optional first name to search for
            last_name: Optional last name to search for
            
        Returns:
            Dictionary containing API response
            
        Raises:
            ValueError: If neither first_name nor last_name is provided
        """
        # Validate that at least one parameter is provided
        if not first_name and not last_name:
            raise ValueError("At least one of first_name or last_name must be provided")
        
        # Build the query string based on provided parameters
        query_parts = []
        if first_name and first_name.strip():
            query_parts.append(f"first_name:'{first_name.strip()}'")
        if last_name and last_name.strip():
            query_parts.append(f"last_name:'{last_name.strip()}'")
        
        query = " AND ".join(query_parts)
        
        encoded_query = urllib.parse.quote(query)
        url = f"{self.base_url}?query={encoded_query}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_requesters_by_department_id(self, department_id: int, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """Get requesters from a specific department with pagination.
        
        Args:
            department_id: Department ID to filter requesters by
            page: Page number (default: 1)
            per_page: Items per page (default: 100, max: 100)
            
        Returns:
            Dictionary containing API response
        """
        query = f"department_id:{department_id}"
        encoded_query = urllib.parse.quote(query)
        url = f'{self.base_url}?query="{encoded_query}"&page={page}&per_page={per_page}'
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_all_requesters_by_department_id(self, department_id: int) -> List[Dict[str, Any]]:
        """Get all requesters from a specific department across all pages.
        
        Args:
            department_id: Department ID to filter requesters by
            
        Returns:
            List of all requesters in the department
        """
        all_requesters = []
        page = 1
        per_page = 100
        
        while True:
            data = await self.get_requesters_by_department_id(department_id, page=page, per_page=per_page)
            
            # Extract requesters from response
            if "requesters" in data:
                requesters = data["requesters"]
                all_requesters.extend(requesters)
                
                # If we got fewer than 100 requesters, we're on the last page
                if len(requesters) < 100:
                    break
            else:
                # Handle case where response structure is different
                current_items = data if isinstance(data, list) else []
                all_requesters.extend(current_items)
                
                # If we got fewer than 100 items, we're done
                if len(current_items) < 100:
                    break
            
            page += 1
        
        return all_requesters
    
    async def get_requester_by_id(self, requester_id: int) -> Dict[str, Any]:
        """Get requester by ID.
        
        Args:
            requester_id: Requester ID
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}/{requester_id}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()


# Convenience functions for backward compatibility
async def search_requesters_by_name(freshservice_domain: str, get_auth_headers_func, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict[str, Any]:
    """Search requesters by first name and/or last name."""
    api = RequestersAPI(freshservice_domain, get_auth_headers_func)
    return await api.search_requesters_by_name(first_name, last_name)


async def get_requesters_by_department_id(freshservice_domain: str, get_auth_headers_func, department_id: int, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
    """Get requesters from a specific department with pagination."""
    api = RequestersAPI(freshservice_domain, get_auth_headers_func)
    return await api.get_requesters_by_department_id(department_id, page, per_page)


async def get_all_requesters_by_department_id(freshservice_domain: str, get_auth_headers_func, department_id: int) -> List[Dict[str, Any]]:
    """Get all requesters from a specific department across all pages."""
    api = RequestersAPI(freshservice_domain, get_auth_headers_func)
    return await api.get_all_requesters_by_department_id(department_id)


async def get_requester_by_id(freshservice_domain: str, get_auth_headers_func, requester_id: int) -> Dict[str, Any]:
    """Get requester by ID."""
    api = RequestersAPI(freshservice_domain, get_auth_headers_func)
    return await api.get_requester_by_id(requester_id)
