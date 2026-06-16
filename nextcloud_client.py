import os
from webdav3.client import Client
from typing import List, Dict
import tempfile
import sys
import pymupdf4llm

class NextCloudClient:
    def __init__(self, share_url: str, share_host: str, share_token: str):
        """Initialize NextCloud client with the share URL."""
        self.share_url = share_url
        self.webdav_options = {
            'webdav_hostname': share_host,
            'webdav_login': share_token,  # Token from the share URL
            'webdav_password': '',
            'webdav_root': 'public.php/dav/files/'+share_token,
        }
        self.client = Client(self.webdav_options)
        
    def list_files(self) -> List[str]:
        """List all files in the shared folder."""
        try:
            files = self.client.list()
            return [f for f in files if not f.endswith('/')]  # Filter out directories
        except Exception as e:
            sys.stderr.write(f"Error listing files: {e}")
            return ["error, unable to read files"]

    def read_file(self, file_path: str) -> str:
        """Read the content of a file from NextCloud."""
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                self.client.download_file(file_path, temp_file.name)
                if file_path.endswith('.pdf'):
                    # pymupdf4llm is on the heavier side. might need to consider swapping
                    content = pymupdf4llm.to_markdown(temp_file.name)
                else:
                    with open(temp_file.name, 'r') as f:
                        content = f.read()
                os.unlink(temp_file.name)
                return content
        except Exception as e:
            sys.stderr.write(f"Error reading file {file_path}: {e}")
            return "Error when reading file."
    
    def build_context(self) -> Dict[str, str]:
        """Build context from all files in the folder."""
        context = {}
        files = self.list_files()
        for file_path in files:
            content = self.read_file(file_path)
            context[file_path] = content
        return context