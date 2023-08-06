# API Identity Server

## Install

**Install package**

    pip install microserviceapiidentity

**Configuration**

...


**Migrations**

    set -x CONFIG ~/Develop/stackmicroservices/identity/extra/config.ini
    set -x FLASK_APP MicroserviceApiIdentity.app:init_api

    flask get-migrations-dir

    flask db show -d ""


Upgrade

    CONFIG=extra/config.ini ./ms-identity-db-upgrade


## Run

    uwsgi --ini uwsgi.ini

## Endpoints

...

## Dockerize

**Docker Image**

    docker build -t registry.gitlab.com/stackmicroservices/identity .

    docker push registry.gitlab.com/stackmicroservices/identity

**Docker Compose**

    docker-compose up