# -*- coding: utf-8 -*-
"""
    core
    ~~~~
    flask-ratify is a simple extension to Flask allowing you to ratify (validate) requests
    using jsonschema

    jsonschema is supported for headers, params, and body (json only)

    For schema details used in flask-ratify, see docs/schema.md
    For jsonschema details, check https://pypi.org/project/jsonschema/ and https://json-schema.org/understanding-json-schema/

    :copyright: (c) 2022 by Parvesh Garg.
    :license: Apache Software License 2.0, see LICENSE for more details.
"""

from jsonschema import Draft7Validator
import logging
import re


LOG = logging.getLogger(__name__)

RegexObject = type(re.compile(''))


def ratify_request(request, schema):
    method = request.method
    if method not in schema:
        LOG.info(
            "schema for method {} in route {} is not specified".format(method, request.uri)
        )
        return True, "Not Implemented"

    _schema = schema[method]

    err = {
        "header": [],
        "json_body": [],
        "args": []
    }
    _h = _j = _a = True
    if 'headers' in _schema:
        v = Draft7Validator(_schema['headers'])
        hh = {kk.lower(): vv for kk, vv in request.headers}
        logging.error(hh)
        for ve in v.iter_errors(hh):
            err["header"].append(ve.message)
            _h = False

    if 'json_body' in _schema:
        v = Draft7Validator(_schema['json_body'])
        for ve in v.iter_errors(request.json):
            err["json_body"].append(ve.message)
            _j = False

    if 'args' in _schema:
        v = Draft7Validator(_schema['args'])
        for ve in v.iter_errors(request.args.to_dict()):
            err['args'].append(ve.message)
            _a = False

    return (_h and _j and _a), err


def probably_regex(maybe_regex):
    if isinstance(maybe_regex, RegexObject):
        return True
    else:
        common_regex_chars = ['*', '\\', ']', '?', '$', '^', '[', ']', '(', ')']
        # Use common characters used in regular expressions as a proxy
        # for if this string is in fact a regex.
        return any((c in maybe_regex for c in common_regex_chars))


def try_match(request_origin, maybe_regex):
    """Safely attempts to match a pattern or string to a request origin."""
    if isinstance(maybe_regex, RegexObject):
        return re.match(maybe_regex, request_origin)
    elif probably_regex(maybe_regex):
        return re.match(maybe_regex, request_origin, flags=re.IGNORECASE)
    else:
        try:
            return request_origin.lower() == maybe_regex.lower()
        except AttributeError:
            return request_origin == maybe_regex
