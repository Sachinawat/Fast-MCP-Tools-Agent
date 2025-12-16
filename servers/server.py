import os
import sys

# --- ENTERPRISE PATH FIX ---
# This block ensures that imports work correctly regardless of 
# where you run the command from.

# 1. Get the absolute path of this file (Fastmcp/servers/server.py)
current_file_path = os.path.abspath(__file__)

# 2. Get the directory containing this file (Fastmcp/servers)
servers_dir = os.path.dirname(current_file_path)

# 3. Get the project root (Fastmcp)
project_root = os.path.dirname(servers_dir)

# 4. Add project root to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# ---------------------------

# Now we can safely import from our package
try:
    from servers.mcp_app import mcp
    from servers.config import logger
except ImportError as e:
    # Print to stderr so the client sees the specific missing module
    print(f"Server Import Error: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    try:
        # Log startup to file
        logger.info("🚀 Enterprise Research MCP Server Starting...")
        
        # Run the server
        mcp.run()
        
    except Exception as e:
        logger.critical(f"🔥 Server Crash: {e}")
        # Print critical error to stderr for the client to catch
        print(f"CRITICAL SERVER FAILURE: {e}", file=sys.stderr)
        raise