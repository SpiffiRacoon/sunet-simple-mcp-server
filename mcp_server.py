from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from nextcloud_client import NextCloudClient

# Load environment variables
load_dotenv()

mcp = FastMCP("Simple NextCloud MCP Server", stateless_http=True,
              json_response=True)

# Initialize NextCloud client with the shared folder URL
NEXTCLOUD_HOSTNAME = os.getenv("HOSTNAME")
NEXTCLOUD_SHARE_URL = os.getenv("SHARED_LINK")
NEXTCLOUD_SHARE_TOKEN = os.getenv("SHARED_TOKEN")
nextcloud_client = NextCloudClient(NEXTCLOUD_SHARE_URL, NEXTCLOUD_HOSTNAME,
                                   NEXTCLOUD_SHARE_TOKEN)

@mcp.tool()
async def list_all_files() -> dict:
    """List available files in the NextCloud shared folder.
    WARNING: Do not pass any arguments or parameters to this tool. 
    Leave the arguments object completely empty."""
    files = nextcloud_client.list_files()
    return {"files": files}

@mcp.tool()
async def list_all_files_detailed() -> dict:
    """A more detaild list of the files in the folder. Includes things like 
        size, modification date, etag, type, and absolute path.
        WARNING: Do not pass any arguments or parameters to this tool. 
        Leave the arguments object completely empty."""
    files = nextcloud_client.list_files_metadata()
    return {"files": files}

@mcp.tool()
async def read_file(filename: str) -> str:
    """Reads the contents of a single file.
    
    Args:
        filename: Full file name (e.g. 2025-08050_3.1 Beslut.pdf)
    """
    file_content = nextcloud_client.read_file(filename)
    return (file_content)

def main():
    # Initialize and run the server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()