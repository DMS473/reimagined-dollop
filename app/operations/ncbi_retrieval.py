import httpx
import xmltodict

async def ncbi_retrieve(url):
    try:
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
    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")

async def ncbi_data_processing(retrieve_data):
    try:
        return retrieve_data
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")