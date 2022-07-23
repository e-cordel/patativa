from typing import Dict, List, Type

import requests
from requests.api import head

from models import Cordel
from models.cordel import Author


class APISession:
    def __init__(self, token: str, auth_method: str, expires_at: str) -> None:
        self.token = token
        self.auth_method = auth_method
        self.expires_at = expires_at

    @staticmethod
    def from_json(data: Dict):
        return APISession(**data)


class APIAuthenticator:
    def __init__(self, username: str, password: str, endpoint_url_auth: str) -> None:
        self.username = username
        self.password = password
        self.api_url = endpoint_url_auth

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
    def __init__(self, sesssion: APISession, api_base_url: str) -> None:
        self.session = sesssion
        self.api_url = api_base_url

    def get_authors(
        self,
    ) -> List[Author]:
        raise NotImplementedError

    def create_author(self, author: Author) -> Author:
        endpoint = "authors"
        endpoint_url = f"{self.api_url}/{endpoint}"
        body = author.to_json()
        headers = {"Authorization": f"Bearer {self.session.token}"}

        response = requests.post(
            headers=headers,
            url=endpoint_url,
            json=body,
        )

        if response.status_code == 201:
            author_id = self.__extract_id_from_response(response)
            new_author = Author(id=author_id, name=author.name)
            return new_author
        else:
            raise Exception("Erro ao Criar novo Autor.")

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
        headers = {"Authorization": f"Bearer {self.session.token}"}

        response = requests.post(headers=headers, url=endpoint_url, json=body)

        if response.status_code == 201:
            cordel_id = self.__extract_id_from_response(response)
            cordel.id = cordel_id
            return cordel
        else:
            raise Exception("Erro ao criar o cordel.")

    def create_xilogravura(self, xilogravura):
        pass

    def __extract_id_from_response(self, response, location=str):
        location = response.headers["Location"]
        id = location.split("/")[-1]
        return id
