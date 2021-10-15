# from pdf2image import convert_from_path
# pages = convert_from_path('/home/regis/Downloads/francisco-sales.pdf', 500,thread_count=3 )


# for page in pages:
#     index = pages.index(page)
#     page.save(f'out{index}.jpg', 'JPEG')


from api.repository_netmundi import RepositoryNetMundi

rnm = RepositoryNetMundi()
cordeis_links = rnm.get_cordeis()
rnm.download_cordeis(cordeis_links)
