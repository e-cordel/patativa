from typing import Dict


class Cordel:
    def __init__(
            self, autor: str,
            titulo: str,
            texto: str,
            image_url: str = None):

        self.autor = autor
        self.titulo = titulo
        self.texto = texto
        self.image_url = image_url
    
    def to_json(self) -> Dict:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "texto": self.texto
        }
        