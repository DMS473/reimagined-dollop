from config import BACDIVE_EMAIL, BACDIVE_PASSWORD
import bacdive

# Get bacdive data
async def bacdive_retrieve(species_name: str):
    try:
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
    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")
    
async def bacdive_data_processing(retrieve_data):
    try:
        # Convert the retrieved data to a dictionary with string keys
        return {str(k): v for k, v in retrieve_data.items()}
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")
        