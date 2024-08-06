from config import BACDIVE_EMAIL, BACDIVE_PASSWORD
import bacdive

# Get bacdive data
async def bacdive_retrieve(species_name: str):
    try:
        bacdive_client = bacdive.BacdiveClient(BACDIVE_EMAIL, BACDIVE_PASSWORD)
        bacdive_count = bacdive_client.search(taxonomy=species_name)
        # print(bacdive_count, 'strains found.')
        
        bacdive_dict: dict = {}
        # filter=['BacDive-ID', 'species']

        k = 0

        for v in bacdive_client.retrieve():
            bacdive_dict[k] = v 
            k = k + 1
        
        return bacdive_dict
    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving data: {str(e)}")
    
async def bacdive_data_processing(retrieve_data):
    try:
        return {str(k): v for k, v in retrieve_data.items()}
    
    except Exception as e:
        raise Exception(f"An error occurred while processing data: {str(e)}")
        