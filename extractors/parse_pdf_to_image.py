from pdf2image import convert_from_path


def parse_pdf_to_images(file_path: str):
    image_list = convert_from_path(file_path, 600, thread_count=3)
    return image_list
