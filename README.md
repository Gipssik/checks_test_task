# Project setup instruction

## Requirements

- [Docker](https://www.docker.com/get-started) (for containerization)

## Running the project

1. Make sure to create `.env` file with the following content:

    ```bash
    ENV=DEV
    PORT=4000
    SECRET_KEY=secret
    DB_USER=postgres
    DB_PASS=postgres
    DB_HOST=postgres
    DB_NAME=postgres
    REDIS_HOST=redis
    ```
    
    You can change the variables if needed.

2. Run `docker-compose build` to build the project.
3. Run `docker-compose up` to start the project.
4. Open [http://localhost:4000/docs](http://localhost:4000/docs) in your browser.
