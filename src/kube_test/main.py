import logging
import os
from datetime import datetime, timedelta

import pytz
import requests
import uvicorn
import yaml
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from articles.article import Article
from articles.article_collection import ArticleCollection

app = FastAPI(title="Kubernetes Deployment Test",
              description="This is a very simple project",
              version="0.0.1",
              docs_url="/")

# TODO fix logging
logger = logging.getLogger('gunicorn.error')
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel('INFO')


config_dir = os.getenv('CONFIG_PATH')

with open(f'{config_dir}/config.yaml') as settings_file:
    configs = yaml.load(settings_file)


@app.get('/get_last_run_info')
def get_last_run_info():
    response = {'last_run': os.environ['LAST_RUN'] + ' UTC', 'articles_crawled': os.environ['ARTICLES_CRAWLED']}
    json_resp = jsonable_encoder(response)
    return JSONResponse(json_resp)


@app.on_event('startup')
@repeat_every(seconds=60)
def scrape():
    tz = pytz.timezone(configs['zeit.de']['timezone'])
    now = datetime.now(tz)
    fastapi_logger.error(f'starting scrape at {now}')

    for day in range(0, 2):
        crawl_date = now - timedelta(days=day)
        crawl_date_str = crawl_date.strftime('%Y-%m-%d')
        request_url = configs['zeit.de']['crawl_url'] + crawl_date_str
        article_collection = ArticleCollection()

        try:
            fastapi_logger.error(f'sending request to {request_url}')
            response = requests.get(url=request_url)
        except Exception as e:
            fastapi_logger.error(f'something went wrong with request: {e}')

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.findAll('article', {'class': 'zon-teaser-news'})
            if not articles:
                fastapi_logger.error('no articles found, stopping')
                break

            for tag in articles:
                publish_time = tag.find('time', {'class': 'zon-teaser-news__date'}).attrs['datetime']
                category = tag.find('span', {'class': 'zon-teaser-news__kicker'}).text
                headline = tag.find('span', {'class': 'zon-teaser-news__title'}).text

                article_collection.add(Article(category=category.strip(),
                                               headline=headline.strip(),
                                               publish_time=publish_time))
                for article in article_collection:
                    logger.error(article)
                # TODO store articles somewhere
        except Exception as e:
            logger.error(f'something went wrong when extracting articles: {e}')

    fastapi_logger.error(f'scraped {len(article_collection)} articles')
    os.environ['LAST_RUN'] = str(now)
    os.environ['ARTICLES_CRAWLED'] = str(len(article_collection))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug', debug=True)
