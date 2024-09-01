import os
from typing import Dict, List

from unidecode import unidecode

from api.ecordel_api import APIAuthenticator, EcordelApi, create_api
from config import API_AUTH_URL, API_URL
from helpers.file_helpers import save_json
from models.author import Author
from setup import Setup
from repositories import RepositoryNetMundi


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


def scrap_netMundi(api: EcordelApi):
    # TODO: implementar log de andamento.
    # TODO: modificar fluxo pra fazer post individual de cada cordel

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
                existent_author = search_author_by_name(
                    authors=authors_created, author=cordel.author
                )
                cordel.author = existent_author
                api.create_cordel(cordel=cordel)
        except:
            pass

if __name__ == "__main__":
    setup = Setup()
    setup.init()
    download_dir = os.getenv("DOWNLOAD_FOLDER")
    api = create_api()

    

    #scrap_netMundi(api)
    #setup.finalize()
