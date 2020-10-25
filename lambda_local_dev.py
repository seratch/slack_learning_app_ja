import os

from slack_bolt import BoltRequest
from slack_bolt.app import App
from slack_bolt.oauth import OAuthFlow
from slack_bolt.response import BoltResponse


def run(app: App):
    @app.use
    def print_request(request: BoltRequest, next, logger):
        logger.info(f"Request body: {request.body}")
        next()

    from flask import Request, Response, make_response
    from slack_bolt.adapter.flask.handler import to_flask_response, to_bolt_request

    class LocalFlaskAppHandler:
        def __init__(self, app: App):  # type: ignore
            self.app = app

        def handle(self, req: Request) -> Response:
            if req.method == "GET":
                if self.app.oauth_flow is not None:
                    oauth_flow: OAuthFlow = self.app.oauth_flow
                    if "code" in req.args or "error" in req.args:
                        bolt_resp = oauth_flow.handle_callback(to_bolt_request(req))
                        return to_flask_response(bolt_resp)
                    else:
                        bolt_resp = oauth_flow.handle_installation(to_bolt_request(req))
                        return to_flask_response(bolt_resp)
            elif req.method == "POST":
                bolt_resp: BoltResponse = self.app.dispatch(to_bolt_request(req))
                return to_flask_response(bolt_resp)

            return make_response("Not Found", 404)

    from flask import Flask, request

    flask_app = Flask(__name__)
    handler = LocalFlaskAppHandler(app)

    path = os.environ["SLACK_LAMBDA_PATH"]

    @flask_app.route(path, methods=["GET", "POST"])
    def slack_events():
        return handler.handle(request)

    flask_app.run(port=3000, debug=True)
