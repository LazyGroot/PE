# coding: utf-8

from bs4 import BeautifulSoup
import requests


payload = {'lieux': '97411', 'offresPartenaires': 'true', 'motsCles': 'developpeur', 'rayon': '10', 'tri': '0'}

r = requests.get('https://candidat.pole-emploi.fr/offres/recherche', params=payload, timeout=5)


#url="https://candidat.pole-emploi.fr/offres/recherche?lieux=97411&offresPartenaires=true&rayon=10&tri=0&motsCles=developpeur"


print(r.url)

#print r.headers['Content-Type']
#print r.encoding
html= r.text.encode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

print( soup.find_all('li','result') )
