import httpx
import xmltodict
from utils.helper.func_helper import convert_to_string, addQueryToURL

index_loc = "data"
index_items = [
    "ScientificName",
    "Rank",
    "Division",
]
index_object = {f"{index_loc}.{item}": 1 for item in index_items}

async def retrieve(portal: dict) -> dict:
    try:
        # Construct the URL to retrieve data from the NCBI API
        url = await addQueryToURL(portal)

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

        data = data['TaxaSet']['Taxon']

        # Return the parsed data
        return data
    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")

async def data_processing(retrieve_data) -> str:
    try:
        return convert_to_string(retrieve_data)
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")