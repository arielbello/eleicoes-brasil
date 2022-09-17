import csv
from io import BytesIO, TextIOWrapper
from pathlib import Path
from zipfile import ZipFile

import rows
import scrapy

import utils
import settings


field_map = {
    "partido": "Partido",
    "nome": "Nome do eleitor",
    "uf": "UF",
    "municipio": "Município",
    "zona_eleitoral": "Zona",
    "titulo_eleitoral": "Título de eleitor",
    "data_filiacao": "Data de filiação",
    "situacao": "Situação",
}


def convert_row(row):
    new = {}
    for new_name, old_name in field_map.items():
        value = utils.unaccent(row[old_name]).upper()
        value = utils.remove_extra_spaces(value)
        if new_name.startswith("data_"):
            value = str(utils.ShortPtBrDateField.deserialize(value) or "")
        new[new_name] = value
    return new


class FiliadosFileParserSpider(scrapy.Spider):
    name = "filiados-file-parse-new"

    def start_requests(self):
        links = rows.import_from_csv(settings.OUTPUT_PATH / "filiacao-links.csv")
        for row in links:
            yield scrapy.Request(
                url="file://" + str(Path(row.filename).absolute()), meta=row._asdict()
            )

    def parse(self, response):
        zf = ZipFile(BytesIO(response.body))
        files = sorted(zf.filelist, key=lambda row: row.filename, reverse=True)
        csv_fobj = None
        for file_info in files:
            filename = Path(file_info.filename).name
            if "tse_filiados" in filename.lower() and filename.endswith(".csv"):
                csv_fobj = zf.open(file_info.filename)
                break

        if csv_fobj is not None:
            reader = csv.DictReader(TextIOWrapper(csv_fobj, encoding="iso-8859-15"))
            for row in reader:
                yield convert_row(row)
