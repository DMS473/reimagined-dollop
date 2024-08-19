def extract_last_nested_value(data):
    """
    Extract the last nested value from a dictionary, leaving the structure intact.
    """
    if isinstance(data, dict):
        if len(data) == 1:
            value = next(iter(data.values()))
            return extract_last_nested_value(value)
        else:
            return {k: extract_last_nested_value(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Process each item in the list
        return [extract_last_nested_value(item) for item in data]
    elif isinstance(data, str):
        return data
    else:
        return data

def process_objects(data_objects):
    """
    Process a list of objects to modify the `data` field such that it includes the last nested level.
    """
    processed_objects = []
    for obj in data_objects:
        processed_obj = obj.copy()
        if 'data' in processed_obj:
            processed_obj['data'] = extract_last_nested_value(processed_obj['data'])
        processed_objects.append(processed_obj)
    
    return {
        "status": 200,
        "success": True,
        "message": "Successfully get data",
        "data": processed_objects
    }

# Example data
data_list = [
    {
        "data": {
            "0": {
                "General": {
                    "description": "Aeromonas hydrophila LUHS TK-19-2 is a human pathogen that was isolated from The intestine of Carassius gibelio ."
                }
            }
        },
        "species": "Aeromonas hydrophila",
        "web": "bacdive"
    },
    {
        "data": {
            "ScientificName": "Aeromonas hydrophila"
        },
        "species": "Aeromonas hydrophila",
        "web": "ncbi"
    },
    {
        "data": {
            "descriptions": {
                "en": {
                    "value": "species of bacterium"
                }
            }
        },
        "species": "Aeromonas hydrophila",
        "web": "wikidata"
    },
    {
        "data": {
            "rank": "SPECIES",
            "order": "Enterobacterales",
            "family": "Aeromonadaceae",
            "genus": "Aeromonas",
            "class": "Gammaproteobacteria"
        },
        "species": "Aeromonas hydrophila",
        "web": "gbif"
    }
]

# Process the data
processed_data = process_objects(data_list)
print(processed_data)
