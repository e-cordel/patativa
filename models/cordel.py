from typing import Dict
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
    ):
        self.id = id
        self.author = author
        self.title = title
        self.content = content
        self.description = description
        # TODO: implementar envio de imagem e pegar URL
        # TODO: implementar class xilogravura
        self.image_url = image_url

    def to_json(self) -> Dict:
        return {
            "title": self.title,
            "author": {"id": self.author.id if self.author.id else -1 ,
                        "name": self.author.name                        
            },
            "description": self.description,
            "published": False,
            "content": self.content,
        }

    @staticmethod
    def from_json(json_data: Dict):
        id = -1 if json_data.get('id') == None else json_data['id']

        cordel = Cordel(
            id=json_data['id'] if 'id' in json_data else -1,
            author=Author.from_json(json_data["author"]),
            content=json_data["content"],
            title=json_data["title"],
            image_url= '' if json_data.get("imageUrl") == None else json_data["imageUrl"],
        )
        return cordel
