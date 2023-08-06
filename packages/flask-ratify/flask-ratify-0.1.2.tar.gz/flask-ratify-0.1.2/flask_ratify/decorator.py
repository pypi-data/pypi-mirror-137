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

from functools import update_wrapper
from flask import make_response, request, jsonify
from .core import *
import logging

LOG = logging.getLogger(__name__)


def ratify(*args, **kwargs):
    _options = kwargs

    def decorator(f):
        def wrapped_function(*args, **kwargs):

            status, message = ratify_request(request, _options['schema'])
            if status:
                resp = make_response(f(*args, **kwargs))
                return resp
            else:
                resp = make_response(jsonify({"errors": message}), 400)
                return resp

        return update_wrapper(wrapped_function, f)

    return decorator

