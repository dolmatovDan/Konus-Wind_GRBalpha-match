import requests
from bs4 import BeautifulSoup as bs

r = requests.get("https://monoceros.physics.muni.cz/hea/GRBAlpha/")
soup = bs(r.content)

# len(soup.find_all("table")) = 1
# This means, that the first one in necessary data
table = soup.find("table")
