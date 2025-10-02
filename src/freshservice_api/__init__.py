"""
FreshService API package for accessing FreshService REST API endpoints.

This package contains modules for different FreshService API resources:
- departments: Department-related API operations
- solutions: Solutions/articles-related API operations
- service: Service items-related API operations
"""

from .departments import (
    DepartmentsAPI,
)

from .solutions import (
    SolutionsAPI,
    clean_html_content
)

from .requesters import (
    RequestersAPI,
)

from .service import (
    ServiceItemsAPI,
)

__all__ = [
    'DepartmentsAPI',
    'SolutionsAPI',
    'clean_html_content',
    'RequestersAPI',
    'ServiceItemsAPI',
]
