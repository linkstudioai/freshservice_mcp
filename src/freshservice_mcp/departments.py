import httpx
from typing import Dict, Any

def register_department_tools(mcp_instance, freshservice_domain: str, get_auth_headers_func):
    """Register department-related tools with the MCP instance."""
    
    @mcp_instance.tool()
    async def list_all_departments() -> Dict[str, Any]:
        """List all departments in Freshservice."""
        url = f"https://{freshservice_domain}/api/v2/departments"
        headers = get_auth_headers_func()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  

                return response.json()

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

