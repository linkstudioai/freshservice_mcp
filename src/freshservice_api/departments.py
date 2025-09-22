"""
FreshService Departments API interface.

This module provides low-level API functions for interacting with FreshService departments.
"""

import httpx
import urllib.parse
from typing import Dict, Any, List, Optional


class DepartmentsAPI:
    """API interface for FreshService departments."""
    
    def __init__(self, freshservice_domain: str, get_auth_headers_func):
        self.freshservice_domain = freshservice_domain
        self.get_auth_headers = get_auth_headers_func
        self.base_url = f"https://{freshservice_domain}/api/v2/departments"
    
    async def list_departments(self, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """List departments with pagination.
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 100, max: 100)
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}?page={page}&per_page={per_page}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_all_departments(self) -> List[Dict[str, Any]]:
        """Fetch all departments across all pages.
        
        Returns:
            List of all departments
        """
        all_departments = []
        page = 1
        per_page = 100
        
        while True:
            data = await self.list_departments(page=page, per_page=per_page)
            
            # Extract departments from response
            if "departments" in data:
                departments = data["departments"]
                all_departments.extend(departments)
                
                # If we got fewer than 100 departments, we're on the last page
                if len(departments) < 100:
                    break
            else:
                # Handle case where response structure is different
                current_items = data if isinstance(data, list) else []
                all_departments.extend(current_items)
                
                # If we got fewer than 100 items, we're done
                if len(current_items) < 100:
                    break
            
            page += 1
        
        return all_departments
    
    async def search_departments_by_name(self, name: str) -> Dict[str, Any]:
        """Search departments by name.
        
        Args:
            name: Department name to search for
            
        Returns:
            Dictionary containing API response
        """
        query = f"name:'{name.strip()}'"
        encoded_query = urllib.parse.quote(query)
        url = f"{self.base_url}?query=\"{encoded_query}\""
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_department_by_id(self, department_id: int) -> Dict[str, Any]:
        """Get department by ID.
        
        Args:
            department_id: Department ID
            
        Returns:
            Dictionary containing API response
        """
        url = f"{self.base_url}/{department_id}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
