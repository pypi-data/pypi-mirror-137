"""
send message reactions to single contact
"""


from dataclasses import dataclass, field
from typing import Optional

from sanic import Blueprint
from sanic.log import logger
from sanic.response import json
from sanic_ext import openapi, validate

from python_signal_cli_rest_api.dataclasses import Error, ResponseTimestamp
from python_signal_cli_rest_api.lib.jsonrpc import jsonrpc

reactions_v1 = Blueprint("reactions_v1", url_prefix="/reactions")


def send_reaction(
    number: str,
    reaction: str,
    remove: bool,
    recipient: str,
    target_author: str,
    timestamp: int,
    groupid: str = "",
):  # pylint: disable=too-many-arguments
    """
    send reaction
    """
    try:
        params = {
            "account": number,
            "emoji": reaction,
            "remove": remove,
            "targetAuthor": target_author,
            "targetTimestamp": timestamp,
            "recipient": recipient,
        }
        if groupid:
            params.update({"groupId": groupid})
        logger.info(params)
        result = jsonrpc({"method": "sendReaction", "params": params}).get("result", {})
        timestamp = result.get("timestamp")
        return {"timestamp": timestamp}, 200
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return {"error": error}, 400


@dataclass
class ReactionsV1PostParams:
    """
    ReactionsV1PostParams
    """

    reaction: str
    target_author: str
    timestamp: int
    recipient: str
    groupid: Optional[str] = field(default_factory=str)
    remove: Optional[bool] = False


@reactions_v1.post("/<number:path>", version=1)
@openapi.tag("Reactions")
@openapi.parameter("number", str, required=True, location="path")
@openapi.body({"application/json": ReactionsV1PostParams}, required=True)
@openapi.response(201, {"application/json": ResponseTimestamp}, description="Created")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Send a reaction.")
@validate(json=ReactionsV1PostParams)
async def reactions_v1_post(
    request, number, body: ReactionsV1PostParams
):  # pylint: disable=unused-argument
    """
    Send a reaction.
    """
    return_message, return_code = send_reaction(
        number=number,
        reaction=body.reaction,
        remove=body.remove,
        target_author=body.target_author,
        timestamp=body.timestamp,
        recipient=body.recipient,
        groupid=body.groupid,
    )
    return json(return_message, return_code)


@dataclass
class ReactionsV1DeleteParams:
    """
    ReactionsV1DeleteParams
    """

    recipient: str
    target_author: str
    timestamp: int


@reactions_v1.delete("/<number:path>", ignore_body=False, version=1)
@openapi.tag("Reactions")
@openapi.parameter("number", str, required=True, location="path")
@openapi.body({"application/json": ReactionsV1DeleteParams}, required=True)
@openapi.response(200, {"application/json": ResponseTimestamp}, description="Deleted")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Delete a reaction.")
@validate(ReactionsV1DeleteParams)
async def reactions_v1_delete(
    request, number, body: ReactionsV1DeleteParams
):  # pylint: disable=unused-argument
    """
    Delete a reaction.
    """
    return_message, return_code = send_reaction(
        number=number,
        reaction="👍",
        remove=True,
        target_author=body.target_author,
        timestamp=body.timestamp,
        recipient=body.recipient,
    )
    return json(return_message, return_code)
