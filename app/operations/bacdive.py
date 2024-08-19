from config import BACDIVE_EMAIL, BACDIVE_PASSWORD
import bacdive
from utils.helper.func_helper import convert_to_string

index_loc = "data.0"
index_items = [
    "General.description", 
    "Name and taxonomic classification.LPSN.domain",
    "Name and taxonomic classification.LPSN.phylum",
    "Name and taxonomic classification.LPSN.class",
    "Name and taxonomic classification.LPSN.order",
    "Name and taxonomic classification.LPSN.family",
    "Name and taxonomic classification.LPSN.genus",
    "Name and taxonomic classification.LPSN.species",
]
index_object = {f"{index_loc}.{item}": 1 for item in index_items}

# Get bacdive data
def retrieve(portal: dict) -> dict:
    try:
        # Create a BacdiveClient object with the provided email and password
        bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)
        
        # Search for the given species name in Bacdive
        species_name = portal['query']['name']
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
    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")
    
async def data_processing(retrieve_data: dict) -> str:
    try:
        return convert_to_string({str(k): v for k, v in retrieve_data.items()})
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")
        