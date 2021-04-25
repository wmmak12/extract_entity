import hug

import sys
sys.path.append('./src')
import util.general_util as gu
from util.api_util import Scrapper, DataStorage


@hug.get("/scrape_entity", output=hug.output_format.json)
def scrape_entity(url: hug.types.text, sqlite_db_path: str = 'gic.db'):
    sqlEngine = gu.create_sqlite_engine(sqlite_db_path)
    scrapper = Scrapper()
    scrapper.fetch_url(url)
    scrapper.identify_entities()
    entities_details = scrapper.fetch_short_description()
    if scrapper.has_problems:
        return 'No entity found'
    else:
        data_storage = DataStorage(sqlEngine)
        for ent in entities_details:
            data_storage.insert_data(ent)
        return entities_details


@hug.get("/fetch_all_entities", output=hug.output_format.json)
def fetch_all_entities(sqlite_db_path: str = 'gic.db'):
    sqlEngine = gu.create_sqlite_engine(sqlite_db_path)
    data_storage = DataStorage(sqlEngine)
    df = data_storage.fetch_all_entities()
    return {
        'extracted_entities': df.extracted_entity.tolist()
    }


@hug.get("/fetch_entity_details", output=hug.output_format.json)
def fetch_entity_details(entity: hug.types.text, sqlite_db_path: str = 'gic.db'):
    sqlEngine = gu.create_sqlite_engine(sqlite_db_path)
    data_storage = DataStorage(sqlEngine)
    df = data_storage.fetch_single_entity(entity)
    if len(df) > 0:
        entity_details = df.entity_details.values[0]
        return {
            entity: entity_details
        }
    else:
        return "No such entity found"
    

@hug.not_found()
def not_found_handler():
    return "Page not found"

