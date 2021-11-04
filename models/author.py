from typing import Dict


class Author:
    def __init__(self, name: str, id: int = None) -> None:

        self.name = name
        self.id = -1 if id == None else id

    def to_json(self) -> Dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_json(json: Dict) -> "Author":
        return Author(id=json["id"], name=json["name"])
