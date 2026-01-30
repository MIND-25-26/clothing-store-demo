## clothing store lecture example

# N.B. Updated example here: https://github.com/fw-teaching/fastapi-postgresql-demo 


### For local real-time development using docker-compose

Rename `.env-example` to `.env` to override the `MODE=production`set in the `Dockerfile`. Note that this needs a valueless declaration of `MODE` in `docker-compose.yml`

To run the container locally:
`docker-compose up --build`
