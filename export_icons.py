# export collections from https://hypixel-skyblock.fandom.com/wiki/Collections
import itertools
import json
import urllib.request
import roman
from bs4 import BeautifulSoup

with open("collections_and_levels.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


l = soup.find_all("table", class_="wikitable")
grouped = list(grouper(2, l))
coll = {}
for i in grouped:
    name = i[0].find("tr")["id"]
    print(name)
    img_src = i[0].find("tr").find("img")["data-src"]
    img_src = img_src[:img_src.find(".png")+4]

    print(img_src)
    try:
        urllib.request.urlretrieve(img_src, 'assets/icons/'+name+".png")
    except:
        print("failed"+name+img_src)
    levels = {}



    coll[name] = levels
print(coll)
print(len(coll))
