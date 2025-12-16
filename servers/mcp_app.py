from mcp.server.fastmcp import FastMCP
from servers.tools import research_rag, math_science, analytics,finance_tool
from servers.tools.orchestrator import manager as orchestrator_manager
from servers.config import log_audit, logger

# Initialize FastMCP Server
mcp = FastMCP("EnterpriseOrchestrator")

@mcp.tool()
def orchestrator_main(complex_query: str, session_id: str = "default") -> str:
    """
    MASTER AGENT: Use this for complex or ambiguous queries.
    It automatically plans steps, decides whether to use research or math, 
    and synthesizes the final answer.
    """
    logger.info(f"Session {session_id}: Orchestrator invoked for '{complex_query}'")
    
    # Delegate to the AgentOrchestrator class
    result = orchestrator_manager.execute_workflow(complex_query, session_id)
    
    # Audit is handled inside the orchestrator steps, but we log the high-level intent here
    log_audit(session_id, "orchestrator_main", complex_query, "Workflow Completed")
    
    return str(result)

@mcp.tool()
def research_agent(query: str, session_id: str = "default") -> str:
    """
    Specific Tool: Performs RAG-based research. 
    Use this when you ONLY need to search documentation or facts 
    without any calculation or complex planning.
    """
    try:
        result = research_rag.execute_research(query)
        output_str = str(result)
        log_audit(session_id, "research_agent", query, output_str)
        return output_str
    except Exception as e:
        return f"Research Error: {str(e)}"

@mcp.tool()
def math_agent(expression: str, session_id: str = "default") -> str:
    """
    Specific Tool: Solves Physics and Math problems.
    Input must be a mathematical expression (e.g., '5.972e24 / 2' or 'sin(pi/4)').
    """
    try:
        result = math_science.execute_math(expression)
        output_str = str(result)
        log_audit(session_id, "math_agent", expression, output_str)
        return output_str
    except Exception as e:
        return f"Math Error: {str(e)}"

@mcp.tool()
def audit_tool(action: str = "view", session_id: str = "default") -> str:
    """
    Specific Tool: Retrieves system logs and interaction history.
    Useful for 'show me what happened' queries.
    """
    try:
        result = analytics.get_logs()
        return str(result)
    except Exception as e:
        return f"Audit Error: {str(e)}"
    

# 3. ADD THIS NEW FUNCTION
@mcp.tool()
def finance_agent(ticker: str, session_id: str = "default") -> str:
    """
    Get stock market data. Input should be a ticker symbol (e.g., AAPL, TSLA).
    """
    try:
        result = finance_tool.get_stock_price(ticker)
        output = str(result)
        
        # Log it to SQL for audit
        log_audit(session_id, "finance_agent", ticker, output)
        
        return output
    except Exception as e:
        return f"Finance Error: {str(e)}"
