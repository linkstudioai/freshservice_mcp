"""
FreshService API package for accessing FreshService REST API endpoints.

This package contains modules for different FreshService API resources:
- departments: Department-related API operations
- solutions: Solutions/articles-related API operations
"""

from .departments import (
    DepartmentsAPI,
    list_departments,
    get_all_departments,
    search_departments_by_name,
    get_department_by_id
)

from .solutions import (
    SolutionsAPI,
    search_articles,
    search_all_articles,
    clean_html_content
)

__all__ = [
    'DepartmentsAPI',
    'list_departments',
    'get_all_departments', 
    'search_departments_by_name',
    'get_department_by_id',
    'SolutionsAPI',
    'search_articles',
    'search_all_articles',
    'clean_html_content'
]
