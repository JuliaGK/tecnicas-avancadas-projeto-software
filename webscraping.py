import requests
from bs4 import BeautifulSoup
import re


# Coletar a primeira página da lista de artistas
page = requests.get('https://fangj.github.io/friends/')
soup = BeautifulSoup(page.text, 'html.parser')
dataSet = soup.find_all('a')
dataSet = str(dataSet)
links = []

file = open("links.csv", "w")

for linha in dataSet.split('<a href="'):
    links.append('https://fangj.github.io/friends/'+ linha.split('">')[0]+"\n")
del links[0]

for linha in links:
    file.write(linha)


print(links)

file.close()

links = open("links.csv", "r")
falas = open("falas.txt", "a")

regex = re.compile('[^a-zA-Z\'\n ]')
count = 0

for link in links:
    page = requests.get(link.split("\n")[0])
    soup = BeautifulSoup(page.text, 'html.parser')
    texto = soup.find_all("p")
    for linha in texto:
        # Remove as tags
        verificar = True
        frase = ""
        for letra in str(linha):
            if (verificar == False):
                if (letra == ">"):
                    verificar = True
            else:
                if (letra == "<"):
                    verificar = False
                else:
                    frase = frase + letra
        # Remove o autor da frase
        frase = frase.split(":")
        if (len(frase) > 1):
            frase = frase[1]
            # Retira espaços e numeros
            frase = frase.strip()
            frase = regex.sub("", frase)
            frase = frase.lower()
            frase = frase.replace("\n", " ")
            if (frase != ""):
                falas.write(frase + "\n")
    count += 1
    print(link)
    print(count)

