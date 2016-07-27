# Ceres api

# Testing the API

In order to test the API we can use [curl](https://curl.haxx.se/) or [httpie.](https://github.com/jkbrzt/httpie#installation) For this documentation we'll be using Httpie.Httpie is a user friendly http client that's written in Python.
You can install httpie using pip

```
pip install httpie
```

## Basic usage

```
http http://127.0.0.1:8000/snippets/
```

# Authenticating with the API

If we try to create a new snippet with authenticating, the API will return an error.

```
http POST http://127.0.0.1:8000/snippets/ code="print 123"

{
    "detail": "Authentication credentials were not provided."
}
```

In order to make a successful request we need to include a username and password of a user already created.

```
http -a tom:password123 POST http://127.0.0.1:8000/snippets/ code="print 123"

{
    "id": 5,
    "owner": "elliot",
    "title": "foo",
    "code": "print 123",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```
If we're interacting with the API programmatically we need to explicitly provide the authentication credentials on each request.

GET, POST, HEAD, OPTIONS
