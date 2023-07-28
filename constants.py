import platformdirs
import json
from PIL import Image

APPNAME = "ben_skyblock_collection_stream"
AUTHOR = "io.github.aws1313"
CACHE_DIR = platformdirs.user_cache_dir(APPNAME, AUTHOR)
DATA_DIR = platformdirs.user_data_dir(APPNAME, AUTHOR)
default_img = Image.new("RGBA", (750,150))


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_from_json(filename):
    with open(filename) as f:
        return json.loads(f.read())
