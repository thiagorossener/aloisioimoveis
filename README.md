# Aloísio Imóveis

Real estate website and system built in Django and Vue.js for [Aloísio Imóveis](http://aloisioimoveis.com.br/)

[![Build Status](https://travis-ci.org/thiagorossener/aloisioimoveis.svg?branch=master)](https://travis-ci.org/thiagorossener/aloisioimoveis)
[![Coverage Status](https://coveralls.io/repos/github/thiagorossener/aloisioimoveis/badge.svg?branch=master)](https://coveralls.io/github/thiagorossener/aloisioimoveis?branch=master)
[![Code Health](https://landscape.io/github/thiagorossener/aloisioimoveis/master/landscape.svg?style=flat)](https://landscape.io/github/thiagorossener/aloisioimoveis/master)

![Aloísio Imóveis](http://res.cloudinary.com/dm7h7e8xj/image/upload/v1499797163/github-aloisioimoveis_tyxsk8.png)

## Features

* Create/Edit/Delete properties
* Search for properties
* Photo album
* Contact form
* Responsive

## Release Notes

Version 1.0.0
* Initial release

## How to develop?

1. Clone the repository
2. Create a virtualenv with Python 3.5
3. Activate your virtualenv
4. Install the dependencies
5. Set up the instance with the .env file
6. Run the tests

```console
git clone git@github.com:thiagorossener/aloisioimoveis.git aloisioimoveis
cd aloisioimoveis
python -m venv .aloisioimoveis
source .aloisioimoveis/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```

## Author

[Thiago Rossener](http://www.rossener.com)
