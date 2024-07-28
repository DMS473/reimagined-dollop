def portal_helper(portal) -> dict:
    if not portal or not isinstance(portal, dict):
        raise ValueError("Invalid portal data.")
    
    return {
        "id": str(portal["_id"]),
        "name": portal["name"],
        "base_url": portal["base_url"],
        "query": portal["query"]
    }