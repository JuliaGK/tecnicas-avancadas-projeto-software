import requests
import re
from bs4 import BeautifulSoup


def get_links_episodios_friends():
    pagina_falas_friends = requests.get('https://fangj.github.io/friends/')
    soup_pagina = BeautifulSoup(pagina_falas_friends.text, 'html.parser')
    dataset_tags_links_episodios = soup_pagina.find_all('a')

    links_episodios = []

    for tag in dataset_tags_links_episodios:
        resultado = re.search(r'href=\"(.+\.html)\"', str(tag))
        if resultado:
            link_completo = 'https://fangj.github.io/friends/' + resultado.group(1)
            links_episodios.append(link_completo)

    return links_episodios


def write_links_episodios_friends(links_episodios):
    with open("links_episodios.csv", "w") as arquivo:
        for link in links_episodios:
            arquivo.write(link)


def get_all_falas():
    links = get_links_episodios_friends()
    falas_todos_episodios = []
    count = 0
    for link in links:
        count += 1
        print('Carregando episódio ' + str(count) + '...')
        falas_todos_episodios.append(get_falas_episodio(link))
    return falas_todos_episodios


def get_falas_episodio(link_episodio):
    pagina_episodio = requests.get(link_episodio)
    soup = BeautifulSoup(pagina_episodio.text, 'html.parser')
    falas_tags = soup.find_all("p")

    falas = []

    for tag in falas_tags:
        personagem = re.search(r'<b>(.+)<\/b>', str(tag))
        fala = re.search(r'<p.+>(.+)<\/p>', str(tag).replace('\n', ''))
        if personagem:
            personagem = remove_tags(personagem.group(1)).strip()
            falas.append(personagem)
        if fala:
            fala = remove_tags(fala.group(1)).strip()
            falas.append(fala)

    return falas


def write_falas(falas_todos_episodios):
    with open("falas_todos_episodios.csv", "w") as arquivo:
        for episodio in falas_todos_episodios:
            for fala in episodio:
                arquivo.write(fala)


def remove_tags(string):
    tags = ['</strong>', '</b>', '</font>', '<b>']
    for tag in tags:
        if tag in string:
            string = string.replace(tag, '')
    return string


write_falas(get_all_falas())
