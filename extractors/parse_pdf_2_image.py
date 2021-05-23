from typing import List
from pdf2image import convert_from_path
from helper.file_helpers import save_images
from PIL import Image, ImageEnhance


def parse_pdf_2_images(file_path: str) -> None:
    pages = convert_from_path(file_path, 600, thread_count=3)    
    return pages
