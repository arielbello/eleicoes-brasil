from pathlib import Path


BASE_PATH = Path(__file__).parent.absolute()
MIRROR_FILENAME = BASE_PATH / "mirror.sh"
SCHEMA_PATH = BASE_PATH / "schema"
DATA_PATH = BASE_PATH / "data"
DOWNLOAD_PATH = DATA_PATH / "download"
OUTPUT_PATH = DATA_PATH / "output"
HEADERS_PATH = BASE_PATH / "headers"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0"

for path in (DATA_PATH, DOWNLOAD_PATH, OUTPUT_PATH):
    if not path.exists():
        path.mkdir(parents=True)
