import spacy
from inscriptis import get_text
import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd


nlp = spacy.load("en_core_web_sm")


class Scrapper:
    def __init__(self) -> None:
        self.entities_details = list()
        self.identify_methods = {
            'csv': self.identify_entities_by_csv,
            'html': self.identify_entities_by_text
        }
        self.page_type = None
        self.content = None
        self.url = None
        self.has_problems = False
        self.problem_details = ''

    def fetch_url(self, url: str) -> None:
        # Fetch the requested url
        self.url = url
        self.content = requests.get(self.url)
    
    def __validate_type_url_content(self):
        # Check the content return
        page_type = self.content.headers['Content-Type']
        self.page_type = re.findall(r'csv|html', page_type)[0]
    
    def identify_entities(self):
        # Validate the page type (html or csv) and identify the entities according to page type
        self.__validate_type_url_content()
        return self.identify_methods[self.page_type]() if self.page_type else None

    def identify_entities_by_csv(self) -> list:
        # Recognize that it is a csv and will extract entities based on csv format
        html_content = self.content.text
        remove_header_content = re.split(r'\n', html_content, maxsplit=1)[1]
        text = get_text(remove_header_content)
        doc = nlp(text)
        list_of_entities = {ent.text for ent in doc.ents if ent.label_ == 'ORG'}
        cleaned_entities = None
        if len(list_of_entities) == 0:
            self.has_problems, self.problem_details = True, 'No identified entities'
            return cleaned_entities
        else:
            cleaned_entities = self.__clean_and_remove_duplicates(list_of_entities, 
                                                                  if_csv=True)
            for ent in cleaned_entities:
                self.entities_details.append({
                    'links': self.url,
                    'extracted_entity': ent,
                })
            return cleaned_entities
    
    def identify_entities_by_text(self) -> list:
        # Recognize that it is a html page and will extract entities based on html format
        html_content = self.content.text
        text = get_text(html_content)
        doc = nlp(text)
        list_of_entities = {ent.text for ent in doc.ents if ent.label_ == 'ORG'}
        cleaned_entities = None
        if len(list_of_entities) == 0:
            self.has_problems, self.problem_details = True, 'No identified entities'
            return cleaned_entities
        else:
            cleaned_entities = self.__clean_and_remove_duplicates(list_of_entities)
            for ent in cleaned_entities:
                self.entities_details.append({
                    'links': self.url,
                    'extracted_entity': ent,
                })
            return cleaned_entities

    def __clean_and_remove_duplicates(self, entities_list, if_csv=False) -> list:
        # Clean and removed the identified entities
        if if_csv:
            reg_pat = r"""'s.*|’s.*|LLP|PTE|“.*|\""""
        else:
            reg_pat = r""", .*|'s.*|’s.*|LLP|PTE|“.*|\""""
        cleaned_list = list({re.sub(reg_pat, '', ent) for ent in entities_list})
        cleaned_list = [clean for clean in cleaned_list if clean != '']
        return cleaned_list

    def fetch_short_description(self) -> list:
        # Fetch a short description of the entity found in wikipedia.
        for ent in self.entities_details:
            entity = ent['extracted_entity']
            try:
                content = requests.get(f'https://en.wikipedia.org/wiki/{entity}', timeout=0.05)
                html_page = content.text
                rendered_html = bs(html_page, 'lxml')
                short_des = rendered_html.find("p").text
                short_des = re.sub(r'"', '', short_des)
            except:
                short_des = 'Takes too long to load. As it is Demo app, will not load it.'
            
            ent['entity_details'] = short_des
        return self.entities_details


class DataStorage:
    def __init__(self, engine) -> None:
        self.ENGINE = engine
    
    def insert_data(self, entity: dict) -> None:
        # Insert data to the database
        cursor = self.ENGINE.connect()
        link = entity['links']
        extracted_entity = entity['extracted_entity']
        entity_details = entity['entity_details']
        statement = f"""
                    INSERT INTO extracted_entities (links, extracted_entity, entity_details) 
                    VALUES ("{link}", "{extracted_entity}", "{entity_details}")
                    """
        cursor.execute(statement)
        
    def fetch_all_entities(self):
        # Fetch all collected(scraped) entities
        q = "SELECT extracted_entity FROM extracted_entities"
        df = pd.read_sql(q, self.ENGINE)
        return df
    
    def fetch_single_entity(self, entity: str):
        # Fetch a single entity with a short description of it.
        query = f"""
                SELECT extracted_entity, entity_details 
                FROM extracted_entities
                WHERE extracted_entity = '{entity}'
                """
        df = pd.read_sql(query, self.ENGINE)
        return df
