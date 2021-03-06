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

Possible endpoints
==================

GET messages/sent

### Auth

    POST    auth/                           - auth endpoint for clients
    POST    auth/login/                     - auth login for web api
    POST    auth/token/                     - returns a auth token for user
    POST    auth/revoke_token/              - deletes a auth token for an auth user

### Accounts

    GET     accounts/                       - all
    GET     accounts/<id>/                  - Detail of id
    GET     accounts/me/                    - returns information for current
                                              auth user.
    POST    accounts/                       - creates a new account                                 
    PUT     accounts/<id>/                  - updates account information
    DELETE  accounts/<id>/                  - deletes an account

    GET     accounts/<id>/friends/          - return list of friends
    GET     accounts/<id>/friends/incoming/ - return list of people that have you added as a friend
    GET     accounts/<id>/friends/outgoing/ - return list of people that you have added as a friend

    POST    accounts/<id>/friends/          - Create a new friend

### Friends

    GET     friends/                        - all user friends information(confirmed/pending)
    GET     friends/<id>/                   - detail of a friend

### Room    

    GET     room/                           - all
    GET     room/<id>/                      - Detail of id
    GET     room/<id>/messages/             - messages in that conversation id

    POST    room/<id>/messages/             - send a message to that conversation

    POST    room/<id>/                      - creates a new conversation
    PUT     room/<id>/                      - updates conversation information
    DELETE  room/<id>/                      - deletes a conversation

### Messages

    GET     messages/                       - all comments you have access to
    GET     messages/<id>/                  - detail of id

    POST    messages/<id>/
    PUT     messages/<id>/
    DELETE  messages/<id>/

### Relationship

Relationship include any information related to two users.
This might include. blocking, muting, marked as spam, notification pref, can pm, etc
