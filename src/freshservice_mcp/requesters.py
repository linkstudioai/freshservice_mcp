"""
MCP tools for FreshService requesters.

This module provides MCP (Model Context Protocol) tool implementations for requester operations.
It uses the freshservice_api package for the actual API calls.
"""

import httpx
from typing import Dict, Any, Optional
from freshservice_api import RequestersAPI


def _format_requester(requester: Dict[str, Any]) -> Dict[str, Any]:
    """Format a single requester for consistent output structure.
    
    Args:
        requester: Raw requester data from API
        
    Returns:
        Formatted requester dictionary
    """
    return {
        "id": requester.get("id"),
        "first_name": requester.get("first_name"),
        "last_name": requester.get("last_name"),
        "primary_email": requester.get("primary_email"),
        "job_title": requester.get("job_title"),
        "department_ids": requester.get("department_ids", []),
        "work_phone_number": requester.get("work_phone_number"),
        "mobile_phone_number": requester.get("mobile_phone_number"),
        "active": requester.get("active"),
        "created_at": requester.get("created_at"),
        "updated_at": requester.get("updated_at")
    }


def register_requester_tools(mcp_instance, freshservice_domain: str, get_auth_headers_func):
    """Register requester-related tools with the MCP instance."""
    
    # Create API instance
    requesters_api = RequestersAPI(freshservice_domain, get_auth_headers_func)
    
    @mcp_instance.tool()
    async def search_requesters_by_name(first_name: str, last_name: Optional[str] = None) -> Dict[str, Any]:
        """Search requesters by first name and optionally last name.
        
        Args:
            first_name: First name to search for (required)
            last_name: Last name to search for (optional)
            
        Returns:
            Dictionary containing matching requesters or error information
        """
        if not first_name or not first_name.strip():
            return {
                "error": "First name is required and cannot be empty"
            }
        
        try:
            data = await requesters_api.search_requesters_by_name(first_name.strip(), last_name.strip() if last_name else None)
            
            # Extract requesters from response
            requesters = data.get("requesters", [])
            
            if not requesters:
                search_term = f"{first_name}"
                if last_name:
                    search_term += f" {last_name}"
                return {
                    "success": True,
                    "message": f"No requesters found with name: '{search_term}'",
                    "requesters": [],
                    "total_count": 0
                }
            
            # Format requesters for consistent output
            formatted_requesters = [_format_requester(req) for req in requesters]
            
            search_term = f"{first_name}"
            if last_name:
                search_term += f" {last_name}"
            
            return {
                "success": True,
                "message": f"Found {len(requesters)} requester(s) matching name: '{search_term}'",
                "requesters": formatted_requesters,
                "total_count": len(requesters)
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            search_term = f"{first_name}"
            if last_name:
                search_term += f" {last_name}"

            return {
                "error": f"Failed to search for requesters with name '{search_term}': {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            search_term = f"{first_name}"
            if last_name:
                search_term += f" {last_name}"
            return {
                "error": f"Unexpected error occurred while searching for requesters with name '{search_term}': {str(e)}"
            }
    
    @mcp_instance.tool()
    async def get_requesters_by_department_id(department_id: int, get_all: bool = True) -> Dict[str, Any]:
        """Get requesters from a specific department.
        
        Args:
            department_id: Department ID to filter requesters by
            get_all: If True, gets all requesters across all pages. If False, gets first page only (default: True)
            
        Returns:
            Dictionary containing requesters from the department or error information
        """
        if not department_id or department_id <= 0:
            return {
                "error": "Department ID is required and must be a positive integer"
            }
        
        try:
            if get_all:
                # Get all requesters from the department across all pages
                all_requesters = await requesters_api.get_all_requesters_by_department_id(department_id)
                
                if not all_requesters:
                    return {
                        "success": True,
                        "message": f"No requesters found in department ID: {department_id}",
                        "requesters": [],
                        "total_count": 0,
                        "department_id": department_id
                    }
                
                # Format requesters for consistent output
                formatted_requesters = [_format_requester(req) for req in all_requesters]
                
                return {
                    "success": True,
                    "message": f"Found {len(all_requesters)} requester(s) in department ID: {department_id}",
                    "requesters": formatted_requesters,
                    "total_count": len(all_requesters),
                    "department_id": department_id
                }
            else:
                # Get first page only
                data = await requesters_api.get_requesters_by_department_id(department_id, page=1, per_page=100)
                requesters = data.get("requesters", [])
                
                if not requesters:
                    return {
                        "success": True,
                        "message": f"No requesters found in department ID: {department_id}",
                        "requesters": [],
                        "total_count": 0,
                        "department_id": department_id
                    }
                
                # Format requesters for consistent output
                formatted_requesters = [_format_requester(req) for req in requesters]
                
                return {
                    "success": True,
                    "message": f"Found {len(requesters)} requester(s) in department ID: {department_id} (first page)",
                    "requesters": formatted_requesters,
                    "total_count": len(requesters),
                    "department_id": department_id,
                    "note": "This shows the first page only. Set get_all=True to retrieve all requesters."
                }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to retrieve requesters for department ID {department_id}: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while retrieving requesters for department ID {department_id}: {str(e)}"
            }
    
    @mcp_instance.tool()
    async def get_requester_by_id(requester_id: int) -> Dict[str, Any]:
        """Get requester details by requester ID.
        
        Args:
            requester_id: The ID of the requester to retrieve
            
        Returns:
            Dictionary containing requester details or error information
        """
        if not requester_id or requester_id <= 0:
            return {
                "error": "Requester ID is required and must be a positive integer"
            }
        
        try:
            data = await requesters_api.get_requester_by_id(requester_id)
            
            # Extract requester from response
            requester = data.get("requester", data)
            
            return {
                "success": True,
                "message": f"Requester found: '{(requester.get('first_name', '') + ' ' + requester.get('last_name', '')).strip()}'",
                "requester": _format_requester(requester)
            }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "message": f"No requester found with ID: {requester_id}",
                    "requester": None
                }
            
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to retrieve requester with ID {requester_id}: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while retrieving requester ID {requester_id}: {str(e)}"
            }
