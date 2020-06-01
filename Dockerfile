FROM python:3.7
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        ffmpeg; \
    rm -rf /var/lib/apt/lists/*;
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/app/main.py"]
