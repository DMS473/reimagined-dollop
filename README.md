# Introduction
This project is a FastAPI-based web service that interacts with a MongoDB database using Motor, an async MongoDB driver for Python. The service retrieves, processes, and stores data across three main collections: portals, raw data, and terms.

This project is designed to facilitate the management of information across different stages of data processing. It includes functionality for:

- Managing portal-related data.
- Collecting and storing raw data.
- Processing raw data into terms, which are then stored for later use.


# Tutorial
## First Step
* `git clone https://github.com/fikridean/INNAKM.git` - Clone the project from **[INNAKM Github Repository](https://github.com/fikridean/INNAKM)**.
* `pip install -r requirements.txt` - Install the required **dependencies**
* `fastapi dev app/main.py` - **Run FastAPI**.
* `mkdocs serve`: This project use **MkDocs** to build and view the documentation. Run this command to preview it locally.

For more information, please visit [INNAKM Github Repository](https://github.com/fikridean/INNAKM).


# Portals & Species
## Types of portals
- [WikiData](https://www.wikidata.org/)
- [NCBI](https://www.ncbi.nlm.nih.gov/)
- [BacDive](https://bacdive.dsmz.de/)
- [GBIF](https://www.gbif.org/)

## Species
- Achromobacter mucicolens
- Aeromonas hydrophila
- Chelatococcus thermostellatus
- Cobetia marina
- Dactylosporangium aurantiacum
- Empedobacter tilapiae
- Escherichia fergusonii
- Klebsiella aerogenes
- Klebsiella pasteurii
- Klebsiella pneumoniae
- Lactiplantibacillus plantarum
- Luteibacter jiangsuensis
- Myxococcus stipitatus
- Ochrobactrum quorumnocens
- Pantoea agglomerans
- Pantoea dispersa
- Pseudomonas ceruminis
- Pseudomonas palmensis
- Pseudomonas qingdaonensis
- Raoultella ornithinolytica
- Rhodopseudomonas palustris
- Stenotrophomonas maltophilia
- Streptomyces fagopyri
- Streptomyces lutosisoli
- Streptomyces mirabilis
- Stutzerimonas stutzeri
- Xanthomonas campestris
- Rhizobium leguminosarum
- Streptomyces kunmingensis
- Streptomyces rochei
- Streptomyces griseorubens
- Streptomyces sp.
- Streptomyces sampsonii
- Micromonospora chalcea
- Klebsiella quasuvaricola
- Escherichia coli
- Gulosibacter sp.
- Pseudomonas hibiscicola
- Providencia rettgeri
- Burkholderia sp.
- Klebsiella oxytoca
- Brevibacterium ammoniilyticum

# Data Parsing

## WikiData Portal
### Steps
#### 1. Initialize HTTP Client
Create an asynchronous HTTP client using `httpx.AsyncClient`.

#### 2. Send Initial GET Request
Send a GET request to the specified URL to retrieve initial data.

#### 3. Parse JSON Response
Parse the JSON response from the initial GET request to extract the required data.

#### 4. Extract ID from JSON Data
Extract the ID from the JSON data for further queries.

#### 5. Construct URL for Data by ID
Construct a new URL to fetch data by ID from the Wikidata API.

#### 6. Send GET Request to Fetch Data by ID
Send a GET request to the Wikidata API using the constructed URL to retrieve data by ID.

#### 7. Parse JSON Response from Data by ID Request
Parse the JSON response from the second GET request to extract the data.

### Python Code
```python

async with httpx.AsyncClient() as client:
  # Send a GET request to the specified URL
  response = await client.get(url)
  response.raise_for_status()

  # Parse the response as JSON
  data = response.json()

# Extract the ID from the JSON data
id = data['results']['bindings'][0]['item']['value'].split('/')[-1]

# Construct the URL to fetch data by ID from Wikidata API
getDataById = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={id}&languages=en"

async with httpx.AsyncClient() as client:
  # Send a GET request to fetch data by ID from Wikidata API
  response = await client.get(getDataById)
  response.raise_for_status()
  
  # Parse the response as JSON
  data = response.json()
```

## NCBI Portal
### Steps
#### 1. Create an Asynchronous HTTP Client Session
Initialize an asynchronous HTTP client session to make HTTP requests.

#### 2. Send a GET Request to the Specified URL
Send a GET request to the provided URL to retrieve initial data.

#### 3. Raise an Exception if the Request was Unsuccessful
Ensure that the request was successful; raise an exception if it was not.

#### 4. Parse the XML Response into a Dictionary
Convert the XML response into a dictionary for easier data manipulation.

#### 5. Extract the ID from the Parsed XML Data
Extract the ID from the dictionary obtained from the XML response.

#### 6. Construct a New URL to Fetch Data by the Extracted ID
Build a new URL to retrieve detailed data using the extracted ID.

#### 7. Create Another Asynchronous HTTP Client Session
Initialize a new asynchronous HTTP client session for the next request.

#### 8. Send a GET Request to the New URL
Send a GET request to the new URL to fetch data by ID.

#### 9. Raise an Exception if the Request was Unsuccessful
Ensure that the request was successful; raise an exception if it was not.

#### 10. Parse the XML Response into a Dictionary
Convert the XML response from the second request into a dictionary.

#### 11. Return the Parsed Data
Return the dictionary containing the parsed data.


### Python Code
```python

# Create an asynchronous HTTP client session
async with httpx.AsyncClient() as client:
    # Send a GET request to the specified URL
    response = await client.get(url)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the XML response into a dictionary
    data = xmltodict.parse(response.text)

# Extract the ID from the parsed XML data
id = data['eSearchResult']['IdList']['Id']

# Construct a new URL to fetch data by the extracted ID
getDataById = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={id}"

# Create another asynchronous HTTP client session
async with httpx.AsyncClient() as client:
    # Send a GET request to the new URL
    response = await client.get(getDataById)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the XML response into a dictionary
    data = xmltodict.parse(response.text)

# Return the parsed data
return data

```

## Bacdive Portal
### Steps
#### 1. Create a BacdiveClient Object
Initialize a BacdiveClient object using the provided email and password.

#### 2. Search for the Given Species Name in Bacdive
Perform a search in Bacdive for the specified species name.

#### 3. Create an Empty Dictionary to Store Retrieved Data
Initialize an empty dictionary to hold the data retrieved from Bacdive.

#### 4. Retrieve Data from Bacdive and Store in the Dictionary
Iterate through the retrieved data and store each item in the dictionary.

#### 5. Return the Retrieved Data Dictionary
Return the dictionary containing the retrieved data.

#### 6. Convert the Retrieved Data to a Dictionary with String Keys
Convert the dictionary keys to strings and return the updated dictionary.


### Python Code
```python

# Create a BacdiveClient object with the provided email and password
bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)

# Search for the given species name in Bacdive
bacdive_count = bacdive_client.search(taxonomy=species_name)

# Create an empty dictionary to store the retrieved data
bacdive_dict: dict = {}

# Retrieve the data from Bacdive and store it in the dictionary
k = 0
for v in bacdive_client.retrieve():
    bacdive_dict[k] = v 
    k = k + 1

# Return the retrieved data dictionary
return bacdive_dict

# Convert the retrieved data to a dictionary with string keys
return {str(k): v for k, v in bacdive_dict.items()}

```

## GBIF Portal
### Steps
#### 1. Send a GET Request to the Specified URL
Use an asynchronous HTTP client to send a GET request to the given URL.

#### 2. Check for Request Success
Ensure the request was successful; handle any errors if the request fails.

#### 3. Parse the JSON Response
Convert the response from the GET request into a JSON format for easy access.

#### 4. Return the Retrieved Data
Return the data obtained from the JSON response.

### Python Code
```python

# Send a GET request to the specified URL using an AsyncClient
async with httpx.AsyncClient() as client:
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()

# Return the retrieved data
return data

```

# Project Structure

- **app/**: Main directory for the FastAPI application.
    - **common/**
        - **message/**
            - **message_enum.py**: Defines enums for different message types used in the application.
    - **config.py**: Contains configuration settings for the FastAPI application.
    - **crud/**
        - **portal_crud.py**: Manages CRUD operations for the `portals` collection.
        - **raw_data_crud.py**: Manages CRUD operations for the `raw_data` collection.
    - **database/**
        - **mongo.py**: Manages MongoDB connections and related utilities.
    - **main.py**: Entry point for the FastAPI application. Initializes the app, includes routers, and starts the server.
    - **models/**
        - **portal_model.py**: Defines the data model for the `portals` collection.
        - **raw_data_model.py**: Defines the data model for the `raw_data` collection.
    - **operations/**
        - **bacdive_retrieval.py**: Handles data retrieval from the BacDive database.
        - **gbif_retrieval.py**: Handles data retrieval from the GBIF database.
        - **ncbi_retrieval.py**: Handles data retrieval from the NCBI database.
        - **wikidata_retrieval.py**: Handles data retrieval from Wikidata.
    - **routers/**
        - **portal_router.py**: Manages routes related to the `portals` collection.
        - **raw_data_router.py**: Manages routes related to the `raw_data` collection.
    - **utils/**
        - **response_helper.py**: Provides utilities for standardizing API responses.
- **docs/**
    - **A.md**: Tutorial section for documentation.
    - **B.md**: Database section for documentation.
    - **C.md**: Project structure section for documentation.
    - **index.md**: Introduction section for documentation.
- **mkdocs.yml**: Configuration file for MkDocs, used to build project documentation.
- **tree_structure.txt**: Contains the structure of the project directory.
- **requirements.txt**: Lists Python dependencies required to run the application.
- **README.md**: Provides an overview of the project, including its structure and instructions for setup and usage.