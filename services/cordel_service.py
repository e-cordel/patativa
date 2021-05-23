from models import Cordel
from repositories import EcordelApi


class CordelService:
    def __init__(self, ecordel_api: EcordelApi) -> None:
        self.token = None
        self.ecordel_api = ecordel_api

    def create_cordel(self, cordel: Cordel):
        """
        1. precisar token
        2. cadastrar autor (ou não)
        3. cadastrar cordel
        """
        pass

    def autenticate(self):
        self.token = self.ecordel_api.authenticate()
