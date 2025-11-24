from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import google.genai as genai
import os
from utils import *

mcp = FastMCP("Image generator")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

IMAGE_MODEL = "gemini-2.5-flash-image"

@mcp.tool()
async def create_image(input: str) -> str:
    """
    Create image
    
    """
    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=input
        )

        for part in getattr(response, "parts", []):
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                img = inline_data.data

                file_path = save_image_locally(img)

                image_url = create_img_url(file_path)
                
                return image_url

    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

    return None

if __name__ == "__main__":
    mcp.run()
