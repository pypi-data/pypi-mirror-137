[![Test](https://github.com/acdh-oeaw/django-gnd/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/django-gnd/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/acdh-oeaw/django-gnd/branch/master/graph/badge.svg?token=tbKyXmzYwa)](https://codecov.io/gh/acdh-oeaw/django-gnd)
[![PyPI version](https://badge.fury.io/py/django-gnd.svg)](https://badge.fury.io/py/django-gnd)


# django-gnd

A django package to query and store data from [Lobid's GND-API](https://lobid.org/gnd)

## install

`pip install django-gnd`

add `gnd` to INSTALLED_APPS:

```python
#  project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gnd',
    'example',
]
```

## features

see the example Project

### GND/LOBID autocomplete widget
