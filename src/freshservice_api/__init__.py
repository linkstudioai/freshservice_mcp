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

from .requesters import (
    RequestersAPI,
    search_requesters_by_name,
    get_requesters_by_department_id,
    get_all_requesters_by_department_id,
    get_requester_by_id
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
    'clean_html_content',
    'RequestersAPI',
    'search_requesters_by_name',
    'get_requesters_by_department_id',
    'get_all_requesters_by_department_id',
    'get_requester_by_id'
]
