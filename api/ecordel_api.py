
from typing import Dict, Type
import requests
from models.cordel import Author
from models import Cordel


class APISession:
    def __init__(self, token: str, auth_method: str, expires_at: str) -> None:
        self.token = token
        self.auth_method = auth_method
        self.expires_at = expires_at

    @staticmethod
    def from_json(data: Dict):
        return APISession(**data)


class APIAuthenticator:

    def __init__(self, username: str, password: str, api_url: str) -> None:
        self.username = username
        self.password = password
        self.api_url = api_url

    def authenticate(self) -> APISession:

        body = {"username": self.username, "password": self.password}

        response = requests.post(url=self.api_url, json=body)

        token = response.json()["token"]
        auth_method = response.json()["authenticationMethod"]
        expires_at = response.json()["expiresAt"]
        api_session = APISession(
            token=token, auth_method=auth_method, expires_at=expires_at
        )
        return api_session


class EcordelApi:
    def __init__(self, api_session: APISession, api_url: str) -> None:
        self.api_session = api_session
        self.api_url = api_url

    def create_author(self, author: Author) -> Author:
        endpoint = "authors"
        endpoint_url = f"{self.api_url}/{endpoint}"

        body = author.to_json()

        response = requests.post(
            headers={"Authorization": f"Bearer {self.api_session.token}"},
            url=endpoint_url, json=body)
        
        if response.status_code == 201:
            location = response.headers['Location']
            author_id = self.__extract_resource_id(location=location)
            new_author = Author(id=author_id, name=author.name)
            return new_author
        else:
            raise Exception('Erro ao Criar autor.')

    def create_cordel(self, cordel: Cordel) -> Cordel:
        """
        Cria um novo cordel na API. 

        Args:
            cordel (Cordel): Um cordel completo, incluindo o autor  com ID.

        Raises:
            Exception: Retorna uma exception caso haja algum erro ao cadastrar o cordel.

        Returns:
            Cordel: Retorna uma instância de um cordel com ID.
        """

        endpoint = "cordels"
        endpoint_url = f"{self.api_url}/{endpoint}"

        body = cordel.to_json()

        response = requests.post(
            headers={"Authorization": f"Bearer {self.api_session.token}"},
            url=endpoint_url, json=body)

        if response.status_code == 201:
            location = response.headers['Location']
            new_cordel_id = self.__extract_resource_id(location=location)
            cordel.id = new_cordel_id
            return cordel
        else:
            raise Exception('Erro ao criar o cordel.')


    def create_xilogravura(self, xilogravura):
        pass


    def __extract_resource_id(self, location=str):
        id = location.split("/")[-1]
        return id
        

