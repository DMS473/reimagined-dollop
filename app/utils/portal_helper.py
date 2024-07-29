def portal_helper(portal) -> dict:
    if not portal or not isinstance(portal, dict):
        raise ValueError("Invalid portal data.")
    
    return {
        "id": str(portal["_id"]),
        "name": portal["name"],
        "slug": portal["slug"],
        "base_url": portal["base_url"],
        "query": portal["query"]
    }

def portal_detail_helper(portal) -> dict:
    if not portal or not isinstance(portal, dict):
        raise ValueError("Invalid portal data.")
    
    return {
        "id": str(portal["_id"]),
        "name": portal["name"],
        "slug": portal["slug"],
        "base_url": portal["base_url"],
        "query": portal["query"],
        "retrieve_data_url": portal["retrieve_data_url"]
    }