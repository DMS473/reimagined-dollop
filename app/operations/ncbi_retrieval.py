import httpx
import xmltodict

async def ncbi_retrieve(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = xmltodict.parse(response.text)
        
        id = data['eSearchResult']['IdList']['Id']

        getDataById = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(getDataById)
            response.raise_for_status()
            data = xmltodict.parse(response.text)

        return data
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")

async def ncbi_data_processing(retrieve_data):
    try:
        return retrieve_data
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")