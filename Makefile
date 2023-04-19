VENV_NAME="my-env"

venv:
	rm -rf ./$(VENV_NAME)
	python3 -m venv $(VENV_NAME)
	source $(VENV_NAME)/bin/activate

install:
	python -m pip install -U pip
	python -m pip install -r requirements.txt

run:
	python website_project/main.py

cold-start: venv install run

clean:
	rm -rf ./$(VENV_NAME)
