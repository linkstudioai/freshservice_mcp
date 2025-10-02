"""
MCP tools for FreshService service items.

This module provides MCP (Model Context Protocol) tool implementations for service item operations.
It uses the freshservice_api package for the actual API calls.
"""

import httpx
from typing import Dict, Any, Optional
from freshservice_api import ServiceItemsAPI


def _format_service_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Format a single service item for consistent output structure.
    
    Args:
        item: Raw service item data from API
        
    Returns:
        Formatted service item dictionary
    """
    return {
        "id": item.get("id"),
        "display_id": item.get("display_id"),
        "name": item.get("name"),
        "description": item.get("description"),
        "short_description": item.get("short_description"),
        "cost": item.get("cost"),
        "quantity": item.get("quantity"),
        "category_id": item.get("category_id"),
        "visibility": item.get("visibility"),
        "deleted": item.get("deleted"),
        "icon_name": item.get("icon_name"),
        # "created_at": item.get("created_at"),
        # "updated_at": item.get("updated_at")
    }


def register_service_item_tools(mcp_instance, freshservice_domain: str, get_auth_headers_func):
    """Register service item-related tools with the MCP instance."""
    
    # Create API instance
    service_items_api = ServiceItemsAPI(freshservice_domain, get_auth_headers_func)
    
    @mcp_instance.tool()
    async def list_all_service_items(per_page: Optional[int] = 100) -> Dict[str, Any]:
        """List all service items in Freshservice. Fetches all items across all pages.
        
        Args:
            per_page: Number of items per page (default: 30, max: 100)
        """
        if per_page < 1 or per_page > 100:
            return {
                "error": "per_page must be between 1 and 100"
            }
        
        try:
            all_items = await service_items_api.get_all_service_items(per_page=per_page)
            
            # Count total items
            total_count = sum(len(page.get("service_items", [])) for page in all_items)
            
            return {
                "success": True,
                "items": all_items,
                "total_count": total_count,
                "pagination": {
                    "per_page": per_page,
                    "total_pages": len(all_items)
                }
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to fetch list of service items: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred: {str(e)}"
            }
    
    @mcp_instance.tool()
    async def search_service_items(query: str) -> Dict[str, Any]:
        """Search for service items using a query string.
        
        Args:
            query: Search query string. Examples:
                   - "name:'laptop'" - Search for items with 'laptop' in the name
                   - "description:'software'" - Search for items with 'software' in description
                   
        Returns:
            Dictionary containing search results or error information
        """
        if not query or not query.strip():
            return {
                "error": "Query is required and cannot be empty"
            }
        
        try:
            data = await service_items_api.search_service_items(query.strip())
            
            # Extract service items from response
            items = data.get("service_items", [])
            
            if not items:
                return {
                    "success": True,
                    "message": f"No service items found matching query: '{query}'",
                    "items": [],
                    "total_count": 0
                }
            
            # Format the items
            formatted_items = [_format_service_item(item) for item in items]
            
            return {
                "success": True,
                "message": f"Found {len(formatted_items)} service item(s)",
                "items": formatted_items,
                "total_count": len(formatted_items)
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to search service items with query '{query}': {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while searching service items: {str(e)}"
            }
    
    @mcp_instance.tool()
    async def get_service_item_by_id(display_id: int) -> Dict[str, Any]:
        """Get service item details by display ID.
        
        Args:
            display_id: The display ID of the service item to retrieve
            
        Returns:
            Dictionary containing service item details or error information
        """
        if not display_id or display_id <= 0:
            return {
                "error": "Display ID is required and must be a positive integer"
            }
        
        try:
            data = await service_items_api.get_service_item_by_id(display_id)
            
            # Extract service item from response
            item = data.get("service_item", data)
            
            return {
                "success": True,
                "message": f"Service item found: '{item.get('name', 'Unknown')}'",
                "item": _format_service_item(item)
            }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "message": f"No service item found with display ID: {display_id}",
                    "item": None
                }
            
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to retrieve service item with display ID {display_id}: {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while retrieving service item ID {display_id}: {str(e)}"
            }

