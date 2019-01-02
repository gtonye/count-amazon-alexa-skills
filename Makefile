clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {}

lint:
	flake8 --exclude=.tox --exclude=.env

docker-build:
	docker build \
	--file=./Dockerfile \
	-t amazon-skill-count ./

docker-run: docker-build
	docker run -it --rm amazon-skill-count