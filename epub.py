# TODO: integrage this module with the project

import ftplib
import json
import logging
import os
import requests
import subprocess

from api.ecordel_api import create_api
from config import API_URL
from ebooklib import epub
from unidecode import unidecode

# logging configurations
logging.basicConfig(level=logging.NOTSET)

# constants definition
PT_BR = 'pt-BR'
HOSTNAME = "ftp.turismonocariri.com.br"
USERNAME = os.environ.get("FTP_USERNAME").replace('\r', '')
PASSWORD = os.environ.get("FTP_PASSWORD").replace('\r', '')
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# request configuration
# it is necessary to avoid 406 error code when requesting the xilogravura image
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

# create content
def create_content(title: str, xhtml: str, file_name: str, cordel, toc):
    logging.info(f"creating content: {file_name}")

    content = epub.EpubHtml(title=title, file_name=file_name, lang=PT_BR)
    content.set_content(xhtml)
    cordel.add_item(content)
    toc.append(epub.Link(file_name, title, file_name))
    return content

def create_epub(id: int):
    logging.info(f"loading cordel with id {id}")

    toc = []
    nav = []
    cordel_data = json.loads(requests.get(f'{API_URL}/cordels/{id}').text)
    logging.info(f"cordel {cordel_data['title']} loaded")

    cordel = epub.EpubBook()
    cordel.set_identifier(f"{cordel_data['id']}")
    cordel.set_title(cordel_data['title'])
    cordel.set_language(PT_BR)

    author_data = cordel_data['author']
    cordel.add_author(f"{author_data['name']}")
    cordel.add_metadata('DC', 'description', cordel_data['description'])

    # add cover image
    logging.info(f"downloading xilogravura: {cordel_data['xilogravuraUrl']}")
    file_name = cordel_data['xilogravuraUrl'].split('/')[-1]
    xilogravura = requests.get(cordel_data['xilogravuraUrl'],headers=headers).content
    with open(file_name, 'wb') as f:
        f.write(xilogravura)
    cordel.set_cover(file_name, open(file_name, 'rb').read())

    # add cordel content
    cordel_content = cordel_data['content'].split('\n\n')
    content_xhtml = '<section epub:type="chapter">'
    content_xhtml += f"<h1>{cordel_data['title']}</h1>"

    for c in cordel_content:
        strophe = c.replace('\n', '<br/>')
        content_xhtml += f"<p>{strophe}</p>"

    content_xhtml += "</section>"

    content = create_content(cordel_data['title'], content_xhtml, 'content.xhtml', cordel, toc)
    nav.append(content)

    # Add author section
    author_xhtml = '<section epub:type="chapter">'
    author_xhtml += f"<h1>{author_data['name']}</h1>"
    author_xhtml += f"<p>{author_data['about']}</p>"
    author_xhtml += f"<p>E-mail: <span>{author_data['email']}</span></p>"
    author_xhtml += "</section>"

    author = create_content('Sobre o autor', author_xhtml, 'author.xhtml', cordel, toc)
    nav.append(author)

    # Add e-cordel section
    ecordel_xhtml = """<section epub:type="chapter">
    <h1>Sobre o e-cordel</h1>
    <p>E-cordel é um projeto de código aberto sem fins lucrativos criado no Cariri Cearense, 
    com intuito de preservar a literatura de cordel e potencializar a sua divulgação através da internet.</p>
    <p>Dessa forma, foi desenvolvida uma plataforma para registro e catalogação de cordéis digitais que pode ser acessada gratuitamente.</p>
    <p>Essa obra é também disponibilizada como um ebook para garantir que pessoas com necessidades especiais possam desfrutar também da literatura de cordel.</p>
    </section>
    """
    ecordel = create_content('Sobre o e-cordel', ecordel_xhtml, 'ecordel.xhtml', cordel, toc)
    nav.append(ecordel)

    cordel.toc = tuple(toc)
    cordel.spine = ['nav', *nav]

    # EPUB2 compatibility
    cordel.add_item(epub.EpubNcx())
    cordel.add_item(epub.EpubNav())

    # write contents to the file
    normalized_name = str(cordel_data['title']).lower().replace(' ','-')
    epub_file = f"epub/{unidecode(normalized_name)}.epub"
    epub.write_epub(epub_file, cordel)
    logging.info(f"new epub created {epub_file}")
    return epub_file

def validate_epub(epub_file: str):
    logging.info(f"validating epub {epub_file}...")
    epub_check_jar = 'epubcheck-5.1.0/epubcheck.jar'
    if not os.path.exists(epub_check_jar):
        r = requests.get('https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip')
        with open("epubcheck.zip", 'wb') as f:
            f.write(r.content)
        subprocess.run(['unzip', '-a', 'epubcheck.zip'])

    subprocess.run(['java','-jar', epub_check_jar, epub_file])

def upload_epub(epub_file: str):
    logging.info(f"uploading cordel {epub_file}...")
    ftp_server.encoding = "utf-8"
    
    with open(epub_file, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR {epub_file.split('/')[1]}", file)

    return f"https://ebooks.ecordel.com.br/{epub_file.split('/')[1]}"

# get published cordels
logging.info("loading cordels...")
ecordel_api = create_api()
# TODO use api module to fetch data
published_cordels = json.loads(requests.get(f'{API_URL}/cordels/summaries?title=&published&size=30').text)
missing_epubs = [3, 5, 15, 25, 29, 20, 39, 27, 38]

#for idx, summary in enumerate(published_cordels['content']):
#    logging.info(f"creating epub {idx+1}/{len(published_cordels)} for {summary['title']}")
#    id = summary['id']
for id in missing_epubs:
    epub_file = create_epub(id)
    validate_epub(epub_file)
    epub_link = upload_epub(epub_file)
    epub_link = f"https://ebooks.ecordel.com.br/{epub_file.split('/')[1]}"
    ecordel_api.set_ebook_url(cordel_id=id,ebook_url=epub_link)
    logging.info(f"epub {id} created\n")

ftp_server.quit()
logging.info("all epubs created successfully")
