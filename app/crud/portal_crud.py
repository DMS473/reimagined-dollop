from database.mongo import portal_collection
from utils.portal_helper import portal_helper
from bson import ObjectId

async def get_portals() -> list:
    # portals = [{
    #     "id": "66a6637243bf293120541f9f",
    #     "name": "WikiData-get-by-id",
    #     "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    #     "query": {
    #         "db": "taxonomy",
    #         "term": "Achromobacter"
    #     },
    # }]

    portals = []

    try:
        async for portal in portal_collection.find({}):
            portals.append(portal_helper(portal))
        return portals
    except Exception as e:
        raise Exception(f"An error occurred while retrieving portals: {str(e)}")