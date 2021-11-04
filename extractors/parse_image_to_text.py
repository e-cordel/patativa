from typing import List
import pytesseract as ocr


def parse_image_to_text(image, language="por") -> str:
    text = ocr.image_to_string(image, language, config="--oem 1")
    return text


def extract_text_from_images(images: List):
    full_text = ""
    for image in images:
        text = parse_image_to_text(image)
        full_text += text

    return full_text
