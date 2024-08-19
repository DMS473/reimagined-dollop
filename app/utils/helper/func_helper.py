import asyncio
from fastapi import HTTPException

import glob
import importlib.util
from urllib.parse import quote

from config import OPERATIONS_FOLDERS

from database.mongo import portal_collection

# pre-process url to handle special characters
async def pre_process_url(url: str) -> str:
    try:
        result = quote(url, safe=':/?=&')
        result = str(result)
        return result

    except Exception as e:
        raise Exception(f"An error occurred while pre-processing url: {str(e)}")

# add query to url if query exists
async def addQueryToURL(portal: dict) -> str:
    try:
        if len(portal['query']) == 0:
            return portal['base_url']
        
        query_str: str = ''
        
        for key in portal['query']:
            return_pre_process_url = await pre_process_url(portal['query'][key])
            query_str += f"{key}={return_pre_process_url}&"
        
        query_str = query_str[:-1]

        return f"{portal['base_url']}?{query_str}"
    
    except Exception as e:
        raise Exception(f"An error occurred while adding query to url: {str(e)}")
    
# Check if portal exists
async def portal_exists(slug: str) -> bool:
    portal = await portal_collection.find_one({"slug": slug}, {"_id": 0})
    return portal

async def check_params(params: list) -> list:
    try:
        if not params.species:
            raise HTTPException(status_code=400, detail="Species not found. Please re-check the species.")
        
        if not params.web:
            raise HTTPException(status_code=400, detail="Web not found. Please re-check the web.")
        
        return params
    
    except Exception as e:
        raise Exception(f"An error occurred while checking params: {str(e)}")

def convert_to_string(obj: any) -> any:
    if isinstance(obj, dict):
        # If it's a dictionary, apply the conversion recursively to each key-value pair
        return {k: convert_to_string(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If it's a list, apply the conversion recursively to each item in the list
        return [convert_to_string(i) for i in obj]
    else:
        # For all other data types, convert them to string
        return str(obj)

async def run_function_from_module(module_name: str, function_name: str, *args: any) -> any:
    # Dynamically import the module
    spec = importlib.util.spec_from_file_location(module_name, OPERATIONS_FOLDERS + '/' + module_name + ".py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the function from the module
    function = getattr(module, function_name)
    
    if asyncio.iscoroutinefunction(function):
        # If the function is async, await it
        return await function(*args)
    else:
        # Otherwise, call the sync function directly
        return function(*args)

def get_index_object_from_files(folder_path: str) -> list:
    index_objects_items: list = []
    # Find all Python files in the folder
    file_paths = glob.glob(folder_path + "/*.py")

    # Loop through each file
    for file_path in file_paths:
        # Get the module name from the file path
        module_name = file_path.split("/")[-1].split(".")[0]

        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if the module has the index_object attribute
        if hasattr(module, "index_object"):
            # Retrieve the index_object attribute and append it to the list
            index_objects_items.append(module.index_object)
        else:
            print(f"Warning: 'index_object' not found in {module_name}.")

    return index_objects_items

# Combine the index objects from all the operation files
index_objects = get_index_object_from_files(OPERATIONS_FOLDERS)

combined_index_object = {}

for index_object in index_objects:
    combined_index_object.update(index_object)

def get_var_from_module(module_name: str, var_name: str) -> any:
    # Dynamically import the module
    spec = importlib.util.spec_from_file_location(module_name, OPERATIONS_FOLDERS + '/' + module_name + ".py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the variable from the module
    return getattr(module, var_name)