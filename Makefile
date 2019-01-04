clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {}

lint:
	flake8 --exclude=.tox --exclude=.env

BROWSER_TYPE ?= "headless"
REPORT_TYPE ?= "minimal"
run:
	python3 count_amazon_skills.py \
	--browser-type ${BROWSER_TYPE} \
	--report-type ${REPORT_TYPE}

docker-build-and-run: docker-build docker-run

docker-build:
	docker build \
	--file=./Dockerfile \
	-t amazon-skill-count ./

ENV_FILE_ARG=
ifdef env-file
	ENV_FILE_ARG=--env-file=$(env-file)
endif
docker-run:
	docker run ${ENV_FILE_ARG} -it --rm amazon-skill-count
