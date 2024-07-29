# INNAKM

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)

## Introduction
INNAKM is a project designed to manage portals with unique slugs. It ensures that each portal has a unique identifier (slug) and provides functionality to create and manage these portals using Python, Pydantic, and MongoDB.

## Features
- Create portals with unique slugs.
- Validate slug uniqueness before saving to the database.
- Handle database operations using MongoDB Motor.

## Installation
To install and set up the project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/fikridean/INNAKM.git
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Run FastAPI
    ```
    fastapi dev app/main.py
    ```