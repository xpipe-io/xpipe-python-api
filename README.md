# XPipe Python API

[![GitHub license](https://img.shields.io/github/license/xpipe-io/xpipe-python-api.svg)](https://github.com/xpipe-io/xpipe-python-api/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/xpipe_api)](https://pypi.org/project/xpipe_api/)

Python client for the XPipe API. This library is a wrapper for the raw [HTTP API](https://github.com/xpipe-io/xpipe/blob/master/openapi.yaml) and intended to make working with it more convenient.

```bash
python3 -m pip install xpipe_api
```

You can find the documentation at https://docs.xpipe.io/guide/python-api. Complementary to the documentation, you can find the code examples from the docs in `samples`.

## Development

To run the test suite, you'll need to define the XPIPE_APIKEY env var.  This will allow the two "log in with the ApiKey 
rather than Local method" tests to work.  Here's the recommended method for running the tests with poetry:

```bash
cd /path/to/xpipe-python-api
poetry install
XPIPE_APIKEY=<api_key> poetry run pytest
```
