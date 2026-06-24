from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from nextcloud_client import NextCloudClient
from presidio_filter import PII_filter

# Load environment variables
load_dotenv()

mcp = FastMCP("Simple NextCloud MCP Server", stateless_http=True,
              json_response=True, port=8420)

# Global clients to be populated during runtime setup
nextcloud_client: NextCloudClient = None

def init_server(entities=None, tokens=None):
    """Initializes the backend configuration pipeline before server execution."""
    global nextcloud_client
    hostname = os.getenv("HOSTNAME")
    share_token = os.getenv("SHARED_TOKEN")
    
    pii_filter = PII_filter(entities=entities, tokens=tokens)
    nextcloud_client = NextCloudClient(hostname, share_token, pii_filter)

@mcp.tool()
async def list_all_files() -> dict:
    """List available files in the NextCloud shared folder.
    WARNING: Do not pass any arguments or parameters to this tool. 
    Leave the arguments object completely empty."""
    files = await nextcloud_client.list_files()
    return {"files": files}

@mcp.tool()
async def list_all_files_detailed() -> dict:
    """A more detaild list of the files in the folder. Includes things like 
        size, modification date, etag, type, and absolute path.
        WARNING: Do not pass any arguments or parameters to this tool. 
        Leave the arguments object completely empty."""
    files = await nextcloud_client.list_files_metadata()
    return {"files": files}

@mcp.tool()
async def read_file(filename: str) -> str:
    """Reads the contents of a single file.
    
    Args:
        filename: Full file name (e.g. 2025-08050_3.1 Beslut.pdf)
    """
    return await nextcloud_client.read_file(filename)
    

@mcp.tool()
async def folder_context() -> dict[str, str]:
    """List all available files in the NextCloud shared folder. then reads 
     all of the files and sends it back in a dict with strings in order to 
     build context for the folder and all included items.
     """
    return await nextcloud_client.build_context()

def main():
    # Initialize and run the server, this is a fallback for no cli
    init_server()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()