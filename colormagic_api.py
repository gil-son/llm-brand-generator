import httpx
from PIL import Image, ImageDraw, ImageFont


async def generate_slogan_palette(slogan: str, query: str):
    """
    Fetch a color palette from the ColorMagic API and create
    an image with the slogan displayed on top of it.

    Args:
        slogan (str): The slogan text to overlay on the palette.
        query (str): Keyword to search for a matching palette.

    Returns:
        tuple: (PIL.Image, palette_name, palette_colors)
            - PIL.Image: Image with palette background and slogan text.
            - palette_name (str): The palette description returned by the API.
            - palette_colors (list[str]): List of hex color codes.
    """
    try:
        url = f"https://colormagic.app/api/palette/search?q={query}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            palettes = resp.json()

        if not palettes:
            raise ValueError("No palette found.")

        # Use the first palette from results
        palette = palettes[0]["colors"]
        text = palettes[0]["text"]

        width, height = 600, 400
        block_width = width // len(palette)
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        # Draw palette blocks side by side
        for i, color in enumerate(palette):
            draw.rectangle(
                [i * block_width, 0, (i + 1) * block_width, height],
                fill=color
            )

        # Load font (fallback to default if missing)
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()

        # Center the slogan text
        bbox = draw.textbbox((0, 0), slogan, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (width - text_w) // 2
        y = (height - text_h) // 2
        draw.text((x, y), slogan, font=font, fill="black")

        return img, text, palette

    except Exception as e:
        print("⚠️ Error generating image:", e)
        # Fallback: plain white background with slogan
        img = Image.new("RGB", (512, 512), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 250), slogan, fill="black")
        return img, "fallback", ["#ffffff"]