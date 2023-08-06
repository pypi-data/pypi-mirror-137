"""
add handler
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


add_v1 = Blueprint("add_v1", url_prefix="/add")


@dataclass
class AddFileNameV1PostParams:
    """
    AddFileNameV1PostParams
    """

    filename: str
    packages: List[str]


@dataclass
class AddFileNameV1PostResponse:
    """
    AddFileNameV1PostResponse
    """

    packages: List[str]


@add_v1.post("/", version=1)
@openapi.tag("Add")
@openapi.body({"application/json": AddFileNameV1PostParams}, required=True)
@openapi.response(
    200,
    {
        "application/json": AddFileNameV1PostResponse,
    },
    description="OK",
)
@openapi.response(400, {"application/json": {"error": str}}, description="Bad Request")
# pylint: disable=too-many-return-statements
@openapi.response(404, {"application/json": {"packages": []}}, description="Not Found")
@openapi.description("Add package name for filename.")
@validate(AddFileNameV1PostParams)
async def add_v1_post(request, body):
    """
    Add package name for filename.
    """
    try:
        app = Sanic.get_app("apthesaurus")
        with dbm.open(app.config.DBM_FILE, "c") as d_b:
            d_b[body.filename] = ujson.dumps(body.packages).encode("utf-8")
        return json({"packages": body.packages})
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
