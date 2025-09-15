"""
Freshservice MCP Server Examples

This module contains example resources that demonstrate how to use the tools and prompts
effectively for common Freshservice operations.
"""

from fastmcp import FastMCP
from typing import Dict, Any, List


def register_examples(mcp: FastMCP):
    """Register all example resources with the MCP server instance"""
    
    @mcp.resource("freshservice://examples/ticket-operations")
    async def ticket_operations_examples() -> str:
        """Examples for common ticket operations in Freshservice"""
        return """# Ticket Operations Examples

## Creating Tickets

### Basic Ticket Creation
```python
# Create a simple support ticket
await create_ticket(
    subject="Email not working",
    description="User cannot send or receive emails since this morning",
    source=1,  # Email
    priority=2,  # Medium
    status=2,  # Open
    email="user@company.com"
)
```

### Ticket with Custom Fields
```python
# Create ticket with custom fields
await create_ticket(
    subject="Software installation request",
    description="Need Adobe Creative Suite installed on workstation",
    source=2,  # Portal
    priority=1,  # Low
    status=2,  # Open
    email="designer@company.com",
    custom_fields={
        "department": "Marketing",
        "location": "Building A, Floor 3",
        "urgency_reason": "Project deadline next week"
    }
)
```

## Filtering Tickets

### Filter by Status and Priority
```python
# Find all high priority open tickets
query = "priority:3 AND status:2"
await filter_tickets(query=query, page=1)
```

### Filter by Date Range
```python
# Find tickets created in the last 7 days
query = "created_at:>'2025-09-08'"
await filter_tickets(query=query)
```

### Complex Filtering
```python
# Find urgent tickets assigned to specific agent, created this month
query = "priority:4 AND agent_id:12345 AND created_at:>'2025-09-01'"
await filter_tickets(query=query)
```

### Filter by Multiple Conditions
```python
# Find pending tickets for specific requester with high priority
query = "status:3 AND email:'user@company.com' AND priority:3"
await filter_tickets(query=query)
```

## Updating Tickets

### Change Priority and Status
```python
# Escalate ticket priority and mark as pending
await update_ticket(
    ticket_id=12345,
    ticket_fields={
        "priority": 4,  # Urgent
        "status": 3,    # Pending
        "custom_fields": {
            "escalation_reason": "Customer VIP status"
        }
    }
)
```

### Assign to Agent
```python
# Assign ticket to specific agent
await update_ticket(
    ticket_id=12345,
    ticket_fields={
        "responder_id": 67890,
        "group_id": 123
    }
)
```

## Ticket Communication

### Add Internal Note
```python
# Add private note for internal team
await create_ticket_note(
    ticket_id=12345,
    body="Escalated to senior technician. Requires hardware replacement."
)
```

### Send Reply to Customer
```python
# Send update to customer
await send_ticket_reply(
    ticket_id=12345,
    body="We have identified the issue and are working on a solution. Expected resolution within 2 hours.",
    from_email="support@company.com"
)
```

### Reply with CC
```python
# Send reply with additional stakeholders
await send_ticket_reply(
    ticket_id=12345,
    body="Issue resolved. Please test and confirm functionality.",
    cc_emails=["manager@company.com", "user@company.com"]
)
```
"""

    @mcp.resource("freshservice://examples/agent-management")
    async def agent_management_examples() -> str:
        """Examples for agent and group management operations"""
        return """# Agent Management Examples

## Creating Agents

### Basic Agent Creation
```python
# Create a new agent
await create_agent(
    first_name="John",
    last_name="Smith",
    email="john.smith@company.com",
    job_title="IT Support Specialist"
)
```

### Create Occasional Agent
```python
# Create occasional agent (limited access)
await create_agent(
    first_name="Jane",
    last_name="Consultant", 
    email="jane@consultant.com",
    occasional=True,
    job_title="External Consultant"
)
```

## Managing Groups

### Create Agent Group
```python
# Create new support group
group_data = {
    "name": "Network Support Team",
    "description": "Handles network infrastructure issues",
    "agent_ids": [123, 456, 789],
    "auto_ticket_assign": True,
    "escalate_to": 100,  # Manager ID
    "unassigned_for": "2h"
}
await create_group(group_data)
```

### Update Group Settings
```python
# Update group configuration
await update_group(
    group_id=50,
    group_fields={
        "name": "Advanced Network Support",
        "auto_ticket_assign": False,
        "unassigned_for": "1h"
    }
)
```

## Agent Filtering and Search

### Find Agents by Department
```python
# Search for agents in specific department
query = "department:'IT Support'"
agents = await filter_agents(query)
```

### Get Agent Workload
```python
# Analyze specific agent's current workload
await agent_workload_prompt(agent_id=123)
```

## Requester Management

### Create Requester
```python
# Create new requester with full details
await create_requester(
    first_name="Alice",
    last_name="Johnson",
    primary_email="alice@company.com",
    job_title="Marketing Manager",
    department_ids=[10, 15],
    work_phone_number="555-0123",
    location_id=5
)
```

### Filter Requesters
```python
# Find requesters by name
query = "first_name:'John'"
await filter_requesters(query, include_agents=False)
```

### Update Requester Information
```python
# Update requester details
await update_requester(
    requester_id=456,
    job_title="Senior Marketing Manager",
    department_ids=[10, 15, 20],
    custom_fields={
        "employee_id": "EMP001",
        "cost_center": "MKT-2024"
    }
)
```
"""

    @mcp.resource("freshservice://examples/knowledge-base")
    async def knowledge_base_examples() -> str:
        """Examples for knowledge base and solution management"""
        return """# Knowledge Base Examples

## Solution Categories

### Create Solution Category
```python
# Create new category for solutions
await create_solution_category(
    name="Network Troubleshooting",
    description="Solutions for common network issues",
    workspace_id=1
)
```

### Update Category
```python
# Update existing category
await update_solution_category(
    category_id=10,
    name="Advanced Network Troubleshooting",
    description="Complex network solutions and procedures"
)
```

## Solution Folders

### Create Solution Folder
```python
# Create folder within category
await create_solution_folder(
    name="WiFi Connection Issues",
    category_id=10,
    department_ids=[1, 2, 3],
    visibility=4,  # All agents
    description="Common WiFi troubleshooting procedures"
)
```

## Solution Articles

### Create Comprehensive Article
```python
# Create detailed solution article
await create_solution_article(
    title="How to Reset Network Adapter on Windows 10",
    description='''
# Network Adapter Reset Procedure

## Problem Description
Users experiencing intermittent network connectivity issues on Windows 10.

## Prerequisites
- Administrative access to the computer
- Basic understanding of Windows settings

## Step-by-Step Solution

### Method 1: Network Reset via Settings
1. Open Windows Settings (Win + I)
2. Navigate to Network & Internet
3. Click on "Network reset" at the bottom
4. Click "Reset now" and confirm
5. Restart the computer

### Method 2: Command Line Reset
1. Open Command Prompt as Administrator
2. Run: `netsh winsock reset`
3. Run: `netsh int ip reset`
4. Restart the computer

### Method 3: Device Manager Reset
1. Right-click on Start button
2. Select Device Manager
3. Expand Network adapters
4. Right-click on your network adapter
5. Select "Uninstall device"
6. Restart computer (driver will reinstall automatically)

## Verification Steps
1. Check network connectivity
2. Test with different websites
3. Verify IP configuration with `ipconfig`

## Troubleshooting
If issues persist:
- Check physical cable connections
- Contact network administrator
- Consider hardware replacement

## Related Articles
- WiFi Password Recovery
- Network Driver Updates
- VPN Configuration Issues
    ''',
    folder_id=25,
    article_type=1,  # Permanent solution
    status=2,  # Published
    tags=["network", "windows", "troubleshooting"],
    keywords=["adapter", "reset", "connectivity", "wifi"]
)
```

### Update Article
```python
# Update existing article
await update_solution_article(
    article_id=100,
    title="Updated: Network Adapter Reset for Windows 10/11",
    tags=["network", "windows", "windows10", "windows11", "troubleshooting"]
)
```

### Publish Article
```python
# Publish draft article
await publish_solution_article(article_id=100)
```

## Knowledge Base Search Strategy

### Search Existing Content
```python
# Use knowledge base prompt for comprehensive search
await knowledge_base_prompt(
    topic="email configuration",
    article_type="procedure"
)
```
"""

    @mcp.resource("freshservice://examples/service-catalog")
    async def service_catalog_examples() -> str:
        """Examples for service catalog and request management"""
        return """# Service Catalog Examples

## Service Items

### List All Service Items
```python
# Get all available service items
items = await list_service_items(page=1, per_page=50)

# Process items for display
for page_data in items['items']:
    if 'service_items' in page_data:
        for item in page_data['service_items']:
            print(f"Item: {item['name']} (ID: {item['id']})")
```

### Create Service Request
```python
# Request software installation
await create_service_request(
    display_id=123,  # Service item ID
    email="user@company.com",
    requested_for="newuser@company.com",  # If requesting for someone else
    quantity=1
)
```

### Multiple Service Requests
```python
# Request multiple licenses
await create_service_request(
    display_id=456,  # Software license item
    email="manager@company.com",
    quantity=5  # 5 licenses
)
```

## Request Management

### Get Requested Items for Ticket
```python
# Check what service items were requested in a ticket
requested_items = await get_requested_items(ticket_id=12345)

if requested_items.get('success'):
    for item in requested_items.get('requested_items', []):
        print(f"Requested: {item['service_item']['name']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Status: {item['status']}")
```

## Products and Assets

### Create Product
```python
# Create new product in catalog
await create_product(
    name="Dell OptiPlex 7090",
    asset_type_id=1,  # Computer asset type
    manufacturer="Dell Inc.",
    status="In Production",
    description="Business desktop computer",
    mode_of_procurement="Purchase"
)
```

### Update Product
```python
# Update product information
await update_product(
    id=789,
    name="Dell OptiPlex 7090 (Updated)",
    status="In Pipeline",
    description="Updated business desktop with enhanced specs"
)
```

### Get Product Details
```python
# Retrieve specific product information
product = await get_products_by_id(product_id=789)
print(f"Product: {product['product']['name']}")
print(f"Status: {product['product']['status']}")
```
"""

    @mcp.resource("freshservice://examples/reporting-analytics")
    async def reporting_analytics_examples() -> str:
        """Examples for reporting and analytics operations"""
        return """# Reporting and Analytics Examples

## Ticket Reports

### Daily Ticket Summary
```python
# Generate daily ticket report
await bulk_ticket_report_prompt(
    status="open",
    days_back=1
)
```

### Weekly Performance Report
```python
# Weekly team performance analysis
await bulk_ticket_report_prompt(
    days_back=7
)
```

### Priority-Based Analysis
```python
# Focus on high priority tickets
await bulk_ticket_report_prompt(
    priority="high",
    days_back=30
)
```

### Agent-Specific Report
```python
# Analyze specific agent's performance
await bulk_ticket_report_prompt(
    agent_id=123,
    days_back=14
)
```

## SLA Monitoring

### Critical SLA Monitoring
```python
# Monitor urgent tickets for SLA compliance
await sla_monitoring_prompt(
    priority_level="urgent"
)
```

### Workspace-Specific SLA
```python
# Monitor SLA for specific workspace
await sla_monitoring_prompt(
    workspace_id=5,
    priority_level="high"
)
```

## Advanced Filtering for Reports

### Overdue Tickets Report
```python
# Find all overdue tickets
query = "due_by:<'2025-09-15' AND status:<4"
overdue_tickets = await filter_tickets(query)
```

### Unassigned Tickets
```python
# Find unassigned open tickets
query = "agent_id:null AND status:2"
unassigned = await filter_tickets(query)
```

### Recent High Priority Tickets
```python
# High priority tickets from last 24 hours
query = "priority:3 AND created_at:>'2025-09-14'"
recent_urgent = await filter_tickets(query)
```

### Customer-Specific Analysis
```python
# All tickets from specific customer domain
query = "email:*'@importantclient.com' AND created_at:>'2025-09-01'"
customer_tickets = await filter_tickets(query)
```

## Workload Analysis

### Team Workload Distribution
```python
# Analyze entire team workload
await agent_workload_prompt()
```

### Individual Agent Analysis
```python
# Deep dive into specific agent performance
await agent_workload_prompt(agent_id=456)
```

## Custom Analytics Queries

### Tickets by Source Analysis
```python
# Email tickets vs Portal tickets
email_query = "source:1 AND created_at:>'2025-09-01'"
portal_query = "source:2 AND created_at:>'2025-09-01'"

email_tickets = await filter_tickets(email_query)
portal_tickets = await filter_tickets(portal_query)
```

### Resolution Time Analysis
```python
# Tickets resolved within SLA
resolved_query = "status:4 AND updated_at:>'2025-09-01'"
resolved_tickets = await filter_tickets(resolved_query)
```

### Escalation Tracking
```python
# Track tickets that have been escalated
escalated_query = "priority:>2 AND updated_at:>'2025-09-01'"
escalated_tickets = await filter_tickets(escalated_query)
```
"""

    @mcp.resource("freshservice://examples/automation-workflows")
    async def automation_workflows_examples() -> str:
        """Examples for automation and workflow scenarios"""
        return """# Automation and Workflow Examples

## Ticket Escalation Workflows

### Automatic Escalation
```python
# Check for tickets requiring escalation
query = "priority:3 AND status:2 AND created_at:<'2025-09-14'"
old_urgent_tickets = await filter_tickets(query)

# Process each ticket for escalation
for ticket in old_urgent_tickets.get('tickets', []):
    await escalation_prompt(
        ticket_id=ticket['id'],
        reason="Ticket open for more than 24 hours without response",
        urgency_level="urgent"
    )
```

### SLA Breach Prevention
```python
# Identify tickets approaching SLA breach
await sla_monitoring_prompt()

# For each at-risk ticket, take preventive action
# This would be implemented as part of a scheduled job
```

## Bulk Operations

### Mass Ticket Update
```python
# Update multiple tickets based on criteria
query = "group_id:123 AND status:2"
tickets_to_update = await filter_tickets(query)

for ticket in tickets_to_update.get('tickets', []):
    await update_ticket(
        ticket_id=ticket['id'],
        ticket_fields={
            "priority": 3,  # Increase priority
            "custom_fields": {
                "bulk_update_reason": "Department restructuring"
            }
        }
    )
```

### Batch Requester Creation
```python
# Create multiple requesters from a list
new_employees = [
    {
        "first_name": "John",
        "last_name": "Doe", 
        "primary_email": "john.doe@company.com",
        "department_ids": [10]
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "primary_email": "jane.smith@company.com", 
        "department_ids": [15]
    }
]

for employee in new_employees:
    await create_requester(**employee)
```

## Notification Workflows

### Daily Summary Notifications
```python
# Generate and send daily summary
query = "created_at:>'2025-09-14' AND created_at:<'2025-09-15'"
daily_tickets = await filter_tickets(query)

summary_message = f\"\"\"
Daily Ticket Summary - {{len(daily_tickets.get('tickets', []))}} new tickets

High Priority: {{len([t for t in daily_tickets.get('tickets', []) if t.get('priority') == 3])}}
Medium Priority: {{len([t for t in daily_tickets.get('tickets', []) if t.get('priority') == 2])}}
Low Priority: {{len([t for t in daily_tickets.get('tickets', []) if t.get('priority') == 1])}}

Unassigned: {{len([t for t in daily_tickets.get('tickets', []) if not t.get('responder_id')])}}
\"\"\"

# Send to management team (implementation depends on notification method)
```

### Overdue Ticket Alerts
```python
# Alert for overdue tickets
query = "due_by:<'2025-09-15' AND status:<4"
overdue_tickets = await filter_tickets(query)

if overdue_tickets.get('tickets'):
    for ticket in overdue_tickets['tickets']:
        # Send alert notification
        await send_ticket_reply(
            ticket_id=ticket['id'],
            body="ALERT: This ticket is past its due date. Please provide immediate attention.",
            from_email="alerts@company.com"
        )
```

## Integration Workflows

### Knowledge Base Auto-Creation
```python
# Automatically create KB articles from resolved tickets
resolved_query = "status:4 AND priority:3 AND created_at:>'2025-09-01'"
resolved_tickets = await filter_tickets(resolved_query)

for ticket in resolved_tickets.get('tickets', []):
    # Get ticket conversations to extract solution
    conversations = await list_all_ticket_conversation(ticket['id'])
    
    # Use knowledge base prompt to structure the article
    await knowledge_base_prompt(
        topic=ticket['subject'],
        article_type="solution"
    )
```

### Service Request Automation
```python
# Auto-approve certain service requests
service_requests_query = "type:'Service Request' AND status:2"
service_requests = await filter_tickets(service_requests_query)

for request in service_requests.get('tickets', []):
    requested_items = await get_requested_items(request['id'])
    
    # Auto-approve low-cost items
    if should_auto_approve(requested_items):
        await update_ticket(
            ticket_id=request['id'],
            ticket_fields={
                "status": 3,  # Pending (for fulfillment)
                "custom_fields": {
                    "approval_status": "Auto-approved",
                    "approval_reason": "Low cost item under threshold"
                }
            }
        )
```

## Monitoring and Health Checks

### System Health Dashboard
```python
# Check system health metrics
open_tickets = await filter_tickets("status:2")
pending_tickets = await filter_tickets("status:3") 
overdue_tickets = await filter_tickets("due_by:<'2025-09-15' AND status:<4")

health_metrics = {
    "open_tickets": len(open_tickets.get('tickets', [])),
    "pending_tickets": len(pending_tickets.get('tickets', [])),
    "overdue_tickets": len(overdue_tickets.get('tickets', [])),
    "health_status": "healthy" if len(overdue_tickets.get('tickets', [])) < 10 else "attention_needed"
}
```

### Agent Workload Balancing
```python
# Automatically balance workload across agents
agents = await get_all_agents()

for agent in agents.get('agents', []):
    workload = await filter_tickets(f"agent_id:{agent['id']} AND status:<4")
    
    if len(workload.get('tickets', [])) > 15:  # Overloaded threshold
        # Trigger workload rebalancing
        await agent_workload_prompt(agent_id=agent['id'])
```
"""

    print("Examples module loaded successfully")
