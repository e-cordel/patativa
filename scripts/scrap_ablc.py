import time
import os
import json
import requests
from typing import List
from models import Cordel
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unidecode

from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://www.ablc.com.br/o-cordel/cordeis-digitalizados/"
CURRENT_DIRECTORY = os.getcwd()
CORDEIS_SALVOS = CURRENT_DIRECTORY + "/cordeis-salvos"

options = Options()
firefox = webdriver.Firefox(options=options)
firefox.implicitly_wait(3)
firefox.get(BASE_URL)


def get_cordels_url():
    links = []
    cards = firefox.find_elements_by_class_name("panel-grid-cell")

    for card in cards:
        try:
            link = card.find_element_by_tag_name("a")
            links.append(link.get_attribute("href"))
        except:
            pass
    return links


def get_titulo():
    titulo_element = firefox.find_element_by_id("single-head")
    titulo = titulo_element.find_element_by_tag_name("h1")
    return titulo.text


def get_autor():
    artigos = firefox.find_elements_by_tag_name("article")
    textos = artigos[1].find_elements_by_tag_name("p")
    autor = textos[0]
    return autor.text


def get_texto():
    texto_completo = ""
    artigos = firefox.find_elements_by_tag_name("article")
    textos = artigos[1].find_elements_by_tag_name("p")

    # Exclui o nome do autor [0] e links para redes sociais [-1]
    for texto in textos[1:-1]:
        estrofe = texto.text
        estrofe += "\n"
        estrofe = "\n" + estrofe
        texto_completo = texto_completo + estrofe

    return texto_completo


def get_image_url():
    artigo = firefox.find_elements_by_tag_name("article")[1]
    try:
        image_element = artigo.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("src")

    except:
        image_url = None

    return image_url


def get_file_extension(filename):
    return filename.split(".")[-1]


def download_cordel_image(image_url, path_dir: str, image_name: str):
    if image_url is None:
        return

    file_extension = get_file_extension(image_url)
    path_file = path_dir + "/" + image_name + f".{file_extension}"
    r = requests.get(image_url, allow_redirects=True)
    with open(path_file, "wb") as file:
        file.write(r.content)


def create_dir(path_dir):
    try:
        os.mkdir(path_dir)
    except FileExistsError:
        return


def normatize_name_dir(name):
    return unidecode.unidecode(name).lower().replace(" ", "-").replace("\n", "-")


def save_to_json_file(filename, path_dir, cordel: Cordel):
    data = cordel.to_json()
    complete_path = path_dir + "/" + filename

    with open(complete_path, "w", encoding="utf-8-sig") as json_file:
        json.dump(data, json_file, ensure_ascii=False)


# PROCESSAMENTO


cordeis_urls = get_cordels_url()
cordeis_list = []

for url in cordeis_urls:
    # for link in links[0:2]:
    firefox.get(url)
    image_url = get_image_url()
    autor = get_autor()
    titulo = get_titulo()
    texto = get_texto()

    novo_cordel = Cordel(autor=autor, titulo=titulo, texto=texto, image_url=image_url)

    cordeis_list.append(novo_cordel)


for cordel in cordeis_list:

    autor_name_dir = normatize_name_dir(cordel.autor)
    cordel_name_dir = normatize_name_dir(cordel.titulo)

    json_file_name = cordel_name_dir + ".json"
    autor_path_dir = CORDEIS_SALVOS + "/" + autor_name_dir
    cordel_path_dir = autor_path_dir + "/" + cordel_name_dir

    create_dir(autor_path_dir)
    create_dir(cordel_path_dir)

    save_to_json_file(filename=json_file_name, path_dir=cordel_path_dir, cordel=cordel)
    nome_da_capa = cordel_name_dir + "-capa"

    download_cordel_image(
        cordel.image_url, path_dir=cordel_path_dir, image_name=nome_da_capa
    )


firefox.quit()
