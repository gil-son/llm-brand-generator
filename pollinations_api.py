import httpx
from PIL import Image, ImageDraw
from io import BytesIO

async def generate_logo_image(prompt: str):
    """
    Generate an image for the slogan using Pollinations.ai.
    Falls back to a simple placeholder if request fails.
    """
    try:
        safe_prompt = prompt.replace(" ", "_")
        print("Safe Prompt: ",safe_prompt)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}"  # ✅ nova URL
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return Image.open(BytesIO(resp.content))
    except Exception as e:
        print("⚠️ Erro ao gerar imagem:", e)
        img = Image.new("RGB", (512, 512), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 250), prompt, fill="black")
        return img