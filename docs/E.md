# Project Structure

```
.
├── README.md
├── __pycache__                   # Compiled Python files
├── app                           # Main application directory
│   ├── __pycache__               # Compiled Python files
│   ├── config.py                 # Configuration settings
│   ├── crud                      # CRUD operations
│   │   ├── __pycache__           # Compiled Python files
│   │   ├── portal_crud.py        # CRUD operations for portals
│   │   ├── raw_data_crud.py      # CRUD operations for raw data
│   │   └── term_crud.py          # CRUD operations for terms
│   ├── database                  # Database connections and configurations
│   │   ├── __pycache__           # Compiled Python files
│   │   └── mongo.py              # MongoDB connection setup
│   ├── log                       # Log files
│   ├── main.py                   # Entry point for the FastAPI application
│   ├── models                    # Data models
│   │   ├── __pycache__           # Compiled Python files
│   │   ├── portal_model.py       # Model for portals
│   │   ├── raw_data_model.py     # Model for raw data
│   │   └── term_model.py         # Model for terms
│   ├── operations                # Data retrieval and processing
│   │   ├── __pycache__           # Compiled Python files
│   │   ├── bacdive.py            # BacDive data retrieval
│   │   ├── gbif.py               # GBIF data retrieval
│   │   ├── ncbi.py               # NCBI data retrieval
│   │   └── wikidata.py           # Wikidata retrieval
│   ├── routers                   # API route handlers
│   │   ├── __pycache__           # Compiled Python files
│   │   ├── portal_router.py      # Router for portal endpoints
│   │   ├── raw_data_router.py    # Router for raw data endpoints
│   │   └── term_router.py        # Router for term endpoints
│   └── utils                     # Utility functions and decorators
│       ├── __pycache__           # Compiled Python files
│       ├── decorator             # Decorators for logging
│       │   └── app_log_decorator.py # Logging decorators
│       ├── helper                # Helper functions
│       │   ├── func_helper.py    # General helper functions
│       │   └── response_helper.py # Response handling functions
│       ├── message               # Message enumerations
│       │   └── message_enum.py   # Enum definitions for messages
│       └── middleware            # Middleware components
│           ├── __pycache__       # Compiled Python files
│           └── request_log_middleware.py # Middleware for logging requests
├── app.log                       # Application log file
├── docs                          # Documentation files
│   ├── assets                    # Asset files for documentation
│   └── index.md                  # Main documentation index
├── mkdocs.yml                    # MkDocs configuration file
├── requirements.txt              # Project dependencies
└── tree_structure.txt            # Directory tree structure
```