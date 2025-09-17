import httpx
from PIL import Image, ImageDraw, ImageFont

async def generate_slogan_palette(slogan: str, query: str):
    """
    Busca uma paleta de cores do ColorMagic e cria uma imagem com o slogan sobre ela.
    """
    try:
        url = f"https://colormagic.app/api/palette/search?q={query}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            palettes = resp.json()

        if not palettes:
            raise ValueError("Nenhuma paleta encontrada.")

        palette = palettes[0]["colors"]
        text = palettes[0]["text"]

        width, height = 600, 400
        block_width = width // len(palette)
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        for i, color in enumerate(palette):
            draw.rectangle(
                [i * block_width, 0, (i + 1) * block_width, height],
                fill=color
            )

        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), slogan, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x = (width - text_w) // 2
        y = (height - text_h) // 2
        draw.text((x, y), slogan, font=font, fill="black")

        return img, text, palette

    except Exception as e:
        print("⚠️ Erro ao gerar imagem:", e)
        img = Image.new("RGB", (512, 512), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 250), slogan, fill="black")
        return img, "fallback", ["#ffffff"]