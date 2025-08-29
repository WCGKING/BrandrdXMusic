FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN python3 -m pip install --upgrade pip setuptools
RUN apt-get update && apt-get install -y git
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD python3 -m BrandrdXMusic
