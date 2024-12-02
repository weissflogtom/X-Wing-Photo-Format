"""Module providing the functions to get an Image from a Weblink 
and convert it into photoformated Image ready to print."""
from io import BytesIO
import requests
from PIL import Image


def _load_image(url: str) -> Image:
    """Takes a String url of a X-Wing card and returns Pillow Image object"""
    response = requests.get(url, timeout=(5, 60))
    return Image.open(BytesIO(response.content))


def _check_oriantation(img: Image) -> Image:
    """Checks if the card is sideways and rotates 90° if necessary."""
    width, height = img.size
    if width > height:
        return img.rotate(90, expand=True)
    return img

def _check_ratio(img: Image, target_ratio = 700 / 503) -> Image:
    """Standardcards should be 8.9x6.1cm"""
    width, height = img.size
    if width / height != target_ratio:
        return img.resize((width, round(width * target_ratio)))
    return img

def _get_mask(width: int, height: int) -> Image:
    """Is used to create an Image 9x13cm based on the Cards Pixels Per Inch"""
    return Image.new('RGB', (width, height))

def _add_img_to_mask(mask: Image, img: Image, spacing: int) -> Image:
    width, height = img.size
    mask.paste(img)
    mask.paste(img, (width + spacing, 0))
    return mask

def get_photo(url: str, width_ratio = 1034 / 503, height_ratio = 716 / 700, target_ratio = 700 / 503, spacing = 3) -> Image:
    """Takes a String url of a X-Wing card and returns a 9x13 Photo - ready to print."""
    img = _load_image(url)
    img = _check_oriantation(img)
    img = _check_ratio(img, target_ratio)
    width, height = img.size
    mask = _get_mask(round(width * width_ratio), round(height * height_ratio))
    
    return _add_img_to_mask(mask, img, spacing)


