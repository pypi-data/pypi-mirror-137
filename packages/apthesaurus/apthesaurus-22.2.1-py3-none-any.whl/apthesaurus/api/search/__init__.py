"""
search handler
"""

from sanic import Blueprint

import dbm
import ujson
from dataclasses import dataclass
from typing import List

from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic_ext import openapi, validate


search_v1 = Blueprint("search_v1", url_prefix="/search")


@dataclass
class SearchFileNameV1PostParams:
    """
    SearchFileNameV1PostParams
    """

    filename: str


@dataclass
class SearchFileNameV1PostResponse:
    """
    SearchFileNameV1PostResponse
    """

    packages: List[str]


@search_v1.post("/", version=1)
@openapi.tag("Search")
@openapi.body({"application/json": SearchFileNameV1PostParams}, required=True)
@openapi.response(
    200,
    {
        "application/json": SearchFileNameV1PostResponse,
    },
    description="OK",
)
@openapi.response(400, {"application/json": {"error": str}}, description="Bad Request")
# pylint: disable=too-many-return-statements
@openapi.response(404, {"application/json": {"package": None}}, description="Not Found")
@openapi.description("Search package name which includes filename")
@validate(SearchFileNameV1PostParams)
async def search_v1_get(
    request, body: SearchFileNameV1PostParams
):  # pylint: disable=unused-argument
    """
    Search package name which includes filename
    """
    try:
        app = Sanic.get_app("apthesaurus")
        with dbm.open(app.config.DBM_FILE, "c") as d_b:
            result = d_b.get(body.filename)
            if result:
                result = result.decode("utf-8")
        if not result:
            return json({"error": "not found"}, 404)
        return json({"packages": ujson.loads(result)})
    # pylint: disable=broad-except
    except Exception as err:
        logger.error(err)
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
