import requests
import json
import platformdirs
import os
import datetime
import operator
from flask import Flask
from flask import jsonify
app = Flask(__name__)
APPNAME = "ben_skyblock_collection_stream"
AUTHOR = "io.github.aws1313"
CACHE_DIR = platformdirs.user_cache_dir(APPNAME, AUTHOR)
DATA_DIR = platformdirs.user_data_dir(APPNAME, AUTHOR)


def get_profile_collection(api_key, profile_id, uuid):
    url = f"https://api.hypixel.net/skyblock/profile?key={api_key}&profile={profile_id}&uuid={uuid}"
    response = requests.get(url)
    return response.json()


def prepare_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    print(f"{CACHE_DIR=}; {DATA_DIR=}")


def get_collected_items():
    url = f"https://api.hypixel.net/resources/skyblock/collections"
    response = requests.get(url)
    return response.json()


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_from_json(filename):
    with open(filename) as f:
        return json.loads(f.read())


def load_conf():
    conf_path = os.path.join(DATA_DIR, "config.json")
    if os.path.exists(conf_path):
        with open(conf_path) as f:
            return json.loads(f.read())
    else:
        save_to_json(conf_path, {"api-key": "", "uuid": "", "profile-id": ""})
        exit(f"Config did not exist please fill out: {conf_path}")


def prepare_collection_infos():
    collection_info_path = os.path.join(CACHE_DIR, "collection_info.json")
    if os.path.exists(collection_info_path) and (datetime.datetime.fromtimestamp(
            os.path.getmtime(collection_info_path)) > datetime.datetime.now() - datetime.timedelta(days=1)):
        return read_from_json(collection_info_path)
    else:
        url = "https://api.hypixel.net/resources/skyblock/collections"
        response = requests.get(url)
        print("Got new collection_infos")
        save_to_json(collection_info_path, response.json())
        return response.json()


def evaluate_changes(old: dict, new: dict, old_collections):
    collected = {}
    for u in new["profile"]["members"]:
        if "collection" in new["profile"]["members"][u].keys():
            for i in new["profile"]["members"][u]["collection"].keys():
                if i in collected.keys():
                    collected[i] += new["profile"]["members"][u]["collection"][i]
                else:
                    collected[i] = new["profile"]["members"][u]["collection"][i]
    print(collected)
    collected_old = {}
    for u in old["profile"]["members"]:
        if "collection" in old["profile"]["members"][u].keys():
            for i in old["profile"]["members"][u]["collection"].keys():
                if i in collected_old.keys():
                    collected_old[i] += old["profile"]["members"][u]["collection"][i]
                else:
                    collected_old[i] = old["profile"]["members"][u]["collection"][i]
    collections = old_collections
    for k in collected.keys():
        collections[k] = {"collected": collected[k]}
        if k in collected_old.keys() and (collected[k] != collected_old[k]):
            collections[k]["last_changed"] = int(datetime.datetime.now().timestamp())
            collections[k]["changed"] = True
            collections[k]["amount_changed"] = collected[k] - collected_old[k]
        else:
            collections[k]["changed"] = False
            collections[k]["amount_changed"] = 0
        if "last_changed" not in collections[k]:
            collections[k]["last_changed"] = 0

    return collections


def get_collections(old: dict, new: dict, collection_infos, old_collections):
    # Target [{"id":"COLLECTION", "display_name":"DISPLAY_NAME", "collected":1000, "tier_now":0,"missing_to_next_tier":500, "percentage_to_next_tier":0.75, "last_changed":0}]
    coll = evaluate_changes(old, new, old_collections)
    print(coll)

    items = {}
    for i in collection_infos["collections"].keys():
        for h in collection_infos["collections"][i]["items"].keys():
            items[h] = collection_infos["collections"][i]["items"][h]

    print(items)
    for c in coll.keys():
        if c in items.keys():
            coll[c]["display_name"] = items[c]["name"]
            coll[c]["id"] = c
            tier = 0
            # get tier now
            for tt in range(len(items[c]["tiers"])):
                t = items[c]["tiers"][tt]
                if coll[c]["collected"] > t["amountRequired"]:
                    tier = t["tier"]
                    if tier == items[c]["maxTiers"]:
                        coll[c]["maxed_out"] = True
                        coll[c]["missing_to_next_tier"] = 0
                        coll[c]["percentage_to_next_tier"] = 1
                    else:
                        coll[c]["maxed_out"] = False
                        next_needed = items[c]["tiers"][tt + 1]["amountRequired"]
                        coll[c]["missing_to_next_tier"] = next_needed - coll[c]["collected"]
                        coll[c]["percentage_to_next_tier"] = coll[c]["missing_to_next_tier"] / (
                                next_needed - t["amountRequired"])

                else:
                    break
            coll[c]["tier_now"] = tier

    return coll

# main
prepare_dirs()

# CONFIG
conf = load_conf()
api_key = conf["api-key"]
uuid = conf["uuid"]
profile_id = conf["profile-id"]

collection_infos = prepare_collection_infos()

# repeat
profile_collections_old = get_profile_collection(api_key, profile_id, uuid)

old_collection = {}

@app.route("/")
def renew_coll():
    global profile_collections_old
    global old_collection
    profile_collections_new = get_profile_collection(api_key, profile_id, uuid)
    save_to_json(os.path.join(CACHE_DIR, str(int(datetime.datetime.now().timestamp())) + ".json"),
                 profile_collections_new)
    c = get_collections(profile_collections_old, profile_collections_new, collection_infos, old_collection)
    print(c)
    sort = list(c.values())
    sort.sort(key=operator.itemgetter('last_changed'), reverse=True)

    print(sort)

    # save_to_json(os.path.join(CACHE_DIR, "exp.json"),sort)

    changed = []
    for s in sort:
        if s["changed"]:
            changed.append(s)

    print(changed)

    profile_collections_old = profile_collections_new
    old_collection = c

    return jsonify({"sorted": sort, "changed": changed})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    while True:
        inp = input("Press enter to continue")
        if inp == "e":
            exit()
        renew_coll()


