# -*- coding: utf-8 -*-
"""
    decorator
    ~~~~
    flask-ratify is a simple extension to Flask allowing you to ratify (validate) requests
    using jsonschema

    jsonschema is supported for headers, params, and body (json only)

    For schema details used in flask-ratify, see docs/schema.md
    For jsonschema details, check https://pypi.org/project/jsonschema/ and https://json-schema.org/understanding-json-schema/

    :copyright: (c) 2022 by Parvesh Garg.
    :license: Apache Software License 2.0, see LICENSE for more details.
"""

from flask import request, make_response, jsonify
from .core import *
import sys
try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus


class FlaskRatify(object):

    def __init__(self, app=None, schema=None, **kwargs):
        self.schema = schema
        self._options = kwargs
        if self.schema is None:
            print("Failed to load schema, None", file=sys.stderr)
            raise ValueError("schema= is required")
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        ratify_before_request = make_before_request_function(self.schema)
        app.before_request(ratify_before_request)


def make_before_request_function(schema):
    def ratify_before_request():
        normalized_path = unquote_plus(request.path)
        for route in sorted(schema, reverse=True):
            if try_match(normalized_path, route):
                logging.info("Request path %s matches schema resource %s", request.path, route)
                _path_schema = schema[normalized_path]
                status, message = ratify_request(request, _path_schema)

                if not status:
                    logging.error("Validation failure")
                    resp = make_response(jsonify({"errors": message}), 400)
                    return resp

    return ratify_before_request
