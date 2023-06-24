# export collections from https://hypixel-skyblock.fandom.com/wiki/Collections
import itertools
import json

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

    levels = {}

    cs = i[1].find_all("tr")
    cs = cs[1:]

    for c in cs:
        if c.has_attr("id"):
            print(c["id"])
            print()
            levels[roman.fromRoman(c["id"])] = int(c.find_all("td")[1].text.replace(",",""))

    coll[name] = levels
print(coll)
print(len(coll))
with open("levels.json","w") as f:
    f.write(json.dumps(coll))