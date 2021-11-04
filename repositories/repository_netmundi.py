import json
import os
import time
from typing import Dict, List

import requests
import unidecode
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from models import Cordel
from repositories.repository_interface import RepositoryInterface


class RepositoryNetMundi(RepositoryInterface):
    def __init__(self) -> None:
        base_url = "https://www.netmundi.org/home/2020/reliquias-do-cordel-38-obras-para-baixar/"

        options = Options()
        self.firefox = webdriver.Firefox(options=options)
        self.firefox.implicitly_wait(3)
        self.firefox.get(base_url)
        self.__pdf_folder = None
        self.__json_folder = None
        self.__create_pdf_and_json_folder()

    def __create_pdf_and_json_folder(self) -> Dict:
        download_folder = os.getenv('DOWNLOAD_FOLDER')
        pdf_folder = f"{download_folder}/pdf"
        json_folder = f"{download_folder}/json"

        try:
            os.mkdir(pdf_folder)
            self.__pdf_folder = pdf_folder
        except FileExistsError:
            self.__pdf_folder = pdf_folder

        try:
            os.mkdir(json_folder)
            self.__json_folder = json_folder
        except FileExistsError:
            self.__json_folder = json_folder

    def step_1():
        # Para recadastrar os autores, deixar epenas {} no arquivo autores_cadastrados.json
        cordeis = return_all_cordels_from_json_files()
        autores = []
        api = create_api()
        autores_cadastrados = file_helpers.load_json(
            "autores_cadastrados.json")

        for cordel in cordeis:
            autores.append(cordel.author)

        autores_cadastrados = create_all_authors(
            autores, api=api, authors_created=autores_cadastrados)

        file_helpers.save_json(autores_cadastrados, "autores_cadastrados.json")

    def __process(
        self,
    ):
        links = self.__get_cordeis_links()
        self.download_pdf_cordeis(links)
        path_pdf_files = self.get_path_pdf_files()
        cordeis = self.create_cordel_from_path()

    def get_cordeis(self) -> List[Cordel]:
        self.__process()

    def __get_cordeis_links(self) -> List[str]:
        cordeis = self.firefox.find_elements_by_tag_name("li")
        links = []
        for li in cordeis:
            try:
                element = li.find_element_by_tag_name("a")
                if element:
                    link = element.get_attribute("href")
                    if link.split(".")[-1].lower() == "pdf":
                        links.append(link)
            except:
                pass

        self.firefox.close()

        return links

    def download_pdf_cordeis(self, links: List[str]):
        download_folder = self.__pdf_folder

        user_agent_string = UserAgent().chrome

        for link in links:
            r = requests.get(link, headers={"User-Agent": user_agent_string})
            filename = self.get_filename(link)

            with open(f"{download_folder}/{filename}", "wb") as f:
                f.write(r.content)
                # TODO: remover break após finalizar implementação do repositório
                break

    def get_filename(self, url):
        if url.find("/"):
            return url.rsplit("/", 1)[1]

    def extract_name(file_path: str):
        """
        Separa o nome do arquivo da extensão e retorna somente o nome do arquivo.

        Args:
            file_path (str): caminho do arquivo

        Returns:
            str: Nome do arquivo sem a extensão.
        """
        filename = file_path.split(".")[0].split("/")[-1]
        return filename

    def extract_autor_name(self, file_path: str):
        """ Extrai o nome do autor do cordel baseado no nome do arquiv.

        Args:
            file_path (str): caminho do arquivo .pdf.

        Returns:
            str: nome do autor do cordel.
        """
        import re
        filename = extract_name(file_path)
        return re.split(string=filename, pattern="Literatura-de-Cordel-por", flags=re.IGNORECASE)[1].replace("-", " ").strip()

    def extract_cordel_name(file_path: str) -> str:
        """
        Extrai o título/nome do cordel baseado no nome do arquivo.
        Args:
            file_path (str): caminho do arquivo .pdf

        Returns:
            str: título/nome do cordel. ex.: meu-cordel
        """
        import re
        filename = extract_name(file_path)
        return re.split(string=filename, pattern="Literatura-de-Cordel-por", flags=re.IGNORECASE)[0].replace("-", " ").strip()

    def get_path_pdf_files(self):
        """
        Lista todos os arquivos no diretório CORDEIS_SOURCE_DIR
        Returns:
            List[str]: Retorna uma lista com todos os arquivos no diretório.
        """
        files = os.listdir(self.__pdf_folder)
        path_pdf_files = [f"{self.__pdf_folder}/{file}" for file in files]
        return path_pdf_files

    def create_cordel_from_path(self, path: str) -> Cordel:
        """"
        Cria um objeto do tipo Cordel a partir de um pdf.
        """
        import gc
        autor_name = extract_autor_name(path)
        cordel_name = extract_cordel_name(path)
        images = parse_pdf_to_images(file_path=path)
        cordel_text = extract_text_from_images(images)
        cordel = Cordel(author=Author(name=autor_name),
                        title=cordel_name,
                        content=cordel_text)

        images = None
        autor_name = None
        cordel_name = None
        cordel_text = None
        gc.collect()
        return cordel

    def create_json_filename(cordel: Cordel) -> str:
        """
        Cria um padrão de nome com a extensão em .json baseado no título do cordel.

        Args:
            cordel (Cordel): [description]

        Returns:
            str: nome do arquivo json. Ex.: meu-cordel.json
        """
        filename = cordel.title.replace(' ', '-')
        return filename + ".json"

    def parse_pdfs_to_json():
        """
        Lê cada cordel em PDF em um diretório, parseia e salva em um arquivo json.
        """
        pdf_paths = list_pdf_paths()
        for pdf_path in pdf_paths:
            try:
                cordel = create_cordel_from_path(path=pdf_path)
                file_helpers.save_cordel_json(
                    cordel=cordel,
                    filename=create_json_filename(cordel),
                    path_dir=CORDEIS_NETMUNDI_JSON_DIR
                )

            except:
                pass

    def return_all_cordels_from_json_files() -> List[Cordel]:
        cordeis_files = os.listdir(CORDEIS_NETMUNDI_JSON_DIR)
        cordeis = []
        for file in cordeis_files:
            file_path = f'{CORDEIS_NETMUNDI_JSON_DIR}/{file}'
            cordel_loaded = file_helpers.load_cordel_from_json_file(file_path)
            cordeis.append(cordel_loaded)

        return cordeis
