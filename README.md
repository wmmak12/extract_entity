# Extract Entity API Service

## Starting the Service in Cloud Run
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
- Click on the cloud-run-button to deploy the service to your Google Cloud account
- Will need to ensure container memory is set to at least 1gb
- Set cloud run port to 8888 :)

## TL:DR
There are a total of 3 different APIs:

| Types of APIs        | Parameters  | Description    |
| :---                 |    :----:   |          :---: |
| scrape_entity        | url (e.g. https://www.google.com) | This will scrape the provided link and identify organizations in the page. The page can be in either html or csv page |
| fetch_all_entities   | None | This will fetch all the entities that was being processed by 'scrape_entity' api |
| fetch_entity_details | entity (e.g. Apple) | This will generate a short description of the provided entity that was scraped by 'scrape_entity' api. The short description is referenced from Wikipedia. This is dependant on the entities you have scrape |

## Example Usage
1. scrape_entity: 
```
>  curl {urldeployed}/scrape_entity?url=https://www.globenewswire.com/en/news-release/2021/04/24/2216333/0/en/O2Gold-Closes-Acquisition-of-Colombian-Gold-Project.html'
```
2. fetch_all_entities
```
> curl {urldeployed}/fetch_all_entities
```
3. fetch_entity_details
```
> curl {urldeployed}/fetch_entity_details?entity={entity scraped}
```

## Repo Structure
This repo consist of the 3 main folders. 
- _src_
    - _extract_entity_api_: contains the main api functions for the service.
    - _create_sqlite_db_: instantiate the sqlite database when the docker container is first deployed
    - util: a folder to contain the supporting functions/classes for _extract_entity_api_ and _create_sqlite_db_
- _test_: 
    - _conftest_: test parameters for the test service
    - _test_service_: test services
- _Dockerfile_: contains Docker instructions to run the service 
- _requirements.txt_: python dependencies

## Next Steps
Project can be refactored in docker-compose for easier management with different environments. 
