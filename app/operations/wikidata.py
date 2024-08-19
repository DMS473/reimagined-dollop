import httpx
from utils.helper.func_helper import convert_to_string, addQueryToURL

index_loc = "data"
index_items = [
    "labels.en.value",
    "descriptions.en.value",
]

index_object = {f"{index_loc}.{item}": 1 for item in index_items}

async def retrieve(portal: dict) -> dict:
    try:
        # Construct the URL to retrieve data from the Wikidata API
        url = await addQueryToURL(portal)

        # Send a GET request to the specified URL using an AsyncClient
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

          # Extract the data by ID
          data = data['entities'][id]

        return data

    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")
  
async def data_processing(retrieve_data) -> str:
    try:
        return convert_to_string(retrieve_data)
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")