FROM debian:sid-slim

WORKDIR /usr/src/app

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    build-essential                            \
    python                                     \
    python3                                    \
    python-setuptools                          \
    python3-pip                                \
    ca-certificates curl firefox               \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz | tar xz -C /usr/local/bin

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY config.py count_amazon_skills.py Makefile ./

CMD ["make", "run"]
