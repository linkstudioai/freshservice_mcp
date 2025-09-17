"""
MCP tools for FreshService solutions/articles.

This module provides MCP (Model Context Protocol) tool implementations for solution operations.
It uses the freshservice_api package for the actual API calls.
"""

import httpx
from typing import Dict, Any
from freshservice_api import SolutionsAPI


def _format_article(article: Dict[str, Any], freshservice_domain: str) -> Dict[str, Any]:
    """Format a single article for consistent output structure.
    
    Args:
        article: Raw article data from API
        freshservice_domain: Domain for generating article URLs
        
    Returns:
        Formatted article dictionary
    """
    return {
        "id": article.get("id"),
        "title": article.get("title"),
        "description": article.get("description"),
        # "status": article.get("status"),
        "article_type": article.get("article_type"),
        "folder_id": article.get("folder_id"),
        "category_id": article.get("category_id"),
        "thumbs_up": article.get("thumbs_up", 0),
        "thumbs_down": article.get("thumbs_down", 0),
        # "hits": article.get("hits", 0),
        "tags": article.get("tags", []),
        "keywords": article.get("keywords", []),
        # "review_date": article.get("review_date"),
        # "created_at": article.get("created_at"),
        "updated_at": article.get("updated_at"),
        "url": f"https://{freshservice_domain}/support/solutions/articles/{article.get('id')}" if article.get('id') else None
    }


def register_solution_tools(mcp_instance, freshservice_domain: str, get_auth_headers_func):
    """Register solution-related tools with the MCP instance."""
    
    # Create API instance
    solutions_api = SolutionsAPI(freshservice_domain, get_auth_headers_func)
    
    @mcp_instance.tool()
    async def search_solutions(search_term: str) -> Dict[str, Any]:
        """Search for solutions/articles in Freshservice knowledge base.
        
        Args:
            search_term: The term to search for in articles (e.g., "printer", "password reset", "network")
            
        Returns:
            Dictionary containing matching articles or error information
        """
        if not search_term or not search_term.strip():
            return {
                "error": "Search term is required and cannot be empty"
            }
        
        try:
            all_articles = await solutions_api.search_all_articles(search_term.strip())
            
            if not all_articles:
                return {
                    "success": True,
                    "message": f"No articles found for search term: '{search_term}'",
                    "articles": [],
                    "total_count": 0
                }
            
            # Filter for only published articles (status: 2) and format for better readability
            published_articles = [article for article in all_articles if article.get("status") == 2]
            
            if not published_articles:
                return {
                    "success": True,
                    "message": f"No published articles found for search term: '{search_term}' (found {len(all_articles)} total articles, but none were published)",
                    "articles": [],
                    "total_count": 0,
                    "total_found": len(all_articles),
                    "search_term": search_term
                }
            
            formatted_articles = [
                _format_article(article, freshservice_domain) 
                for article in published_articles
            ]
            
            return {
                "success": True,
                "message": f"Found {len(published_articles)} published articles for search term: '{search_term}' (filtered from {len(all_articles)} total articles)",
                "articles": formatted_articles,
                "total_count": len(published_articles),
                "total_found": len(all_articles),
                "search_term": search_term
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to search for articles with term '{search_term}': {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while searching for articles with term '{search_term}': {str(e)}"
            }
    
    @mcp_instance.tool()
    async def search_solutions_paginated(search_term: str, page: int = 1, per_page: int = 30) -> Dict[str, Any]:
        """Search for solutions/articles with pagination control.
        
        Args:
            search_term: The term to search for in articles
            page: Page number to retrieve (default: 1)
            per_page: Number of articles per page (default: 30, max: 100)
            
        Returns:
            Dictionary containing paginated articles or error information
        """
        if not search_term or not search_term.strip():
            return {
                "error": "Search term is required and cannot be empty"
            }
        
        if page < 1:
            return {
                "error": "Page number must be 1 or greater"
            }
        
        if per_page < 1 or per_page > 100:
            return {
                "error": "Items per page must be between 1 and 100"
            }
        
        try:
            data = await solutions_api.search_articles(search_term.strip(), page, per_page)
            
            # Extract articles from response
            articles = data.get("articles", [])
            
            if not articles:
                return {
                    "success": True,
                    "message": f"No articles found for search term: '{search_term}' on page {page}",
                    "articles": [],
                    "page": page,
                    "per_page": per_page,
                    "total_count": 0
                }
            
            # Filter for only published articles (status: 2) and format for better readability
            published_articles = [article for article in articles if article.get("status") == 2]
            
            if not published_articles:
                return {
                    "success": True,
                    "message": f"No published articles found for search term: '{search_term}' on page {page} (found {len(articles)} total articles, but none were published)",
                    "articles": [],
                    "page": page,
                    "per_page": per_page,
                    "returned_count": 0,
                    "total_found": len(articles),
                    "search_term": search_term,
                    "has_more": len(articles) == per_page
                }
            
            formatted_articles = [
                _format_article(article, freshservice_domain) 
                for article in published_articles
            ]
            
            return {
                "success": True,
                "message": f"Found {len(published_articles)} published articles for search term: '{search_term}' on page {page} (filtered from {len(articles)} total articles)",
                "articles": formatted_articles,
                "page": page,
                "per_page": per_page,
                "returned_count": len(published_articles),
                "total_found": len(articles),
                "search_term": search_term,
                "has_more": len(articles) == per_page  # Indicates if there might be more pages
            }

        except httpx.HTTPStatusError as e:
            error_text = None
            try:
                error_text = e.response.json() if e.response else None
            except Exception:
                error_text = e.response.text if e.response else None

            return {
                "error": f"Failed to search for articles with term '{search_term}': {str(e)}",
                "status_code": e.response.status_code if e.response else None,
                "details": error_text
            }

        except Exception as e:
            return {
                "error": f"Unexpected error occurred while searching for articles with term '{search_term}': {str(e)}"
            }
