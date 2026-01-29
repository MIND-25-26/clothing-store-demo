# rahti2-fastapi 

## First deployment to Rahti2 OpenShift

- In the OpenShift web UI, add a PostgreSQL (persistent) instance from the Developer Catalog
- Add this app using Import from Git
- Build the DB_URL string using the database-name, database-password and database-user from the Secrets section (postgresl)
- Check the postgresl servername by clicking on the PostgreSQL instance and opening the Service. check the hostname (e.g. postgresql.my-project.svc.cluster.local) and the port (5432). The first subdomain, "postgresql" in this case is enough.
- The format of the DB_URL is `postgres://database-user:database-password@hostname:5432/database-name` so something like: `postgres://user37A:WSWeEHjhgF823GO@hostname:5432/sampledb`
- Add the DB_URL as an Environment Variable in the Edit Deployment section of the fastapi app instance.


### For push-to-deploy to Rahti2

- Copy the GitHub Webhook url from the BuildConfig of the app instance (cklick the instance, select the Build)
- Set up the Webhook on GitHub (remember application/json)

Note: OpenShift wants the main branch to be named *master* by default, you have two options:
1. Push to origin/master to deploy
2. Change the setting in Openshift to *main*:    
    Edit BuildConfig ==> Show advanced git options ==> Git reference: `main`

See also: https://fastapi.tiangolo.com/deployment/docker/



### For local real-time development using docker-compose

Rename `.env-example` to `.env` to override the `MODE=production`set in the `Dockerfile`. Note that this needs a valueless declaration of `MODE` in `docker-compose.yml`

To run the container locally:
`docker-compose up --build`
