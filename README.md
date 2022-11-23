# Feed Manager
This project is a RSS scraper and feed manager backend service with `python 3.10`. The service is for saving RSS feeds to a database and users can read and bookmark them.
This is developed using FastAPI and Postgresql database.

## Run via docker compose

Just run following command: (supposed to docker and docker compose have been installed before)
### Test:
```shell script
docker-compose -f docker-compose-test.yml up --build    
```
### Web Service
```shell script
docker-compose up --build
```
Project will run on http://localhost:8000

* You can see OpenApi documentation on http://localhost:8000/swagger
