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
# from helper import file_helpers
from models import Cordel


# MOVIDO PRA SETUP ENVIRONMENT
# def clear_tmp_dir():
#     """
#     Apaga todos os arquivos que estão no diretório de trabalho TEMP_WORKDIR
#     """
#     files = os.listdir(TEMP_WORKDIR)
#     for file in files:
#         os.remove(f"{TEMP_WORKDIR}/{file}")


# MOVIDO PRA REPOSITORY NETMUNDI
# def list_pdf_paths():
#     """
#     Lista todos os arquivos no diretório CORDEIS_SOURCE_DIR
#     Returns:
#         List[str]: Retorna uma lista com todos os arquivos no diretório.
#     """
#     files = os.listdir(CORDEIS_SOURCE_DIR)
#     file_paths = [f"{CORDEIS_SOURCE_DIR}/{file}" for file in files]
#     return file_paths

# MOVIDO PRA REPOSITORY NETMUNDI
# def extract_name(file_path: str):
#     """
#     Separa o nome do arquivo da extensão e retorna somente o nome do arquivo.

#     Args:
#         file_path (str): caminho do arquivo

#     Returns:
#         str: Nome do arquivo sem a extensão.
#     """
#     filename =  file_path.split(".")[0].split("/")[-1]
#     return filename

# MOVIDO PRA REPOSITORY NETMUNDI
# def extract_autor_name(file_path: str):
#     """ Extrai o nome do autor do cordel baseado no nome do arquiv.

#     Args:
#         file_path (str): caminho do arquivo .pdf.

#     Returns:
#         str: nome do autor do cordel.
#     """
#     import re
#     filename = extract_name(file_path)
#     return re.split(string=filename,pattern="Literatura-de-Cordel-por",flags=re.IGNORECASE)[1].replace("-", " ").strip()

# MOVIDO PRA REPOSITORY NETMUNDI
# def extract_cordel_name(file_path: str) -> str:
#     """
#     Extrai o título/nome do cordel baseado no nome do arquivo.
#     Args:
#         file_path (str): caminho do arquivo .pdf

#     Returns:
#         str: título/nome do cordel. ex.: meu-cordel
#     """
#     import re
#     filename = extract_name(file_path)
#     return re.split(string=filename,pattern="Literatura-de-Cordel-por", flags=re.IGNORECASE)[0].replace("-", " ").strip()


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

# MOVIDO PRA REPOSITORY NETMUNDI
# def create_cordel_from_path(path: str) -> Cordel:
#     """"
#     Cria um objeto do tipo Cordel a partir de um pdf.
#     """
#     import gc
#     autor_name = extract_autor_name(path)
#     cordel_name = extract_cordel_name(path)
#     images = parse_pdf_to_images(file_path=path)
#     cordel_text = extract_text_from_images(images)
#     cordel = Cordel(author=Author(name=autor_name),
#                     title=cordel_name,
#                     content=cordel_text)
    
#     images = None
#     autor_name = None
#     cordel_name = None
#     cordel_text = None
#     gc.collect()
#     return cordel


# MOVIDO PRA REPOSITORY NETMUNDI
# def create_json_filename(cordel: Cordel) -> str:
#     """
#     Cria um padrão de nome com a extensão em .json baseado no título do cordel.

#     Args:
#         cordel (Cordel): [description]

#     Returns:
#         str: nome do arquivo json. Ex.: meu-cordel.json
#     """
#     filename = cordel.title.replace(' ', '-')
#     return filename + ".json"

# MOVIDO PRA REPOSITORY NETMUNDI
# def parse_pdfs_to_json():
#     """
#     Lê cada cordel em PDF em um diretório, parseia e salva em um arquivo json.
#     """
#     pdf_paths = list_pdf_paths()  
#     for pdf_path in pdf_paths:
#         try:
#             cordel = create_cordel_from_path(path=pdf_path)
#             file_helpers.save_cordel_json(
#                 cordel=cordel,
#                 filename=create_json_filename(cordel),
#                 path_dir=CORDEIS_NETMUNDI_JSON_DIR
#             )
            
#         except:            
#             pass

# MOVIDO PRA REPOSITORY NETMUNDI
# def return_all_cordels_from_json_files() -> List[Cordel]:
#     cordeis_files = os.listdir(CORDEIS_NETMUNDI_JSON_DIR)
#     cordeis = []
#     for file in cordeis_files:
#         file_path = f'{CORDEIS_NETMUNDI_JSON_DIR}/{file}'
#         cordel_loaded = file_helpers.load_cordel_from_json_file(file_path)
#         cordeis.append(cordel_loaded)
    
#     return cordeis

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


def step_1():
    # Para recadastrar os autores, deixar epenas {} no arquivo autores_cadastrados.json
    cordeis = return_all_cordels_from_json_files()
    autores = []
    api = create_api()
    autores_cadastrados = file_helpers.load_json("autores_cadastrados.json")

    for cordel in cordeis:
        autores.append(cordel.author)
    
    autores_cadastrados = create_all_authors(autores, api=api, authors_created=autores_cadastrados)

    file_helpers.save_json(autores_cadastrados,"autores_cadastrados.json" )

def step_2():
      
    
    clear_tmp_dir()
    api = create_api()
    autores_cadastrados = file_helpers.load_json("autores_cadastrados.json")
    cordeis = return_all_cordels_from_json_files()
    for cordel in cordeis:
        author_id = autores_cadastrados[cordel.author.name]
        cordel.description = f"Cordel {cordel.title} por {cordel.author.name}"
        cordel.author.id = author_id
        cordel.link_fonte = "https://www.netmundi.org/home/2020/reliquias-do-cordel-38-obras-para-baixar/"
        api.create_cordel(cordel)
    

from setup import Setup
from repositories import RepositoryNetMundi
if __name__ == "__main__":
    setup = Setup()
    setup.setup()
    

    netmundi_repository = RepositoryNetMundi()
    cordeis = netmundi_repository.get_cordeis()
    print(cordeis)
    
    # setup.tear_down()