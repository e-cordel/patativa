import os
from typing import Dict, List

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from helpers import extract_text_from_images, parse_pdf_to_images
from models import Cordel
from models.author import Author
from repositories.repository_interface import RepositoryInterface
from selenium.webdriver.common.by import By

class RepositoryNetMundi(RepositoryInterface):
    def __init__(self) -> None:
        self.__base_url = "https://www.netmundi.org/home/2020/reliquias-do-cordel-38-obras-para-baixar/"

        options = Options()
        self.firefox = webdriver.Firefox(options=options)
        self.firefox.implicitly_wait(3)
        self.firefox.get(self.__base_url)
        self.__pdf_folder = None
        self.__json_folder = None
        self.__create_pdf_and_json_folder()

    @property
    def base_url(self):
        return self.__base_url

    def get_cordeis(self) -> List[Cordel]:
        """
        Return all cordeis in json format

        Returns:
            List['Dict']:
        """
        return self.__process_by_number()


    def __process_by_number(
        self,
    ) -> List[Cordel]:
        links = self.__get_cordeis_links()
        self.__download_pdf_cordeis(links)
        path_pdf_files = self.__get_path_pdf_files()
        cordeis = []
        count = 1
        total = len(path_pdf_files)
        for cordel_file in path_pdf_files:
            print(f"Processando [{count}/{total}]")
            try:
                cordel = self.__create_cordel_from_pdf(cordel_file)
                cordel.link_fonte = self.base_url
                cordeis.append(cordel)
                count = count + 1                
            except:
                pass
        
        print(f"Processados {count} de {total} cordeis.")
        return cordeis


    def __get_cordeis_links(self) -> List[str]:
        cordeis = self.firefox.find_elements(By.TAG_NAME, 'li') 
        links = []
        for li in cordeis:
            try:
                element = li.find_elements(By.TAG_NAME,"a")
                if element:
                    link = element.get_attribute("href")
                    if link.split(".")[-1].lower() == "pdf":
                        links.append(link)
            except:
                pass

        self.firefox.close()

        return links

    def __download_pdf_cordeis(self, links: List[str]):
        download_folder = self.__pdf_folder

        user_agent_string = UserAgent().chrome

        for link in links:
            r = requests.get(link, headers={"User-Agent": user_agent_string})
            filename = self.__create_filename_from_url(link)

            with open(f"{download_folder}/{filename}", "wb") as f:
                f.write(r.content)

            
    def __create_filename_from_url(self, url: str) -> str:
        if url.find("/"):
            return url.rsplit("/", 1)[1]


    def __extract_autor_name(self, file_path: str):
        """Extrai o nome do autor do cordel baseado no nome do arquiv.

        Args:
            file_path (str): caminho do arquivo .pdf.

        Returns:
            str: nome do autor do cordel.
        """
        import re

        filename = self.__extract_name(file_path)
        return (
            re.split(
                string=filename, pattern="Literatura-de-Cordel-por", flags=re.IGNORECASE
            )[1]
            .replace("-", " ")
            .strip()
        )

    def __extract_cordel_name(self, file_path: str) -> str:
        """
        Extrai o título/nome do cordel baseado no nome do arquivo.
        Args:
            file_path (str): caminho do arquivo .pdf

        Returns:
            str: título/nome do cordel. ex.: meu-cordel
        """
        import re

        filename = self.__extract_name(file_path)
        return (
            re.split(
                string=filename, pattern="Literatura-de-Cordel-por", flags=re.IGNORECASE
            )[0]
            .replace("-", " ")
            .strip()
        )

    def __extract_name(self, file_path: str):
        """
        Separa o nome do arquivo da extensão e retorna somente o nome do arquivo.

        Args:
            file_path (str): caminho do arquivo

        Returns:
            str: Nome do arquivo sem a extensão.
        """
        filename = file_path.split(".")[0].split("/")[-1]
        return filename


    def __get_path_pdf_files(self):
        """
        Lista todos os arquivos no diretório CORDEIS_SOURCE_DIR
        Returns:
            List[str]: Retorna uma lista com todos os arquivos no diretório.
        """
        files = os.listdir(self.__pdf_folder)
        path_pdf_files = [f"{self.__pdf_folder}/{file}" for file in files]
        return path_pdf_files

    def __create_cordel_from_pdf(self, path: str) -> Cordel:
        """ "
        Cria um objeto do tipo Cordel a partir de um pdf.
        """
        import gc

        autor_name = self.__extract_autor_name(path)
        cordel_name = self.__extract_cordel_name(path)
        images = parse_pdf_to_images(file_path=path)
        cordel_text = extract_text_from_images(images)
        cordel = Cordel(
            author=Author(name=autor_name), title=cordel_name, content=cordel_text
        )

        images = None
        autor_name = None
        cordel_name = None
        cordel_text = None
        gc.collect()
        return cordel

    def __create_pdf_and_json_folder(self) -> Dict:
        download_folder = os.getenv("DOWNLOAD_FOLDER")
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
