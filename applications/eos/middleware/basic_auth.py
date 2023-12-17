from applications.eos.common import auth


class BasicAuthMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            http_authorization = environ['HTTP_AUTHORIZATION']
            if not http_authorization:
                valid_auth = False
            else:
                valid_auth = auth.validate_basic_auth_token(http_authorization)
        except KeyError as ex:
            valid_auth = False

        if not valid_auth:
            status = '401'
            start_response(status, [("Content-Type", "application/json")])
            resp_body = """
            {
                "meta": {
                    "code": 401,
                    "message": "unauthorized"
                }
            }"""
            return [resp_body]

        items = self.app(environ, start_response)
        return items
