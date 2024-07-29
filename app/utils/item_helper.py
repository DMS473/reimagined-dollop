def item_helper(item) -> dict:
    if not item or not isinstance(item, dict):
        raise ValueError("Invalid item data.")
    
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"],
        "price": item["price"]
    }