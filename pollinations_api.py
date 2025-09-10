import requests
from PIL import Image
from io import BytesIO

def generate_slogan_image(prompt: str):
    """
    Generate an image for the slogan using Pollinations.ai.
    Falls back to a simple placeholder if request fails.
    """
    try:
        safe_prompt = prompt.replace(" ", "_")
        url = f"https://pollinations.ai/p/{safe_prompt}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        # fallback: return white placeholder with slogan text
        from PIL import ImageDraw
        img = Image.new("RGB", (512, 512), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 250), prompt, fill="black")
        return img