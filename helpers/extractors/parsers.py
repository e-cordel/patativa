from pdf2image import convert_from_path
from typing import List
import pytesseract as ocr
from PIL import Image


def parse_image_to_text(image: Image, language="por") -> str:
    text = ocr.image_to_string(image, language, config="--oem 1")
    return text


def extract_text_from_images(images: List):
    full_text = ""
    for image in images:
        text = parse_image_to_text(image)
        full_text += text

    return full_text


def parse_pdf_to_images(file_path: str):
    image_list = convert_from_path(file_path, 600, thread_count=3)
    return image_list
