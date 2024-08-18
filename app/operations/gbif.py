import httpx
from utils.helper.func_helper import convert_to_string, addQueryToURL

index_object = {"data.species": 1, "data.genus": 1, "data.family": 1, "data.order": 1, "data.class": 1, "data.phylum": 1}

async def retrieve(portal: dict) -> dict:
  try:
    # Construct the URL to retrieve data from the GBIF API
    url = await addQueryToURL(portal)

    # Send a GET request to the specified URL using an AsyncClient
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    # Return the retrieved data
    return data

  except Exception as e:
      raise Exception(f"An error occurred while retrieving data: {str(e)}")
  
async def data_processing(retrieve_data) -> str:
    try:
        return convert_to_string(retrieve_data)
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")