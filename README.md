# extract_entity
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
- Click on the cloud-run-button to deploy the service to your Google Cloud account
- Will need to ensure container memory is set to at least 1gb

# TL:DR
There are a total of 3 different APIs:

| Types of APIs        | Parameters  | Description    |
| :---                 |    :----:   |          :---: |
| scrape_entity        | url         | This will scrape the provided link and identify organizations in the page. The page can be in either html or csv page |
| fetch_all_entities   | None        | This will fetch all the entities that was being processed by 'scrape_entity' api |
| fetch_entity_details | entity      | This will generate a short description of the provided entity that was scraped by 'scrape_entity' api. The short description is referenced from Wikipedia |

# Example Usage
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

# Next Steps
Project can be refactored in docker-compose for easier management with different environments. 
