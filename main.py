import os
from typing import Dict, List

from unidecode import unidecode

from api.ecordel_api import APIAuthenticator, EcordelApi
from config import API_AUTH_URL, API_URL
from helpers.file_helpers import save_json
from models.author import Author


def create_api() -> EcordelApi:
    """
    Cria uma instância do tipo EcordelApi pronta para uso.

    Returns:
        EcordelAPI: Instância da API pronta para uso.
    """
    api_username = os.environ.get("API_USERNAME")
    api_password = os.environ.get("API_PASSWORD")
    api_authenticator = APIAuthenticator(
        username=api_username, password=api_password, endpoint_url_auth=API_AUTH_URL
    )

    session = api_authenticator.authenticate()
    api = EcordelApi(sesssion=session, api_base_url=API_URL)
    return api


def create_all_authors(authors: List[Author], api: EcordelApi, created_authors: Dict):

    for author in authors:
        all_autors = [name.lower() for name in created_authors.keys()]
        if author.name.lower() not in all_autors:
            new_author = api.create_author(author)
            created_authors[f"{author.name}"] = new_author.id

    return created_authors


def author_exists(authors: List[Author], author: Author):

    author_names = [unidecode(author.name.lower()) for author in authors]

    if unidecode(author.name.lower()) in author_names:
        return True
    else:
        return False

def search_author_by_name(authors: List[Author], author: Author):
    for a in authors:
        if unidecode(a.name.lower()) == unidecode(author.name.lower()):
            return a
    
    return None



# def step_1():
#     # Para recadastrar os autores, deixar epenas {} no arquivo autores_cadastrados.json
#     cordeis = return_all_cordels_from_json_files()
#     autores = []
#     api = create_api()
#     autores_cadastrados = file_helpers.load_json("autores_cadastrados.json")

#     for cordel in cordeis:
#         autores.append(cordel.author)

#     autores_cadastrados = create_all_authors(autores, api=api, authors_created=autores_cadastrados)

#     file_helpers.save_json(autores_cadastrados,"autores_cadastrados.json" )


from repositories import RepositoryNetMundi
from setup import Setup

if __name__ == "__main__":
    setup = Setup()
    setup.init()
    download_dir = os.getenv("DOWNLOAD_FOLDER")
    api = create_api()
    repository = RepositoryNetMundi()
    cordeis = repository.get_cordeis()
    authors_created = []

    
    for cordel in cordeis:
        try:
            if not author_exists(authors=authors_created, author=cordel.author):
                new_author = api.create_author(author=cordel.author)
                authors_created.append(new_author)
                cordel.author = new_author
                api.create_cordel(cordel=cordel)
            else:
                existent_author = search_author_by_name(authors=authors_created,author=cordel.author)
                cordel.author = existent_author
                api.create_cordel(cordel=cordel)
        except:
            pass
    
    # setup.finalize()
