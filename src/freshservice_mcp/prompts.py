"""
Freshservice MCP Server Prompts

This module contains all the prompts for the Freshservice MCP server.
Prompts provide pre-written templates and instructions for common operations.
"""

from fastmcp import FastMCP
from typing import Optional, Dict, Any, List


def register_prompts(mcp: FastMCP):
    """Register all prompts with the MCP server instance"""
    
    @mcp.prompt()
    async def create_ticket_prompt(
        subject: str,
        description: str,
        priority: str = "medium",
        requester_email: Optional[str] = None
    ) -> str:
        """Generate a prompt for creating a new support ticket in Freshservice.
        
        Args:
            subject: The ticket subject/title
            description: Detailed description of the issue
            priority: Priority level (low, medium, high, urgent)
            requester_email: Email of the person requesting support
        """
        priority_map = {
            "low": "1",
            "medium": "2", 
            "high": "3",
            "urgent": "4"
        }
        
        priority_value = priority_map.get(priority.lower(), "2")
        
        prompt = f"""I need to create a support ticket in Freshservice with the following details:

**Subject:** {subject}

**Description:** {description}

**Priority:** {priority} (value: {priority_value})

**Source:** Email (value: 1)

**Status:** Open (value: 2)
"""
        
        if requester_email:
            prompt += f"\n**Requester Email:** {requester_email}"
        else:
            prompt += "\n**Note:** Please specify the requester email address"
            
        prompt += """

Please use the create_ticket tool with these parameters:
- subject: "{subject}"
- description: "{description}" 
- source: 1 (Email)
- priority: {priority_value}
- status: 2 (Open)
- email: "{requester_email}" (if provided)

Would you like me to create this ticket now?"""
        
        return prompt

    @mcp.prompt()
    async def ticket_analysis_prompt(ticket_id: int) -> str:
        """Generate a prompt for analyzing a specific ticket and its details.
        
        Args:
            ticket_id: The ID of the ticket to analyze
        """
        return f"""Please analyze ticket #{ticket_id} in Freshservice and provide a comprehensive summary including:

1. **Basic Information:**
   - Ticket subject and description
   - Current status and priority
   - Requester details
   - Assigned agent/group
   - Creation and last update dates

2. **Ticket History:**
   - All conversations and replies
   - Status changes
   - Priority changes
   - Assignment changes

3. **Analysis:**
   - Time since creation
   - Response time metrics
   - Resolution progress
   - Any escalations or delays

4. **Recommendations:**
   - Next steps for resolution
   - Priority adjustments if needed
   - Additional resources or expertise required

Please start by fetching the ticket details using get_ticket_by_id({ticket_id}) and then gather conversation history using list_all_ticket_conversation({ticket_id})."""

    @mcp.prompt()
    async def bulk_ticket_report_prompt(
        status: Optional[str] = None,
        priority: Optional[str] = None,
        agent_id: Optional[int] = None,
        days_back: int = 7
    ) -> str:
        """Generate a prompt for creating a bulk ticket report with filtering options.
        
        Args:
            status: Filter by status (open, pending, resolved, closed)
            priority: Filter by priority (low, medium, high, urgent)  
            agent_id: Filter by assigned agent ID
            days_back: Number of days to look back (default: 7)
        """
        status_map = {
            "open": "2",
            "pending": "3", 
            "resolved": "4",
            "closed": "5"
        }
        
        priority_map = {
            "low": "1",
            "medium": "2",
            "high": "3", 
            "urgent": "4"
        }
        
        filters = []
        query_parts = []
        
        if status:
            status_value = status_map.get(status.lower())
            if status_value:
                query_parts.append(f"status:{status_value}")
                filters.append(f"Status: {status}")
                
        if priority:
            priority_value = priority_map.get(priority.lower())
            if priority_value:
                query_parts.append(f"priority:{priority_value}")
                filters.append(f"Priority: {priority}")
                
        if agent_id:
            query_parts.append(f"agent_id:{agent_id}")
            filters.append(f"Agent ID: {agent_id}")
            
        # Add date filter for last N days
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        date_filter = f"created_at:>'{start_date.strftime('%Y-%m-%d')}'"
        query_parts.append(date_filter)
        filters.append(f"Created in last {days_back} days")
        
        query = " AND ".join(query_parts)
        filter_text = ", ".join(filters) if filters else "No filters applied"
        
        return f"""Generate a comprehensive ticket report for Freshservice with the following criteria:

**Filters Applied:** {filter_text}

        **Query String:** {query}

**Report Should Include:**
1. **Summary Statistics:**
   - Total number of tickets
   - Breakdown by status
   - Breakdown by priority
   - Average resolution time
   - Tickets by agent/group

2. **Detailed Analysis:**
   - Oldest unresolved tickets
   - High priority tickets requiring attention
   - Tickets approaching SLA deadlines
   - Most common issue categories

3. **Actionable Insights:**
   - Bottlenecks in the workflow
   - Resource allocation recommendations
   - Process improvement suggestions

Please start by using filter_tickets with the query: {query} and then analyze the results to generate this comprehensive report."""

    @mcp.prompt()
    async def escalation_prompt(
        ticket_id: int,
        reason: str,
        urgency_level: str = "high"
    ) -> str:
        """Generate a prompt for escalating a ticket with proper documentation.
        
        Args:
            ticket_id: The ID of the ticket to escalate
            reason: Reason for escalation
            urgency_level: Level of urgency (medium, high, urgent)
        """
        return f"""TICKET ESCALATION REQUEST - #{ticket_id}

**Escalation Reason:** {reason}

**Urgency Level:** {urgency_level.upper()}

**Required Actions:**

1. **Update Ticket Priority:**
   - Current ticket needs priority review
   - Recommended priority: {urgency_level}
   - Use update_ticket tool to adjust priority if needed

2. **Add Escalation Note:**
   - Document the escalation reason
   - Include timeline and impact assessment
   - Use create_ticket_note tool to add detailed escalation note

3. **Notify Stakeholders:**
   - Prepare escalation notification
   - Include current status and required actions
   - Use send_ticket_reply tool to notify relevant parties

4. **Documentation Required:**
   - What troubleshooting steps have been attempted?
   - What is the business impact?
   - What resources are needed for resolution?
   - What is the expected timeline?

**Escalation Note Template:**
```
ESCALATION NOTICE - {urgency_level.upper()} PRIORITY

Reason for Escalation: {reason}

Current Status: [To be filled based on ticket analysis]
Business Impact: [To be assessed]
Steps Taken: [To be documented]
Required Resources: [To be identified]
Expected Resolution Timeline: [To be estimated]

Escalated by: System
Escalation Date: [Current timestamp]
```

Please proceed with:
1. Analyzing the current ticket status using get_ticket_by_id({ticket_id})
2. Adding the escalation note using create_ticket_note
3. Updating priority if necessary using update_ticket
4. Sending escalation notification using send_ticket_reply"""

    @mcp.prompt()
    async def knowledge_base_prompt(
        topic: str,
        article_type: str = "solution"
    ) -> str:
        """Generate a prompt for searching or creating knowledge base content.
        
        Args:
            topic: The topic to search for or create content about
            article_type: Type of content (solution, procedure, faq)
        """
        return f"""KNOWLEDGE BASE OPERATION - {topic}

**Topic:** {topic}
**Content Type:** {article_type}

**Search Strategy:**
1. **Search Existing Content:**
   - Look through solution categories using get_all_solution_category
   - Search solution articles for related content
   - Check for existing procedures or FAQs

2. **Content Analysis:**
   - Identify gaps in current documentation
   - Find outdated or incomplete articles
   - Locate related topics that could be linked

3. **Content Creation (if needed):**
   - Determine appropriate category and folder
   - Create comprehensive article covering:
     * Problem description
     * Step-by-step solution
     * Prerequisites and requirements
     * Troubleshooting tips
     * Related articles and resources

**Recommended Actions:**
1. Search existing knowledge base for "{topic}"
2. If content exists: Review and suggest updates
3. If content missing: Propose new article structure
4. Identify the best category and folder for placement
5. Create draft content following best practices

**Article Template for "{topic}":**
```
Title: [Clear, descriptive title]

Description:
- Brief overview of the topic
- When to use this solution
- Expected outcome

Prerequisites:
- System requirements
- User permissions needed
- Tools or resources required

Step-by-Step Instructions:
1. [Detailed steps]
2. [With screenshots if applicable]
3. [Including error handling]

Troubleshooting:
- Common issues and solutions
- Error messages and fixes
- When to escalate

Related Articles:
- Link to related procedures
- Reference materials
- Contact information for experts
```

Please start by searching the knowledge base for existing content related to "{topic}"."""

    @mcp.prompt()
    async def agent_workload_prompt(agent_id: Optional[int] = None) -> str:
        """Generate a prompt for analyzing agent workload and performance.
        
        Args:
            agent_id: Specific agent ID to analyze (optional)
        """
        if agent_id:
            return f"""AGENT WORKLOAD ANALYSIS - Agent #{agent_id}

**Analysis Scope:** Individual Agent Performance

**Required Data Collection:**
1. **Agent Information:**
   - Get agent details using get_agent({agent_id})
   - Agent profile, role, and group assignments
   - Contact information and availability

2. **Current Workload:**
   - Active tickets assigned to agent
   - Use filter_tickets with query: "agent_id:{agent_id} AND status:<5"
   - Categorize by priority and age

3. **Performance Metrics:**
   - Tickets resolved in last 30 days
   - Average resolution time
   - Customer satisfaction scores (if available)
   - Response time metrics

4. **Workload Distribution:**
   - Compare with team averages
   - Identify overloaded or underutilized agents
   - Skill set alignment with ticket types

**Analysis Report Should Include:**
- Current ticket count and priority breakdown
- Overdue tickets and SLA compliance
- Workload compared to team average
- Recommendations for workload balancing
- Training or support needs identified

Please start by gathering the agent information and current ticket assignments."""
        else:
            return """TEAM WORKLOAD ANALYSIS - All Agents

**Analysis Scope:** Complete Team Performance Overview

**Required Data Collection:**
1. **Team Overview:**
   - Get all agents using get_all_agents()
   - Agent groups and their members
   - Team structure and hierarchy

2. **Workload Distribution:**
   - Active tickets per agent
   - Queue distribution across teams
   - Priority distribution analysis

3. **Performance Comparison:**
   - Resolution rates by agent
   - Response time metrics
   - SLA compliance rates
   - Customer satisfaction trends

4. **Resource Planning:**
   - Identify bottlenecks
   - Skill gap analysis
   - Training requirements
   - Capacity planning recommendations

**Deliverables:**
1. Executive summary of team performance
2. Individual agent performance cards
3. Workload balancing recommendations
4. Resource allocation suggestions
5. Process improvement opportunities

Please start by collecting the team information and analyzing current ticket distribution."""

    @mcp.prompt()
    async def sla_monitoring_prompt(
        workspace_id: Optional[int] = None,
        priority_level: Optional[str] = None
    ) -> str:
        """Generate a prompt for monitoring SLA compliance and identifying at-risk tickets.
        
        Args:
            workspace_id: Specific workspace to monitor (optional)
            priority_level: Focus on specific priority level (optional)
        """
        query_parts = ["status:<4"]  # Open and pending tickets only
        
        if priority_level:
            priority_map = {"low": "1", "medium": "2", "high": "3", "urgent": "4"}
            if priority_level.lower() in priority_map:
                query_parts.append(f"priority:{priority_map[priority_level.lower()]}")
        
        query = " AND ".join(query_parts)
        workspace_text = f" in workspace {workspace_id}" if workspace_id else ""
        priority_text = f" with {priority_level} priority" if priority_level else ""
        
        return f"""SLA MONITORING AND COMPLIANCE REPORT{workspace_text}{priority_text}

**Monitoring Scope:**
- Active tickets (open and pending status)
{f"- Workspace: {workspace_id}" if workspace_id else "- All workspaces"}
{f"- Priority Level: {priority_level}" if priority_level else "- All priority levels"}

**SLA Analysis Required:**

1. **At-Risk Tickets Identification:**
   - Tickets approaching SLA deadlines
   - Overdue tickets past SLA targets
   - High-priority tickets requiring immediate attention

2. **Response Time Analysis:**
   - First response time compliance
   - Time to resolution metrics
   - Escalation timeline adherence

3. **Breach Prevention:**
   - Early warning system for approaching deadlines
   - Resource reallocation recommendations
   - Priority adjustment suggestions

4. **Compliance Reporting:**
   - SLA compliance percentage by priority
   - Breach analysis and root causes
   - Trend analysis over time

**Query for Analysis:** {query}

**Action Plan:**
1. **Immediate Actions (Next 2 Hours):**
   - Identify tickets breaching SLA in next 2 hours
   - Alert responsible agents and managers
   - Escalate critical issues

2. **Short-term Actions (Today):**
   - Review tickets due today
   - Reallocate resources if needed
   - Update ticket priorities as required

3. **Medium-term Planning (This Week):**
   - Analyze SLA breach patterns
   - Identify process improvements
   - Plan resource adjustments

**Automated Monitoring Setup:**
- Set up alerts for SLA breaches
- Create dashboard for real-time monitoring
- Establish escalation procedures

Please start by filtering tickets using the query above and analyzing their SLA status."""

    print("Prompts module loaded successfully")
