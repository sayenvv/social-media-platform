# SOCIAL MEDIA PLATFORM

The social media platform is essentially a simple platform developed using Django REST Framework. Our project adheres to a clean coding standard. To maintain these standards, I have implemented pre-commit hooks in our project, which will clean the data before committing the staged changes.


## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Postman_Collection](#postman_collection)
- [Directory_Structure](#directory_structure)
  

## Features

- list friends
- search users with email id or name
- list users with paginated results
- sent friend request
- accept friend requests
- reject friend requests

## Dependencies

- rest_framework
- authtoken
- allauth
- drf_yasg
- pre commit
- dozzler
- docker

## Installation

1. First, clone the repository:

    ```bash
    git clone https://github.com/sayenvv/social-media-platform.git
    ```
2. Second,checkout to development branch
   ```bash
    git checkout develop
    ```

3. Install dependencies:

    ```bash
    docker compose build
    docker compose up
    ```

4. Migrations:
 
    ```bash
    docker compose exec social_networking bash 
    python manage.py migrate
    ```

5. Swagger API documentation:
 
    ```bash
    http://localhost:8000/api_docs/
    ```

6. Project logs:

   You can get logs for separate containers here. You can check them using Dozzler.
   After running the project, navigate to
 
    ```bash
    http://localhost:9999
    ```
## Usage


## Postman_Collection

Run and tests in postman link below

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/19381284-1dc321e5-6f2d-4753-b57e-bbc8cca4ea52?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19381284-1dc321e5-6f2d-4753-b57e-bbc8cca4ea52%26entityType%3Dcollection%26workspaceId%3D6109cd70-e86a-4a55-8775-9fbe6ac537a5#?env%5Baccuknox%20environment%5D=W3sia2V5IjoiYXV0aF9wcmVmaXgiLCJ2YWx1ZSI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9hcGkvdjAvYXV0aCIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0In0seyJrZXkiOiJhcHBfcHJlZml4IiwidmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvYXBpL3YwIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQifSx7ImtleSI6ImF1dGhUb2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSJ9LHsia2V5IjoiZW1haWxfYXV0aCIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSJ9LHsia2V5IjoicGFzc3dvcmRfYXV0aCIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSJ9LHsia2V5IjoiZnJpZW5kX3JlcXVlc3RfZW1haWwiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkifSx7ImtleSI6ImZyaWVuZF9yZXF1ZXN0X2lkIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55In1d)

Steps:

- Click on the link `Run in Postman`.
- Click on the "Fork Collection" button on the popup page.
- Click on "sayen-vv's Fork Collection" button on the next page.
- You now have the collection for AccuKnox.



## Directory_Structure
```
📦
 ┣ 📂 social networking app - accuknox app
 ┣ 📂 social networking media - accuknox project
 ┣ 📜 .gitignore
 ┣ 📜 .pre-commit-config.yaml
 ┣ 📜 db.sqlite3
 ┣ 📜 docker-compose.yml -  docker compose configurations
 ┣ 📜 manage.py
 ┣ 📜 python.dockerfile
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
 ```
