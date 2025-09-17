"""
FreshService Solutions API interface.

This module provides low-level API functions for interacting with FreshService solutions/articles.
"""

import httpx
import urllib.parse
from typing import Dict, Any, List, Optional


class SolutionsAPI:
    """API interface for FreshService solutions/articles."""
    
    def __init__(self, freshservice_domain: str, get_auth_headers_func):
        self.freshservice_domain = freshservice_domain
        self.get_auth_headers = get_auth_headers_func
        self.base_url = f"https://{freshservice_domain}/api/v2/solutions/articles"
    
    async def search_articles(self, search_term: str, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """Search articles with pagination.
        
        Args:
            search_term: Term to search for in articles
            page: Page number (default: 1)
            per_page: Items per page (default: 100, max: 100)
            
        Returns:
            Dictionary containing API response
        """
        # URL encode the search term
        encoded_search_term = urllib.parse.quote(search_term)
        url = f"{self.base_url}/search?search_term={encoded_search_term}&page={page}&per_page={per_page}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def search_all_articles(self, search_term: str) -> List[Dict[str, Any]]:
        """Search all articles across all pages for a given term.
        
        Args:
            search_term: Term to search for in articles
            
        Returns:
            List of all matching articles
        """
        all_articles = []
        page = 1
        per_page = 100
        
        while True:
            data = await self.search_articles(search_term=search_term, page=page, per_page=per_page)
            
            # Extract articles from response
            if "articles" in data:
                articles = data["articles"]
                all_articles.extend(articles)
                
                # If we got fewer than per_page articles, we're on the last page
                if len(articles) < per_page:
                    break
            else:
                # Handle case where response structure is different
                current_items = data if isinstance(data, list) else []
                all_articles.extend(current_items)
                
                # If we got fewer than per_page items, we're done
                if len(current_items) < per_page:
                    break
            
            page += 1
        
        return all_articles


# Convenience functions for backward compatibility
async def search_articles(freshservice_domain: str, get_auth_headers_func, search_term: str, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
    """Search articles with pagination."""
    api = SolutionsAPI(freshservice_domain, get_auth_headers_func)
    return await api.search_articles(search_term, page, per_page)


async def search_all_articles(freshservice_domain: str, get_auth_headers_func, search_term: str) -> List[Dict[str, Any]]:
    """Search all articles across all pages for a given term."""
    api = SolutionsAPI(freshservice_domain, get_auth_headers_func)
    return await api.search_all_articles(search_term)
