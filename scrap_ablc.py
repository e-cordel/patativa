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
firefox.implicitly_wait(2)
firefox.get(BASE_URL)


def get_cordels_url():
    links = []
    cards = firefox.find_elements_by_class_name("panel-grid-cell")

    for card in cards:
        try:
            link = card.find_element_by_tag_name("a")
            links.append(link.get_attribute('href'))
        except:
            pass
    return links


def get_titulo():
    titulo_element = firefox.find_element_by_id('single-head')
    titulo = titulo_element.find_element_by_tag_name("h1")
    return titulo.text


def get_autor():
    artigos = firefox.find_elements_by_tag_name("article")
    textos = artigos[1].find_elements_by_tag_name("p")
    autor = textos[0]
    return autor.text


def get_texto():
    texto_completo = ''
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
    return filename.split('.')[-1]


def download_cordel_image(image_url,
                          path_dir: str,
                          image_name: str):
    if image_url is None:
        return

    file_extension = get_file_extension(image_url)
    path_file = path_dir + "/" + image_name + f".{file_extension}"
    r = requests.get(image_url, allow_redirects=True)
    with open(path_file, 'wb') as file:
        file.write(r.content)

    


def create_cordel_dir(path_dir):
    os.mkdir(path_dir)


def normatize_name_dir(name):
    return unidecode.unidecode(name).lower().replace(' ', '-').replace("\n", "-")


def save_to_json_file(filename, path_dir, cordel: Cordel):
    data = cordel.to_json()
    complete_path = path_dir + "/" + filename

    with open(complete_path, 'w', encoding="utf-8-sig") as json_file:
        json.dump(data, json_file, ensure_ascii=False)

# PROCESSAMENTO


cordeis_urls = get_cordels_url()
cordeis_list = []

for url in cordeis_urls[0:2]:
    # for link in links[0:2]:
    firefox.get(url)
    image_url = get_image_url()
    autor = get_autor()
    titulo = get_titulo()
    texto = get_texto()

    novo_cordel = Cordel(autor=autor,
                         titulo=titulo,
                         texto=texto,
                         image_url=image_url
                         )

    cordeis_list.append(novo_cordel)


for cordel in cordeis_list:
    name_dir = normatize_name_dir(cordel.autor)
    file_name = name_dir + ".json"
    path_dir = CORDEIS_SALVOS + "/" + name_dir
    
    create_cordel_dir(path_dir)
    
    save_to_json_file(filename=file_name,
                      path_dir=path_dir,
                      cordel=cordel)
    nome_da_capa = name_dir + "-capa"
    
    
    download_cordel_image(
        cordel.image_url, path_dir=path_dir, image_name=nome_da_capa)


# print(cordeis_list[0].texto)

firefox.quit()
