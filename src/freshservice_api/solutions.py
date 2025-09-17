"""
FreshService Solutions API interface.

This module provides low-level API functions for interacting with FreshService solutions/articles.
"""

import httpx
import urllib.parse
import re
from typing import Dict, Any, List, Optional, Union
from markdownify import markdownify as md


def clean_html_content(content) -> Union[str, Dict[str, Any]]:
    """Convert HTML content to clean Markdown format.
    
    Can handle both individual text strings and article dictionaries.
    
    Args:
        content: Either a string with HTML content, or a dict representing an article
        
    Returns:
        If string: Markdown formatted text
        If dict: Article data with HTML converted to Markdown in text fields
    """
    if isinstance(content, str):
        # Handle string input - convert HTML to Markdown
        if not content:
            return ""
        
        # Convert HTML to Markdown using markdownify
        markdown_text = md(
            content,
            heading_style="ATX",  # Use # for headings
            bullets="-",          # Use - for bullet points
            strip=['script', 'style']  # Remove script and style tags completely
        )
        
        # Clean up excessive whitespace and newlines
        markdown_text = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_text)  # Max 2 consecutive newlines
        markdown_text = re.sub(r'[ \t]+', ' ', markdown_text)  # Multiple spaces to single space
        markdown_text = markdown_text.strip()
        
        return markdown_text
    
    elif isinstance(content, dict):
        # Handle article dictionary - clean HTML from text fields
        if not content:
            return content
        
        # Create a copy to avoid modifying the original
        cleaned_article = content.copy()
        
        # Fields that commonly contain HTML
        html_fields = ['description', 'title', 'summary']
        
        for field in html_fields:
            if field in cleaned_article and cleaned_article[field]:
                cleaned_article[field] = clean_html_content(cleaned_article[field])
        
        return cleaned_article
    
    else:
        # Return as-is for other types
        return content


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
            Dictionary containing API response with HTML converted to Markdown in text fields
        """
        # URL encode the search term
        encoded_search_term = urllib.parse.quote(search_term)
        url = f"{self.base_url}/search?search_term={encoded_search_term}&page={page}&per_page={per_page}"
        headers = self.get_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Clean HTML from articles if present
            if "articles" in data and data["articles"]:
                data["articles"] = [clean_html_content(article) for article in data["articles"]]
            
            return data
    
    async def search_all_articles(self, search_term: str) -> List[Dict[str, Any]]:
        """Search all articles across all pages for a given term.
        
        Args:
            search_term: Term to search for in articles
            
        Returns:
            List of all matching articles with HTML converted to Markdown in text fields
        """
        all_articles = []
        page = 1
        per_page = 100
        
        while True:
            data = await self.search_articles(search_term=search_term, page=page, per_page=per_page)
            
            # Extract articles from response (already cleaned by search_articles)
            if "articles" in data:
                articles = data["articles"]
                all_articles.extend(articles)
                
                # If we got fewer than per_page articles, we're on the last page
                if len(articles) < per_page:
                    break
            else:
                # Handle case where response structure is different
                current_items = data if isinstance(data, list) else []
                # Clean HTML from items if they're not already cleaned
                cleaned_items = [clean_html_content(item) if isinstance(item, dict) else item for item in current_items]
                all_articles.extend(cleaned_items)
                
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


