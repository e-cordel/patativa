import os
from typing import List
import uuid

import pytesseract as ocr
from PIL import Image


def parse_image_to_text(image, language="por") -> str:
    text = ocr.image_to_string(image, language, config="--oem 1")
    return text


def extract_full_text(images: List):
    full_text = ""
    for image in images:
        text = parse_image_to_text(image)
        full_text += text

    return full_text


# def parse_image_2_text(image_path: str, language='por') -> str:
#     image = Image.open(os.path.join(image_path))
#     text = ocr.image_to_string(image, language, config="--oem 1")
#     return text.split('\n')
