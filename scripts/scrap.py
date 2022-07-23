import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://docvirt.com/docreader.net/DocReader.aspx?bib=CordelFCRB&pagfis=54242"
options = Options()

firefox = webdriver.Firefox(options=options)
firefox.implicitly_wait(10)
firefox.get(BASE_URL)
iframe = firefox.find_element_by_name("PublicidadeWnd")
firefox.switch_to.frame(iframe)
time.sleep(3)
firefox.find_element_by_id("closebtn").click()
firefox.switch_to.parent_frame()


def get_autors():
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name("li")
    return autores


def click_cordel(cordel):
    pass


def get_cordels(autor_index):
    firefox.get(BASE_URL)
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name("li")
    autor = autores[autor_index]
    autor.find_element_by_class_name("rtIn").click()

    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name("li")
    autor = autores[autor_index]
    autor.find_element_by_class_name("rtPlus").click()

    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name("li")
    autor = autores[autor_index]

    cordeis_dir = autor.find_element_by_tag_name("ul")
    cordeis = cordeis_dir.find_elements_by_tag_name("li")
    for cordel in cordeis:
        print(cordel.text)


autores = get_autors()


for index in range(0, len(autores)):

    get_cordels(index)
    time.sleep(3)


firefox.quit()
