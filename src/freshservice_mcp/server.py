import os
import logging
import base64
from fastmcp import FastMCP

from dotenv import load_dotenv 
load_dotenv()

# Import department tools
from .departments import register_department_tools
# Import solution tools
from .solutions import register_solution_tools
# Import requester tools
from .requesters import register_requester_tools
# Import service item tools
from .service import register_service_item_tools


# Set up logging
logging.basicConfig(level=logging.INFO)


# Create MCP INSTANCE
mcp = FastMCP("freshservice_mcp")


# API CREDENTIALS
FRESHSERVICE_DOMAIN = os.getenv("FRESHSERVICE_DOMAIN")
FRESHSERVICE_API_KEY = os.getenv("FRESHSERVICE_API_KEY")


# GET AUTH HEADERS
def get_auth_headers():
    return {
        "Authorization": f"Basic {base64.b64encode(f'{FRESHSERVICE_API_KEY}:X'.encode()).decode()}",
        "Content-Type": "application/json"
    }


# Register department tools
register_department_tools(mcp, FRESHSERVICE_DOMAIN, get_auth_headers)

# Register solution tools
register_solution_tools(mcp, FRESHSERVICE_DOMAIN, get_auth_headers)

# Register requester tools
register_requester_tools(mcp, FRESHSERVICE_DOMAIN, get_auth_headers)

# Register service item tools
register_service_item_tools(mcp, FRESHSERVICE_DOMAIN, get_auth_headers)


def main():
    logging.info("Starting Freshservice MCP server")
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")

if __name__ == "__main__":
    main()
