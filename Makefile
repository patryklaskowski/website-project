DOCKER_TAG="website_project"

init:
	curl -sSL https://install.python-poetry.org | python3 - --version "1.6.1"
	poetry install

run:
	export FLASK_DEBUG=true && \
	poetry run python website_project/main.py

docker-build:
	docker build . --tag $(DOCKER_TAG):latest --file Dockerfile

docker-run: docker-build
	docker run \
		-it --rm \
		--name website_project_local \
		-p 5000:5000 \
		--env FLASK_DEBUG=false \
		$(DOCKER_TAG):latest

dockerhub-run:
	docker pull patryklaskowski/$(DOCKER_TAG):latest
	docker run \
		-it --rm \
		--name website_project_dockerhub \
		-p 5000:5000 \
		--env FLASK_DEBUG=false \
		patryklaskowski/$(DOCKER_TAG):latest

docker-publish:
	# DockerHub: https://hub.docker.com/r/patryklaskowski/website_project
	docker tag $(DOCKER_TAG):latest patryklaskowski/$(DOCKER_TAG):latest
	@echo "$(DOCKER_PASSWORD)" | docker login --username patryklaskowski --password-stdin
	docker push patryklaskowski/$(DOCKER_TAG):latest
	docker logout

test:
	poetry run python -m pytest -v

docker-test: docker-build
	docker run -it --rm --name website_project_test $(DOCKER_TAG):latest make test
