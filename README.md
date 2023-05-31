# Place App

This is a Django REST Framework application for managing places.

## Features

- CRUD operations for places (create, read, update, delete)
- Search for the nearest place based on coordinates
- API documentation with Swagger UI

## Installation and Setup

1. Clone the repository:

```shell
git clone https://github.com/ostapT/gis_place_API.git
```
2. Run with Docker (Docker should be installed)
```shell
docker-compose build
docker-compose up
```
# API Endpoints

- GET /places/: Get a list of all places.
- POST /places/: Create a new place.
- GET /places/{pk}/: Get details of a specific place.
- PATCH /places/{pk}/: Update details of a specific place.
- DELETE /places/{pk}/: Delete a specific place.
- GET /places/nearest/: Find the nearest place based on coordinates.
- GET /doc/swagger/: explore the documentation using the Swagger UI.
