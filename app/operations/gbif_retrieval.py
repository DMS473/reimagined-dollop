import httpx

async def gbif_retrieve(url):
  try:
      async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

      return data

  except Exception as e:
      raise Exception(f"An error occurred while retrieving data: {str(e)}")
  
async def gbif_data_processing(retrieve_data):
    try:
        return retrieve_data
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")