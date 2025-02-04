### Build stage
FROM nikolaik/python-nodejs:python3.10-nodejs19 AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

### Runtime stage
FROM nikolaik/python-nodejs:python3.10-nodejs19-slim
COPY --from=builder /app /app
WORKDIR /app/

CMD python3 -m BrandrdXMusic
