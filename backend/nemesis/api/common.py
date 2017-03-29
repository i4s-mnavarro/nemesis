# -*- coding: utf-8 -*-

import json

from slackclient import SlackClient
from bottle import request, abort, response, hook, route

from nemesis.common import constants
from nemesis.common.config import options


@hook('after_request')
def set_response():

    response.content_type = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, \
                                                        Content-Type, X-Requested-With, X-CSRF-Token'


def authorize(request):
    def check_token(api_func):
        def wrapper(**kwds):
            auth_token = request.headers.get('Authorization')
            if auth_token is not None:
                res = SlackClient(auth_token).api_call("users.identity", scope=constants.OAUTH_SCOPE)
                if res['ok'] is False:
                    abort(401, "Not authorized")
                return api_func(**kwds)
            else:
                abort(401, "Not authorized")
        return wrapper
    return check_token


@route('/', method='OPTIONS')
@route('/<path:path>', method='OPTIONS')
def options_handler(path=None):
    return


@route("/auth-token/", method='GET')
def auth_token():

    auth_code = request.query.code

    slack_client = SlackClient("")
    auth_response = slack_client.api_call(
        "oauth.access",
        client_id=options.slack_client_id,
        client_secret=options.slack_client_secret,
        code=auth_code
    )

    return json.dumps(auth_response)
