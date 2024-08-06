import httpx

async def wikidata_retrieve(url):
    try:
        async with httpx.AsyncClient() as client:
          response = await client.get(url)
          response.raise_for_status()
          data = response.json()

        id = data['results']['bindings'][0]['item']['value'].split('/')[-1]

        getDataById = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={id}&languages=en"

        async with httpx.AsyncClient() as client:
          response = await client.get(getDataById)
          response.raise_for_status()
          data = response.json()

        return data

    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")
  
async def wikidata_data_processing(retrieve_data):
    try:
        return retrieve_data
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")