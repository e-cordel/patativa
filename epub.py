import json
import logging
import requests

from ebooklib import epub
from PIL import Image

# logging configurations
logging.basicConfig(level=logging.NOTSET)

# request configuration
# it is necessary to avoid 406 error code when requesting the xilogravura image
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

url = "https://api.ecordel.com.br/api/v1/cordels/38"
data = json.loads(requests.get(url).text)

logging.info(f"cordel {data['title']} loaded")

cordel = epub.EpubBook()

cordel.set_identifier(f"{data['id']}")
cordel.set_title(data['title'])
cordel.set_language('pt-BR')


cordel.add_author(f"{data['author']['name']}")
cordel.add_metadata('DC', 'description', data['description'])

# add cover image
logging.info(f"downloading xilogravura: {data['xilogravuraUrl']}")
xilogravura = requests.get(data['xilogravuraUrl'],headers=headers).content
with open("cover.jpg", 'wb') as f:
    f.write(xilogravura)
cordel.set_cover("cover.jpg", open('cover.jpg', 'rb').read())

# create content
logging.info("creating content")
content = epub.EpubHtml(title=data['title'],
                   file_name='content.xhtml',
                   lang='pt')

cordelContent = data['content'].split('\n\n')
xhtmlContent = ""
for c in cordelContent:
    strophe = c.replace('\n', '<br/>')
    xhtmlContent += f"<p>{strophe}</p>"

content.set_content(xhtmlContent)

cordel.add_item(content)

cordel.toc = (epub.Section('Content'), content)
cordel.spine = ['nav', content]

cordel.add_item(epub.EpubNcx())
cordel.add_item(epub.EpubNav())


epub.write_epub(f"{data['title']}.epub", cordel)
