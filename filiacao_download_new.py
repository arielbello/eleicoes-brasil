import os
import random
import re
import string
import tempfile
from pathlib import Path

import scrapy

import settings

URLS = [
    "https://cdn.tse.jus.br/filiados/a2/30db99e78f92818212ecaf2d0884068e4bc1dc/TSE_Filiados_AC_20220715.zip",
    "https://cdn.tse.jus.br/filiados/4f/2d1ae9275afb305fe3e80de1d7164704f8cf65/TSE_Filiados_AL_20220715.zip",
    "https://cdn.tse.jus.br/filiados/71/6fe02cb94a80180f3f96a4f466ca2fa32997f4/TSE_Filiados_AM_20220715.zip",
    "https://cdn.tse.jus.br/filiados/bf/5b55eb692543df68e3de41c730f348e8272bde/TSE_Filiados_AP_20220715.zip",
    "https://cdn.tse.jus.br/filiados/45/425367f233a8afa874777fe257f9479e351975/TSE_Filiados_BA_20220715.zip",
    "https://cdn.tse.jus.br/filiados/53/6f8a5ede2e2ac5846dc1380065b3d36177ae6f/TSE_Filiados_CE_20220715.zip",
    "https://cdn.tse.jus.br/filiados/54/1b19c639ee169e1db113bf218ebd5bf7c3ec6c/TSE_Filiados_DF_20220715.zip",
    "https://cdn.tse.jus.br/filiados/1f/babe168d46c67d32dc6d02a2deb9b1528ddcea/TSE_Filiados_ES_20220715.zip",
    "https://cdn.tse.jus.br/filiados/f6/7022fc7713a97b2a967aeae29cce5a937208d8/TSE_Filiados_GO_20220715.zip",
    "https://cdn.tse.jus.br/filiados/57/5627775471317eebb2f74b51f3349e1e1ffe4c/TSE_Filiados_MA_20220715.zip",
    "https://cdn.tse.jus.br/filiados/1d/6151f13842601224316b2f3bb0dd9476b6c453/TSE_Filiados_MG_20220715.zip",
    "https://cdn.tse.jus.br/filiados/c9/5a550c2e3b4313a9e80dd3c5a909dd6bab1a66/TSE_Filiados_MS_20220715.zip",
    "https://cdn.tse.jus.br/filiados/09/9452189be790012fe4c4c684258e508d5eca6b/TSE_Filiados_MT_20220715.zip",
    "https://cdn.tse.jus.br/filiados/40/02191500a17fd89a296efda4a7804f525b409b/TSE_Filiados_PA_20220715.zip",
    "https://cdn.tse.jus.br/filiados/79/1b9c728233ed9b39fd957b3acdca27f14ac382/TSE_Filiados_PB_20220715.zip",
    "https://cdn.tse.jus.br/filiados/5a/0747d12c0c62c62e6f74c218e2263364938f20/TSE_Filiados_PE_20220715.zip",
    "https://cdn.tse.jus.br/filiados/71/5cdcd3ccd36376c95eb40e2e016008fa04cab1/TSE_Filiados_PI_20220715.zip",
    "https://cdn.tse.jus.br/filiados/f7/f0514d217e27ee35ddaa6e47c61e44a34fa80c/TSE_Filiados_PR_20220715.zip",
    "https://cdn.tse.jus.br/filiados/d8/8a6390c3facf5e9ed077ec66f888b411231bca/TSE_Filiados_RJ_20220715.zip",
    "https://cdn.tse.jus.br/filiados/ac/9cb7d4c4513d84b4702ef6ea82a261b53b9f1b/TSE_Filiados_RN_20220715.zip",
    "https://cdn.tse.jus.br/filiados/d8/3bd78697c1f2ce59e7ab5e670147091402944a/TSE_Filiados_RO_20220715.zip",
    "https://cdn.tse.jus.br/filiados/c1/741d7e2e1e7bfb46bac7e8be613da9c6e76538/TSE_Filiados_RR_20220715.zip",
    "https://cdn.tse.jus.br/filiados/98/696e3b854950b04c3e3f88aff446d3e62209a6/TSE_Filiados_RS_20220715.zip",
    "https://cdn.tse.jus.br/filiados/6a/69a7df0dbd04712c2c3fdf2fef63fd0cd86d5f/TSE_Filiados_SC_20220715.zip",
    "https://cdn.tse.jus.br/filiados/37/6eef97ad636d85c72334cfeba1827981829b27/TSE_Filiados_SE_20220715.zip",
    "https://cdn.tse.jus.br/filiados/7e/f65e40eced82c96e781e6d6c325243576f0882/TSE_Filiados_SP_20220715.zip",
    "https://cdn.tse.jus.br/filiados/47/cf12b16ddcce216009928fa7d671f5eae98ece/TSE_Filiados_TO_20220715.zip",
    "https://cdn.tse.jus.br/filiados/92/102f58551b37a5284804770da52b2c6cf20fa6/TSE_Filiados_Exterior_20220715.zip",
]

STATE_REGEX = re.compile(r"TSE_FILIADOS_([\w]+?)_", re.IGNORECASE)


def random_string(length):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def random_file():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix="txt")
    with open(tmp.name, mode="w") as fobj:
        fobj.write("test\n")
    return Path(tmp.name)


class FiliadosFileListSpider(scrapy.Spider):
    name = "filiados-file-list-new"

    def filename(self, state):
        return f"eleitorado/filiados/uf/filiados_{state}.zip"

    def download_filename(self, state):
        return settings.DOWNLOAD_PATH / self.filename(state)

    def start_requests(self):
        for url in URLS:
            state = STATE_REGEX.search(url).group(1)
            download_filename = self.download_filename(state)
            if not download_filename.exists():
                yield scrapy.Request(
                    url=url,
                    meta={
                        "filename": download_filename,
                        "state": state,
                    },
                    callback=self.save_zip,
                )
            else:
                # Hack to yield an already downloaded file from here
                temp_filename = random_file()
                yield scrapy.Request(
                   "file://" + str(temp_filename),
                    meta={
                        "row": {
                            "filename": download_filename,
                            "state": state,
                            "url": url,
                        },
                        "dont_cache": True,
                        "temp_filename": temp_filename,
                    },
                    callback=self.yield_row,
                )

    def yield_row(self, response):
        meta = response.meta
        yield meta["row"]
        os.unlink(meta["temp_filename"])

    def save_zip(self, response):
        meta = response.request.meta
        filename = meta["filename"]
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        with open(filename, mode="wb") as fobj:
            fobj.write(response.body)
        yield {
            "filename": meta["filename"],
            "state": meta["state"],
            "url": response.url,
        }
