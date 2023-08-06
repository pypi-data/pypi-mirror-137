"""
api blueprints group
"""


from sanic import Blueprint

from apthesaurus.api.search import search_v1
from apthesaurus.api.add import add_v1

entrypoint = Blueprint.group(
    add_v1,
    search_v1,
    url_prefix="/",
)
