"""
REST Wrapper for signal-cli running w/ JSON RPC
"""


import os
from sanic import Sanic

from python_signal_cli_rest_api.api import entrypoint
from python_signal_cli_rest_api.version import __version__

dirname = os.path.dirname(os.path.realpath(__file__))
app = Sanic("python-signal-cli-rest-api", env_prefix="PYTHON_SIGNAL_CLI_REST_API_")
app.static(
    "/openapi/assets/swagger",
    f"{dirname}/openapi/assets/swagger",
    name="swagger-assets",
)
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.OAS_UI_DEFAULT = "swagger"
app.config.OAS_UI_REDOC = False
app.config.OAS_PATH_TO_SWAGGER_HTML = f"{dirname}/openapi/assets/swagger/swagger.html"
app.config.API_HOST = (
    f'{app.config.get("API_HOST", "127.0.0.1")}:{app.config.get("API_PORT", 8080)}'
)
app.config.API_BASEPATH = app.config.get("API_BASEPATH")
app.config.API_SCHEMES = app.config.get("API_SCHEMES", "http,https").split(",")
app.config.API_LICENSE_NAME = "MIT"
app.config.API_LICENSE_URL = "https://mit-license.org/"
app.config.API_TITLE = "Signal Cli REST API"
app.config.API_DESCRIPTION = "This is the Signal Cli REST API documentation."
app.config.API_VERSION = __version__
if "ACCOUNT" in app.config.keys():
    if not str(app.config.ACCOUNT).startswith("+"):
        app.config.ACCOUNT = f"+{app.config.ACCOUNT}"
app.blueprint(entrypoint)


def run():
    """
    run app
    """
    app.run(
        host=app.config.get("HOST", "127.0.0.1"),
        port=app.config.get("PORT", 8080),
        debug=app.config.get("DEBUG", False),
        workers=app.config.get("WORKERS", 1),
        access_log=app.config.get("ACCESS_LOG", False),
        auto_reload=app.config.get("AUTO_RELOAD", False),
    )
