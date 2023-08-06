"""
apthesaurus - find package names for filenames
"""


from sanic import Sanic

from apthesaurus.api import entrypoint
from apthesaurus.version import __version__

app = Sanic("apthesaurus", env_prefix="APTHESAURUS_")
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.OAS_UI_DEFAULT = "swagger"
app.config.OAS_UI_REDOC = False
app.config.API_HOST = (
    f'{app.config.get("API_HOST", "127.0.0.1")}:{app.config.get("API_PORT", 8080)}'
)
app.config.API_BASEPATH = app.config.get("API_BASEPATH")
app.config.API_SCHEMES = app.config.get("API_SCHEMES", "http,https").split(",")
app.config.API_LICENSE_NAME = "MIT"
app.config.API_LICENSE_URL = "https://mit-license.org/"
app.config.API_TITLE = "apthesaurus"
app.config.API_DESCRIPTION = "This is the apthesaurus documentation."
app.config.API_VERSION = __version__
if "DBM_FILE" not in app.config:
    app.config.DBM_FILE = "/dev/shm/apt-filenames.db"
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
