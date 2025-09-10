# craiyon_api.py
from PIL import Image, ImageDraw

def generate_slogan_image(prompt: str) -> Image.Image:
    """
    Gera uma imagem simples com o texto do slogan escrito.
    (Placeholder: não usa modelo pesado)
    """
    img = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 250), prompt, fill="black")
    return img
