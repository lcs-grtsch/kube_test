FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./src /app
COPY ./config /config
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV CONFIG_PATH="/config"
ENV LAST_RUN="Not run yet"
ENV ARTICLES_CRAWLED="0"

CMD ["python", "kube_test/main.py"]