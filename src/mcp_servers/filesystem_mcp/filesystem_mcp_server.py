from mcp.server.fastmcp import FastMCP
import os
import time
from pathlib import Path

mcp = FastMCP("Filesystem")

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage" / "docs"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

@mcp.tool()
async def list_files() -> dict:
    """
    List local files
    
    """
    files = []
    for name in os.listdir(STORAGE_DIR):
        path = os.path.join(STORAGE_DIR, name)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append({
                "name": name,
                "size": stat.st_size,
                "modified": time.ctime(stat.st_mtime)
            })
    return {"files": files}

@mcp.tool()
async def read_file(name: str, offset: int = 0, length: int = 2048) -> dict:
    """
    Read files locally
    
    """  
    safe = os.path.basename(name)
    path = os.path.join(STORAGE_DIR, safe)

    if not os.path.exists(path):
        return {"error": "file not found"}

    with open(path, "rb") as f:
        f.seek(offset)
        data = f.read(length)

    return {
        "name": safe,
        "offset": offset,
        "length": len(data),
        "content_b64": data.decode("latin1")
    }

    
if __name__ == "__main__":
    mcp.run()
