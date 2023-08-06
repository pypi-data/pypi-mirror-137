flask-ratify
============

|Latest Version| |Supported Python versions| |License|

A Flask extension for ratifying (validating) requests

This package uses the `jsonschema <https://pypi.org/project/jsonschema/>`__ for validating the requests. A package
specific schema has been implemented on top of jsonschema to validate headers, args, and json\_body.

Installation
------------

Install the extension with using pip, or easy\_install.

.. code:: bash

    $ pip install -U flask-ratify

Usage
-----

This package exposes a Flask extension which can enforce validations on selected routes. Routes can be specified as
regexes as well. The package also contains a decorator, for those who prefer this approach.

flask-ratify returns status 400

Simple Usage
~~~~~~~~~~~~

.. code:: python

    from flask import Flask
    from flask_ratify import FlaskRatify

    users_schema = {
        "POST": {
            "headers": {
                "type": "object",
                "properties": {
                    "authorization": {"type": "string"}
                },
                "required": ["authorization"]
            },
            "json_body": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["user_id", "email"],
                "additionalProperties": False,
            },
            "args": {
                "type": "object"
                # add further validations if needed
            }
        },
        "GET": {
            # Add validations for GET
        }
    }

    schema = {
        "/users": users_schema
    }

    app = Flask(__name__)
    FlaskRatify(app, schema)

    @app.route("/users", methods=["POST", "GET"])
    def create_user():
         = request.args.get("


Schema
~~~~~~

flask-ratify schema follows a simple model of it's own on top of json-schema. For better understanding of json-schema, read

-   `Python jsonschema package documentation <https://python-jsonschema.readthedocs.io/en/latest/>`__
-   `Understanding jsonschema <https://json-schema.org/understanding-json-schema/>`__


.. code:: python

    {
        "endpoint": {
            "http method": {
                "headers": {
                    "type": "object" # For headers this is always object
                    "properties": {
                        "header_name": {"type": "string"} # header names should be lower cased,
                                                          #  rest any jsonschema element can be used
                    #   ...
                    },
                    "required": ["header1", "header2"], # Optional
                    "additionalProperties": False,      # Boolean, Optional
                },
                "args": {
                    "type": "object" # For args this is always object
                    "properties": {
                        "arg_name": {"type": "string"} # any jsonschema element can be used
                    # ...
                    },
                    "required": ["arg1", "arg2"], # Optional
                    "additionalProperties": False,      # Boolean, Optional
                },
                "json_body": {
                    "type": "object|array|..." # json_body can follow any type as per jsonschema
                    "properties": {
                        "field_name": {"type": "string"} # any jsonschema element can be used
                    # ...
                    },
                    "required": ["field1", "field2"],   # Optional
                    "additionalProperties": False,      # Boolean, Optional
                }
            }
        }
    }


Troubleshooting
---------------

If things aren't working as you expect, enable logging to help understand what is going on under the hood, and why.

.. code:: python

    logging.getLogger('flask_').level = logging.DEBUG


TODO
----

-   Test cases
-   Schema validation for debugging
-   Automatic API documentation generation from schema
-


Contributing
------------

Questions, comments or improvements?
Please create an issue on `Github <https://github.com/parveshgarg/flask-ratify>`__

For code contributions, please create an issue and raise a pull request.


Credits
-------

-   `jsonschema <https://pypi.org/project/jsonschema/>`__


.. |Latest Version| image:: https://img.shields.io/pypi/v/flask-ratify.svg
   :target: https://pypi.python.org/pypi/flask-ratify/
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/flask-ratify.svg
   :target: https://img.shields.io/pypi/pyversions/flask-ratify.svg
.. |License| image:: https://img.shields.io/:license-apache-blue.svg
   :target: https://pypi.python.org/pypi/flask-ratify/
