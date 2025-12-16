import asyncio
import os
import sys
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add parent dir to path to find imports if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

console = Console()

class EnterpriseClient:
    def __init__(self):
        self.session_id = "sess_001"
        # Calculate absolute path to server.py to avoid "file not found" errors
        self.server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '../servers/server.py'))

    def determine_intent(self, user_query):
        """
        Simple Router Logic (In prod, use a lightweight LLM call here)
        """
        user_query = user_query.lower()
        
        # 1. Routing Logic
        if any(x in user_query for x in ['calc', 'solve', '+', '*', 'physics', 'math']):
            return "math_agent", {"expression": user_query.replace("solve", "").strip(), "session_id": self.session_id}
        
        elif "log" in user_query or "history" in user_query:
            return "audit_tool", {"action": "view", "session_id": self.session_id}
        
        # 2. Master Orchestrator for complex queries
        elif "and" in user_query or "then" in user_query:
            return "orchestrator_main", {"complex_query": user_query, "session_id": self.session_id}
        

        elif any(x in user_query for x in ['stock', 'price', 'market', 'share']):
            # Simple extraction: assume the last word is the ticker or prompt for it
            # For this simple demo, we pass the whole query or hardcode extraction
            # A better way is to regex extract the ticker, e.g., "AAPL"
            import re
            words = user_query.split()
            ticker = words[-1] # Naive extraction: "price of AAPL" -> "AAPL"
            return "finance_agent", {"ticker": ticker, "session_id": self.session_id}
            
        else:
            return "research_agent", {"query": user_query, "session_id": self.session_id}

    async def run(self):
        console.print(Panel.fit("[bold cyan]Enterprise Research OS[/bold cyan]\n[dim]Orchestrator Active[/dim]", style="blue"))

        # --- CRITICAL FIXES FOR WINDOWS/VENV ---
        server_params = StdioServerParameters(
            command=sys.executable, # Uses the CURRENT venv python, not global python
            args=["-u", self.server_script], # '-u' forces unbuffered output (vital for MCP)
            env=os.environ.copy()
        )
        # ---------------------------------------

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Verify tools loaded
                    tools = await session.list_tools()
                    console.print(f"[green]✓ Connected to Server. Loaded {len(tools.tools)} tools.[/green]")

                    while True:
                        query = Prompt.ask("\n[bold green]Request[/bold green]")
                        if query.lower() in ["exit", "quit"]:
                            break

                        # 1. Orchestration Step (Router)
                        tool_name, args = self.determine_intent(query)
                        
                        console.print(f"[dim]⚡ Routing to agent: [bold]{tool_name}[/bold]...[/dim]")

                        # 2. Execution Step (FastMCP)
                        try:
                            result = await session.call_tool(tool_name, arguments=args)
                            
                            # Handle potential empty content
                            if not result.content:
                                console.print("[red]No content returned from tool.[/red]")
                                continue

                            output_text = result.content[0].text
                            
                            # 3. Visualization Step
                            if tool_name == "audit_tool":
                                # Parse JSON and show table
                                try:
                                    data = json.loads(output_text.replace("'", '"'))
                                    table = Table(title="Audit Logs")
                                    table.add_column("Tool", style="cyan")
                                    table.add_column("Timestamp", style="magenta")
                                    
                                    # Handle case where logs might be empty or dict
                                    if isinstance(data, list):
                                        for row in data:
                                            table.add_row(str(row.get('tool', 'N/A')), str(row.get('timestamp', 'N/A')))
                                        console.print(table)
                                    else:
                                        console.print(data)
                                except:
                                    console.print(output_text)
                            else:
                                # Render Markdown/Text
                                console.print(Panel(Markdown(output_text), title=f"Result: {tool_name}", border_style="green"))
                                
                        except Exception as e:
                            console.print(f"[bold red]Tool Execution Error:[/bold red] {e}")
        
        except Exception as e:
            console.print(Panel(f"[bold red]CRITICAL CONNECTION ERROR[/bold red]\n\n{str(e)}\n\nCheck logs/system_events.log for server details.", border_style="red"))

if __name__ == "__main__":
    client = EnterpriseClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\nShutting down...")