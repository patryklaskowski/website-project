DOCKER_TAG="website_project"
VENV_NAME=".venv"


venv:
	rm -rf ./$(VENV_NAME)
	python3 -m venv $(VENV_NAME)
	source $(VENV_NAME)/bin/activate; \
	make install

install:
	python -m pip install -U pip
	python -m pip install -r requirements.txt
	python -m pip install -e .

run:
	export FLASK_DEBUG=true && \
	python website_project/main.py

docker-build:
	docker build . --tag $(DOCKER_TAG):latest --file Dockerfile

docker-run: docker-build
	docker run \
		-it --rm \
		--name website_project_local \
		-p 5000:5000 \
		--env FLASK_DEBUG=false \
		--env-file .env \
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
	python -m pytest -v

docker-test: docker-build
	docker run -it --rm --name website_project_test $(DOCKER_TAG):latest make test
