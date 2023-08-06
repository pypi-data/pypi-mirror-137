# Python Web Robot Builder

[![Build Status](https://travis-ci.org/OpenCIAg/py-robot.svg?branch=master)](https://travis-ci.org/OpenCIAg/py-robot)
[![PyPI version](https://badge.fury.io/py/ciag-robot.svg)](https://badge.fury.io/py/ciag-robot)
[![Maintainability](https://api.codeclimate.com/v1/badges/4116e2ba99ce56e1397e/maintainability)](https://codeclimate.com/github/OpenCIAg/py-robot/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4116e2ba99ce56e1397e/test_coverage)](https://codeclimate.com/github/OpenCIAg/py-robot/test_coverage)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT)



The main idea of py-robot is to simplify the code, and improve the performance of web crawlers.

## Install

```sh
pip install ciag-robot
```


## Intro

Bellow we have a simple example of crawler that needs to get a page, and for each specific item get another page.
Because it was written without the use of async requests, it will make a request and make the another one only when the previous has finished.

```py
# examples/iot_eetimes.py

import requests
import json

from lxml import html
from pyquery.pyquery import PyQuery as pq

page = requests.get('https://iot.eetimes.com/')
dom = pq(html.fromstring(page.content.decode()))

result = []
for link in dom.find('.theiaStickySidebar ul li'):
    news = {
        'category': pq(link).find('span').text(),
        'url': pq(link).find('a[href]').attr('href'),
    }
    news_page = requests.get(news['url'])
    dom = pq(news_page.content.decode())
    news['body'] = dom.find('p').text()
    news['title'] = dom.find('h1.post-title').text()
    result.append(news)

print(json.dumps(result, indent=4))

```

We can rewrite that using py-robot, and it will look like that:


```py
# examples/iot_eetimes2.py

import json
from robot import Robot
from robot.collector.shortcut import *
import logging

logging.basicConfig(level=logging.DEBUG)

collector = pipe(
    const('https://iot.eetimes.com/'),
    get(),
    css('.theiaStickySidebar ul li'),
    foreach(dict(
        pipe(
            css('a[href]'), attr('href'), any(),
            get(),
            dict(
                body=pipe(css('p'), as_text()),
                title=pipe(css('h1.post-title'), as_text()),
            )
        ),
        category=pipe(css('span'), as_text()),
        url=pipe(css('a[href]'), attr('href'), any(), url())
    ))
)

with Robot() as robot:
    result = robot.sync_run(collector)
print(json.dumps(result, indent=4))

```

Now all the requests will be async, so it will start all the requests for each item at the same time, and it will improve the performance of the crawler.
