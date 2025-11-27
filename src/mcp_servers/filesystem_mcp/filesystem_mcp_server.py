from mcp.server.fastmcp import FastMCP
import os
import time
from pathlib import Path
import PyPDF2

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
async def read_file(name: str) -> dict:
    """
    Read files locally
    
    """
    safe = os.path.basename(name)
    path = os.path.join(STORAGE_DIR, safe)

    if not os.path.exists(path):
        return {"error": "file not found"}

    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages.append({
                    "page": i,
                    "text": text,
                })

        return {
            "name": safe,
            "pages": len(pages),
            "content": pages,  
        }

    except Exception as e:
        return {"error": f"failed to read pdf: {e}"}

    
if __name__ == "__main__":
    mcp.run()
