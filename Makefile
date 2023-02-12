###################
### Virtual ENV ###
###################
env-create:
	conda create -n pattern python=3.11
env-delete:
	conda env remove -n pattern
env-init:
	pip install pipenv
env-activate:
	source ~/anaconda3/etc/profile.d/conda.sh; conda activate pattern
	export PYTHONPATH=$(pwd)
requirements-prod: Pipfile 
	pipenv requirements --hash > requirements-prod.txt
requirements-dev: env-init Pipfile 
	pipenv requirements --hash --dev > requirements-dev.txt
install-requirements-prod: requirements-prod
	pip3 install -r requirements-prod.txt
install-requirements-dev: requirements-dev
	pip3 install -r requirements-dev.txt

.PHONY: env-activate env-create kivy-install env-init requirements-prod requirements-dev install-requirements-prod install-requirements-dev 

###################
###### Build ######
###################

app: src/app.py
	pyclean . -q
	cd src && python app.py
	pyclean . -q
format:
	python -m black .
lint:
	python -m pylint src/. tests/.
clean:
	pyclean .