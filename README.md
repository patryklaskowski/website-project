# Website Project

---
## Requirements

- Set following environmental variables:
  - `MONGODB_DB_NAME` e.g. "website_project_database"
  - `MONGODB_USERNAME` e.g. "pl"
  - `MONGODB_PASSWORD` e.g. "developer"
---
## How to start

- Run web server the latest release using `docker`.
  See [patryklaskowski/website_project](https://hub.docker.com/r/patryklaskowski/website_project) on DockerHub
   ```bash
   make dockerhub-run
   ```

---
## Docker cheatsheet

### Run custom Docker container

1. Prepare `Dockerfile`
   ```dockerfile
   FROM python:3.9-alpine
   RUN apk update && \
       apk add bash
   ```

2. Build image named `my-example-image` based on `Dockerfile` in current directory (`.`)
    ```bash
    docker build . --tag my-example-image:latest --file Dockerfile
    ```
   
3. Run container executing bash command interactively
    ```bash
    docker run -it --rm -v $(pwd):/my-workspace my-example-image:latest bash
    ```
   - `-v` mounts current directory to `my-workspace` path in container

4. Publish image to DockerHub
   1. Tag image
      ```bash
      docker tag my-example-image:latest patryklaskowski/my-example-image:latest
      ```
   3. Log in to DockerHub
      ```bash
      docker login --username $DOCKER_USERNAME --password $DOCKER_PASSWORD
      ```
   4. Push your image to DockerHub
      ```bash
      docker push patryklaskowski/my-example-image:latest
      ```
