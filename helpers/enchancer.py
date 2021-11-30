from PIL import Image, ImageEnhance


def enchance_image(filename: str):
    img = Image.open(filename)
    enhancer1 = ImageEnhance.Sharpness(img)
    enhancer2 = ImageEnhance.Contrast(img)
    img_edit = enhancer1.enhance(20.0)
    img_edit = enhancer2.enhance(1.5)
    img_edit.save(filename)
