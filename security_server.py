#Code Starts Here
import os
import logging
from mcp.server.fastmcp import FastMCP
# --- COMPONENT 1: AUDIT LOGGER ---
# This creates mcp_audit.log in your current directory.
logging.basicConfig(
    filename="mcp_audit.log",
    level=logging.INFO,
    format="%(asctime)s - [AUDIT] - %(message)s"
)
logger = logging.getLogger("CyberDefender")

# Initialize the MCP Server
mcp = FastMCP("SecurityAuditServer")
# --- COMPONENT 2: VULNERABLE TOOL (Phase A & B) ---
# This tool is the "Confused Deputy" because it doesn't check the path.

# --- COMPONENT 3: HARDENED TOOL (Phase C) ---
# Uncomment the lines below ONLY when you reach Phase C.
# Remember to comment out the read_log tool above when you do this.
@mcp.tool()
def secure_read_log(filename: str) -> str:
    """Hardened log reader with path sanitization and least-privilege enforcement."""
 
    # Establish the authorized boundary: the lab directory only.
    # os.path.abspath resolves any . or .. sequences to their canonical form.
    BASE_DIR = os.path.abspath(os.getcwd())
    requested_path = os.path.abspath(os.path.join(BASE_DIR, filename))
 
    # ── THE CRITICAL CHECK ─────────────────────────────────────────────────
    # After resolving all path traversal sequences, verify the resulting
    # canonical path is still inside BASE_DIR.
    # '../../../../etc/passwd' resolves to '/etc/passwd' — does NOT start
    # with BASE_DIR, so the check catches it.
    if not requested_path.startswith(BASE_DIR):
        logger.warning(f"BLOCKED PATH TRAVERSAL: requested={filename} resolved={requested_path}")
        return "ACCESS DENIED: Requested path is outside the authorized directory."
 
    logger.info(f"AUTHORIZED ACCESS: {requested_path}")
 
    if not os.path.exists(requested_path):
        return "Error: File not found within authorized directory."
 
    with open(requested_path, "r") as f:
        return f.read()


if __name__ == "__main__": mcp.run(transport="stdio")
