# django-bootstrap v5

This package builds on top of the excellent [django-bootstrap4](https://github.com/zostera/django-bootstrap4) package.

[![CI](https://github.com/zelenij/django-bootstrap-v5/workflows/CI/badge.svg?branch=main)](https://github.com/django-bootstrap-v5/actions?workflow=CI)
[![Coverage Status](https://coveralls.io/repos/github/django-bootstrap-v5/badge.svg?branch=main)](https://coveralls.io/github/django-bootstrap-v5?branch=main)
[![Latest PyPI version](https://img.shields.io/pypi/v/django-bootstrap-v5.svg)](https://pypi.python.org/pypi/django-bootstrap-v5)
[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Bootstrap 5 integration for Django.

## Package name

Unfortunately, someone squatted on the django-bootstrap-v5 (as well as 6, 7, 8 etc) name in PyPi in 2013, so I had to modify the name of this package accordingly.

## Goal

The goal of this project is to seamlessly blend Django and Bootstrap 5.

## Requirements

Python 3.6 or newer with Django >= 2.2 or newer.

## Documentation

The full documentation is at https://django-bootstrap-v5.readthedocs.io/

## Installation

1. Install using pip:

    ```shell script
    pip install django-bootstrap-v5
    ```
   
   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = (
       # ...
       "bootstrap5",
       # ...
   )
   ````

3. In your templates, load the `bootstrap5` library and use the `bootstrap_*` tags:

## Example template

```jinja
{% load bootstrap5 %}

{# Display a form #}

<form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
```

Demo
----

A demo app is provided in `demo`. You can run it from your virtualenv with `python manage.py runserver`.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/zelenij/django-bootstrap-v5/issues


License
-------

You can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.


Author
------

Developed and maintained by [Andre Bar'yudin](https://www.baryudin.com)

Original authors: 

* [Zostera](https://zostera.nl)
* [Dylan Verheul](https://github.com/dyve)

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see [AUTHORS.md](AUTHORS.md) for a list of contributors.
