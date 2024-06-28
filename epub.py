# TODO: integrage this module with the project

import json
import logging
import requests

from ebooklib import epub
from PIL import Image

from config import API_URL

# logging configurations
logging.basicConfig(level=logging.NOTSET)

# constants definition
PT_BR = 'pt-BR'

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
    xilogravura = requests.get(cordel_data['xilogravuraUrl'],headers=headers).content
    with open("cover.jpg", 'wb') as f:
        f.write(xilogravura)
    cordel.set_cover("cover.jpg", open('cover.jpg', 'rb').read())

    # add cordel content
    cordel_content = cordel_data['content'].split('\n\n')
    content_xhtml = '<section epub:type="chapter">'
    content_xhtml += f"<h1>{cordel_data['title']}</h1>"

    for c in cordel_content:
        strophe = c.replace('\n', '<br/>')
        content_xhtml += f"<p>{strophe}</p>"

    content_xhtml += "</section>"

    create_content(cordel_data['title'], content_xhtml, 'content.xhtml', cordel, toc)

    # Add author section
    author_xhtml = '<section epub:type="chapter">'
    author_xhtml += f"<h1>{author_data['name']}</h1>"
    author_xhtml += f"<p>{author_data['about']}</p>"
    author_xhtml += f"<p>E-mail: <span>{author_data['email']}</span></p>"
    author_xhtml += "</section>"

    create_content('Sobre o autor', author_xhtml, 'author.xhtml', cordel, toc)

    # Add e-cordel section
    ecordel_xhtml = """<section epub:type="chapter">
    <h1>Sobre o e-cordel</h1>
    <p>E-cordel é um projeto de código aberto sem fins lucrativos criado no Cariri Cearense, 
    com intuito de preservar a literatura de cordel e potencializar a sua divulgação através da internet.</p>
    <p>Dessa forma, foi desenvolvida uma plataforma para registro e catalogação de cordéis digitais que pode ser acessada gratuitamente.</p>
    <p>Essa obra é também disponibilizada como um ebook para garantir que pessoas com necessidades especiais possam desfrutar também da literatura de cordel.</p>
    </section>
    """
    create_content('Sobre o e-cordel', ecordel_xhtml, 'ecordel.xhtml', cordel, toc)

    cordel.toc = tuple(toc)
    cordel.spine = ['nav', *nav]

    # EPUB2 compatibility
    cordel.add_item(epub.EpubNcx())
    cordel.add_item(epub.EpubNav())

    # write to the file
    epub.write_epub(f"epub/{cordel_data['title']}.epub", cordel)
    logging.info(f"new epub created {cordel_data['title']}.epub")

# get published cordels
logging.info("loading cordels...")
published_cordels = json.loads(requests.get(f'{API_URL}/cordels/summaries?title=&published&size=30').text)

for summary in published_cordels['content']:
    logging.info(f"creating epub for {summary['title']}")
    create_epub(summary['id'])

logging.info("all epubs created successfully")
