from models.author import Author
import os
from api import ecordel_api
from api.ecordel_api import APIAuthenticator
from api.ecordel_api import EcordelApi
from api.ecordel_api import APISession

from typing import Dict, List, Set
from config import DESTINATION_PDF_DIR
from config import TEMP_WORKDIR
from config import CORDEIS_SOURCE_DIR
from config import API_AUTH_URL
from config import API_URL
from config import CORDEIS_NETMUNDI_JSON_DIR
from models import Cordel



def create_api() -> EcordelApi:
    """
    Cria uma instância do tipo EcordelApi pronta para uso.

    Returns:
        EcordelAPI: Instância da API pronta para uso.
    """
    api_username = os.environ.get('API_USERNAME')
    api_password = os.environ.get('API_PASSWORD')
    api_authenticator = APIAuthenticator(
        username=api_username,
        password=api_password,
        endpoint_url_auth=API_AUTH_URL)

    api_session = api_authenticator.authenticate()
    api = EcordelApi(api_session=api_session, api_base_url=API_URL)
    return api




def create_all_authors(authors: List[Author] ,api: EcordelApi, authors_created: Dict):
    
    for author in authors:
        all_autors = [name.lower() for name in authors_created.keys()]
        if author.name.lower() not in all_autors:
            new_author = api.create_author(author)
            authors_created[f'{author.name}'] = new_author.id
    
    return authors_created

def author_exists(authors: List[Author], author: Author):
    authors_keys = [name.lower() for name in authors.keys()]
    
    if author.name.lower() in authors_keys:
        return True
    else:
        return False


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

# def step_2():
      
    
#     clear_tmp_dir()
#     api = create_api()
#     autores_cadastrados = file_helpers.load_json("autores_cadastrados.json")
#     cordeis = return_all_cordels_from_json_files()
#     for cordel in cordeis:
#         author_id = autores_cadastrados[cordel.author.name]
#         cordel.description = f"Cordel {cordel.title} por {cordel.author.name}"
#         cordel.author.id = author_id
#         cordel.link_fonte = "https://www.netmundi.org/home/2020/reliquias-do-cordel-38-obras-para-baixar/"
#         api.create_cordel(cordel)
    

from setup import Setup
from repositories import RepositoryNetMundi
if __name__ == "__main__":
    setup = Setup()
    setup.setup()
    api = create_api()
    repository = RepositoryNetMundi()
    cordeis = repository.get_cordeis()

    for cordel in cordeis:
        pass

    setup.tear_down()