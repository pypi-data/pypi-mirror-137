from typing import Callable
from functools import wraps
from jinja2 import Environment, BaseLoader
from flask import Flask, url_for, Response

# Jinja template for the sitemap
SITEMAP = """<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  {% for url in urlset %}
    <url>
      {% for arg, value in url.items() %}
        <{{arg}}>{{ value }}</{{arg}}>
      {% endfor %}
    </url>
  {% endfor %}
</urlset>"""


class Sitemapper:
    def __init__(self, app: Flask) -> None:
        self.app = app  # Store the flask app instance
        self.urlset = []  # A list to store urls for the sitemap

    def include(self, **kwargs) -> Callable:
        """A decorator for route functions to add them to the sitemap"""

        def decorator(func: Callable) -> Callable:
            with self.app.app_context():
                url = {
                    "loc": url_for(
                        func.__name__,
                        _external=True,
                        _scheme=self.app.config.get("PREFFERED_URL_SCHEME", "http"),
                    )
                }

            url.update(kwargs)
            self.urlset.append(url)

            @wraps(func)
            def wrapper(*args, **kwargs):
                with self.app.app_context():
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def generate(self):
        """Creates the response for the sitemap route"""
        template = Environment(loader=BaseLoader).from_string(SITEMAP)
        xml = template.render(urlset=self.urlset)
        return Response(xml, mimetype="text/xml")
