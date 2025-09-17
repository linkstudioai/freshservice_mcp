"""
MCP tools for FreshService departments.

This module provides MCP (Model Context Protocol) tool implementations for department operations.
It uses the freshservice_api package for the actual API calls.
"""

import httpx
from typing import Dict, Any
from freshservice_api import DepartmentsAPI


def register_department_tools(mcp_instance, freshservice_domain: str, get_auth_headers_func):
    """Register department-related tools with the MCP instance."""
    
    # Create API instance
    departments_api = DepartmentsAPI(freshservice_domain, get_auth_headers_func)
    
    @mcp_instance.tool()
    async def list_all_departments() -> Dict[str, Any]:
        """List all departments in Freshservice. Fetches all departments across all pages."""
        try:
            all_departments = await departments_api.get_all_departments()
            
            return {
                "success": True,
                "departments": all_departments,
                "total_count": len(all_departments)
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to fetch list of departments: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred: {str(e)}"
            }
    
    @mcp_instance.tool()
    async def get_department_by_name(name: str) -> Dict[str, Any]:
        """Get department ID and details by department name.
        
        Args:
            name: The name of the department to search for
            
        Returns:
            Dictionary containing department details or error information
        """
        if not name or not name.strip():
            return {
                "error": "Department name is required and cannot be empty"
            }
        
        try:
            data = await departments_api.search_departments_by_name(name.strip())
            
            # Extract departments from response
            departments = data.get("departments", [])
            
            if not departments:
                return {
                    "success": False,
                    "message": f"No department found with name: '{name}'",
                    "department": None
                }
            
            # Return the first matching department (should be exact match)
            department = departments[0]
            
            return {
                "success": True,
                "message": f"Department found: '{department.get('name', 'Unknown')}'",
                "department": {
                    "id": department.get("id"),
                    "name": department.get("name"),
                    "description": department.get("description"),
                    "head_user_id": department.get("head_user_id"),
                    "prime_user_id": department.get("prime_user_id"),
                    "domains": department.get("domains", []),
                    "created_at": department.get("created_at"),
                    "updated_at": department.get("updated_at")
                },
                "total_matches": len(departments)
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to search for department '{name}': {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while searching for department '{name}': {str(e)}"
            }
    
    @mcp_instance.tool()
    async def get_department_id(department_id: int) -> Dict[str, Any]:
        """Get department details by department ID.
        
        Args:
            department_id: The ID of the department to retrieve
            
        Returns:
            Dictionary containing department details or error information
        """
        if not department_id or department_id <= 0:
            return {
                "error": "Department ID is required and must be a positive integer"
            }
        
        try:
            data = await departments_api.get_department_by_id(department_id)
            
            # Extract department from response
            department = data.get("department", data)
            
            return {
                "success": True,
                "message": f"Department found: '{department.get('name', 'Unknown')}'",
                "department": {
                    "id": department.get("id"),
                    "name": department.get("name"),
                    "description": department.get("description"),
                    "head_user_id": department.get("head_user_id"),
                    "prime_user_id": department.get("prime_user_id"),
                    "domains": department.get("domains", []),
                    "created_at": department.get("created_at"),
                    "updated_at": department.get("updated_at")
                }
            }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "message": f"No department found with ID: {department_id}",
                    "department": None
                }
            
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to retrieve department with ID {department_id}: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while retrieving department ID {department_id}: {str(e)}"
            }
