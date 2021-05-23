from models.author import Author
from typing import List, Dict
import json
from models import Cordel


def save_images(pages: List, destination_dir: str) -> None:
    for page in pages:
        index = pages.index(page)
        page.save(f"{destination_dir}/out{index}.jpg", "JPEG")

def save_json(data: dict, file_path: str):
    with open(file_path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False)

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_cordel_json(filename, path_dir, cordel: Cordel):
    data = cordel.to_json()
    complete_path = path_dir + "/" + filename

    with open(complete_path, "w", encoding="utf-8-sig") as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def load_cordel_from_json_file(file_path: str) -> Cordel:
    json_data = load_json(file_path=file_path)
    cordel = Cordel.from_json(json_data)
    return cordel

