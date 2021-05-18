import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 


BASE_URL = "http://docvirt.com/docreader.net/DocReader.aspx?bib=CordelFCRB&pagfis=54242"
options = Options()
# options.headless = True
firefox = webdriver.Firefox(options=options)
firefox.implicitly_wait(10)
firefox.get(BASE_URL)
time.sleep(2)
iframe = firefox.find_element_by_name("PublicidadeWnd")
firefox.switch_to.frame(iframe)
firefox.find_element_by_id("closebtn").click()
firefox.switch_to.parent_frame()





def get_autors():
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name('li')
    return autores

def click_cordel(cordel):
    pass

def get_cordels(autor_index):    
    firefox.get(BASE_URL)
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name('li')
    autor = autores[autor_index]
    autor.find_element_by_class_name("rtIn").click()
    
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name('li')
    autor = autores[autor_index]
    autor.find_element_by_class_name("rtPlus").click()
    
    pastas = firefox.find_element_by_xpath("//div[@id='PastasUpdatePanel']//div//ul")
    autores = pastas.find_elements_by_tag_name('li')
    autor = autores[autor_index]

    
    cordeis_dir = autor.find_element_by_tag_name("ul")
    cordeis = cordeis_dir.find_elements_by_tag_name("li")
    for cordel in cordeis:
        print(cordel.text)
    
    

    


autores = get_autors()


for index in range(0, len(autores)):
    get_cordels(index)


firefox.quit()