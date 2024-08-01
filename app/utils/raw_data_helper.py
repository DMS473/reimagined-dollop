def raw_data_helper(raw_data) -> dict:
    if not raw_data or not isinstance(raw_data, dict):
        raise ValueError("Invalid raw_data data.")
    
    return {
        "id": str(raw_data["_id"]),
        "slug": raw_data["slug"],
        "data": raw_data["data"],
    }