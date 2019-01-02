FROM debian:sid-slim

WORKDIR /usr/src/app

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    python \
    python3 \
    python-setuptools \
    python3-pip \
    ca-certificates curl firefox               \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz | tar xz -C /usr/local/bin

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY count_amazon_skills.py Makefile ./

CMD ["python3", "count_amazon_skills.py"]