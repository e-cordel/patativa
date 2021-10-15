import os

API_AUTH_URL = "https://ecordel-restapi.herokuapp.com/api/v1/auth"
API_URL = "https://ecordel-restapi.herokuapp.com/api/v1"

CURRENT_DIRECTORY = os.getcwd()
DESTINATION_PDF_DIR = f"{CURRENT_DIRECTORY}/cordeis-netmundi"
CORDEIS_SOURCE_DIR = f"{CURRENT_DIRECTORY}/cordeis-pdf"
TEMP_WORKDIR = f"{CURRENT_DIRECTORY}/tmp"
CORDEIS_NETMUNDI_JSON_DIR = f"{CURRENT_DIRECTORY}/cordeis-netmundi-json"
