import time
import os
import json
import requests
from fake_useragent import UserAgent

from typing import List
from models import Cordel
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import unidecode

from selenium.webdriver.support import expected_conditions as EC

# from .repository_interface import RepositoryInterface


class RepositoryNetMundi():
    def __init__(self) -> None:
        base_url = "https://www.netmundi.org/home/2020/reliquias-do-cordel-38-obras-para-baixar/"
        CURRENT_DIRECTORY = os.getcwd()

        options = Options()
        self.firefox = webdriver.Firefox(options=options)
        self.firefox.implicitly_wait(3)
        self.firefox.get(base_url)

    def get_cordeis(self):
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

    def download_cordeis(self, links):
        ua_str = UserAgent().chrome

        for link in links:
            r = requests.get(link, headers={"User-Agent": ua_str})
            filename = self.get_filename(link)

            with open(filename, "wb") as f:
                f.write(r.content)

    def get_filename(self, url):
        if url.find("/"):
            return url.rsplit("/", 1)[1]
