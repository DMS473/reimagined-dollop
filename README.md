# INNAKM Rest API Documentation
For code requirements, please visit [INNAKM Github Repository](https://github.com/fikridean/INNAKM).

## Installations
* `git clone https://github.com/fikridean/INNAKM.git` - Clone the project from INNAKM Github Repository.
* `pip install -r requirements.txt` - Install the required dependencies
* `fastapi dev app/main.py` - Run FastAPI.

## Project Structure

This document outlines the structure of the project, detailing the purpose of each directory and file.

### Root Directory

- **README.md** - The main documentation file for the project.
- **mkdocs.yml** - The configuration file for the documentation generator.
- **requirements.txt** - The file containing the required dependencies for the project.

### app/ - Application Code

#### common/ - Common Utilities and Helper Functions
- **message/**
  - **message_enum.py** - Defines message enums.

#### config.py - Configuration Settings
- Contains settings for the application.

#### crud/ - CRUD Operations
- **portal_crud.py** - CRUD operations for the portal entity.
- **raw_data_crud.py** - CRUD operations for the raw data entity.

#### database/ - Database-Related Code
- **mongo.py** - Handles MongoDB database connection and operations.

#### main.py - Main Entry Point
- The main file that starts the application.

#### models/ - Data Models
- **portal_model.py** - Defines the portal data model.
- **raw_data_model.py** - Defines the raw data model.

#### operations/ - Various Operations
- **bacdive_retrieval.py** - Handles BacDive data retrieval operations.
- **gbif_retrieval.py** - Handles GBIF data retrieval operations.
- **ncbi_retrieval.py** - Handles NCBI data retrieval operations.
- **(Placeholder)** - Placeholder for another operation file.

#### routers/ - API Routers
- **portal_router.py** - Defines the router for the portal API.
- **raw_data_router.py** - Defines the router for the raw data API.

#### utils/ - Utility Functions
- **response_helper.py** - Helper functions for generating API responses.

### docs/ - Documentation Files
- **index.md** - The main documentation file for the project.

### (Placeholder) - Placeholder for another file or directory
