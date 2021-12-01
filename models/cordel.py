from typing import Dict, Type

from .author import Author


class Cordel:
    def __init__(
        self,
        author: Author,
        title: str,
        content: str,
        description: str = None,
        image_url: str = None,
        id: int = None,
        link_fonte: str = None,
    ):
        self.id = id
        self.author = author
        self.title = title
        self.content = content
        self.description = description
        self.image_url = image_url
        self.link_fonte = link_fonte

        # TODO: implementar envio de imagem e pegar URL
        # TODO: implementar class xilogravura

    def to_json(self) -> Dict:
        if self.link_fonte:
            content = self.content + f"\n\nFonte: {self.link_fonte}\n"
        else:
            content = self.content

        return {
            "title": self.title,
            "author": {
                "id": self.author.id if self.author.id else -1,
                "name": self.author.name,
            },
            "description": self.description,
            "published": False,
            "content": content,
            "fonte": self.link_fonte if self.link_fonte else "",
        }

    @staticmethod
    def from_json(json_data: Dict) -> Type["Cordel"]:
        id = -1 if json_data.get("id") == None else json_data["id"]

        cordel = Cordel(
            id=json_data["id"] if "id" in json_data else -1,
            author=Author.from_json(json_data["author"]),
            content=json_data["content"],
            title=json_data["title"],
            image_url=""
            if json_data.get("imageUrl") == None
            else json_data["imageUrl"],
        )
        return cordel
