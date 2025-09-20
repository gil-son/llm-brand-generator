import httpx
from PIL import Image, ImageDraw
from io import BytesIO


async def generate_logo_image(prompt: str):
    """
    Generate a logo image using the Pollinations.ai API.

    Args:
        prompt (str): Text prompt describing the logo.

    Returns:
        PIL.Image: Generated image from Pollinations.ai, or a fallback
        placeholder image if the request fails.
    """
    try:
        safe_prompt = prompt.replace(" ", "_")
        print("Safe Prompt:", safe_prompt)

        # Pollinations.ai endpoint
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

        # Send request to Pollinations API
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return Image.open(BytesIO(resp.content))

    except Exception as e:
        print("⚠️ Error generating image:", e)

        # Fallback: plain white background with prompt text
        img = Image.new("RGB", (512, 512), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 250), prompt, fill="black")
        return img