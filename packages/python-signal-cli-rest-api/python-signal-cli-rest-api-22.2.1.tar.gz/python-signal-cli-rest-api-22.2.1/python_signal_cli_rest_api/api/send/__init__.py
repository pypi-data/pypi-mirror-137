"""
send messages to single contact or group
"""


from dataclasses import dataclass, field
from os import remove as os_remove
from typing import List, Optional
from uuid import uuid4

from sanic import Blueprint, Sanic
from sanic.log import logger
from sanic.response import json
from sanic_ext import openapi, validate

from python_signal_cli_rest_api.dataclasses import Error, ResponseTimestamp
from python_signal_cli_rest_api.lib.helper import (
    do_decode_attachments,
    is_groupid,
    is_phone_number,
)
from python_signal_cli_rest_api.lib.jsonrpc import jsonrpc

send_v1 = Blueprint("send_v1", url_prefix="/send")
send_v2 = Blueprint("send_v2", url_prefix="/send")


def do_send_message(
    recipients: list, number: str, message: str, version: int = 2, **kwargs
):
    """
    send message
    """
    try:
        params = {
            "account": number,
            "message": message,
        }
        is_group = is_groupid(recipient=recipients[0], version=version)
        if is_group:
            params.update({"groupId": recipients[0]})
        elif is_phone_number(recipients=recipients, number=number):
            params.update({"recipient": recipients})
        else:
            return (
                {
                    "error": f"{recipients} is neither a phone number nor a valid group id"
                },
                400,
            )
        if kwargs.get("attachments"):
            params.update({"attachment": kwargs.get("attachments")})
        if kwargs.get("mentions"):
            params.update({"mention": kwargs.get("mentions")})
        res = jsonrpc({"method": "send", "params": params})
        timestamp = res.get("result").get("timestamp")
        if not timestamp:
            return {"error": res}, 400
        return {"timestamp": str(timestamp)}, 201
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return {"error": error}, 400
    finally:
        for attachment in kwargs.get("attachments", []):
            os_remove(attachment)


@dataclass
class SendV2PostParams:
    """
    SendV2PostParams
    """

    recipients: List[str]
    message: str
    number: Optional[str] = field(default_factory=str)
    base64_attachments: Optional[List[str]] = field(default_factory=list)
    mentions: Optional[List[str]] = field(default_factory=list)


@send_v2.post("/", version=2)
@openapi.tag("Messages")
@openapi.body({"application/json": SendV2PostParams}, required=True)
@openapi.response(201, {"application/json": ResponseTimestamp}, description="Created")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description(
    (
        "Send a signal message."
        "`number` can be ommited if API is running w/ `PYTHON_SIGNAL_CLI_REST_API_ACCOUNT`"
    )
)
@validate(SendV2PostParams)
async def send_v2_post(
    request, body: SendV2PostParams
):  # pylint: disable=unused-argument
    """
    Send a signal message.
    """
    decoded_attachments = []
    app = Sanic.get_app("python-signal-cli-rest-api")
    recipients = body.recipients
    try:
        number = body.number or app.config.ACCOUNT
    except AttributeError:
        return json(
            {"error": "number missing in request and PYTHON_SIGNAL_CLI_REST_API_ unset "},
            400,
        )
    attachments = body.base64_attachments
    uuid = str(uuid4())
    if isinstance(attachments, list):
        decoded_attachments = do_decode_attachments(attachments, uuid)
    return_message, return_code = do_send_message(
        recipients=recipients,
        number=number,
        message=body.message,
        attachments=decoded_attachments,
        mentions=body.mentions,
    )
    return json(return_message, return_code)


@dataclass
class SendV1PostParams:
    """
    SendV1PostParams
    """

    message: str
    number: Optional[str] = field(default_factory=str)
    base64_attachments: List[str] = field(default_factory=list)


@send_v1.post("/<recipient:path>", version=1)
@openapi.tag("Messages")
@openapi.parameter("recipient", str, required=True, location="path")
@openapi.body({"application/json": SendV1PostParams}, required=True)
@openapi.response(201, {"application/json": ResponseTimestamp}, description="Created")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description(
    (
        "Send a signal message."
        "`number` can be ommited if API is running w/ `PYTHON_SIGNAL_CLI_REST_API_`"
    )
)
@validate(SendV1PostParams)
async def send_v1_post(
    request, recipient, body: SendV1PostParams
):  # pylint: disable=unused-argument
    """
    Send a signal message.
    """
    decoded_attachments = []
    app = Sanic.get_app("python-signal-cli-rest-api")
    try:
        number = body.number or app.config.ACCOUNT
    except AttributeError:
        return json(
            {"error": "number missing in request and PYTHON_SIGNAL_CLI_REST_API_ unset "},
            400,
        )
    attachments = body.base64_attachments
    uuid = str(uuid4())
    if isinstance(attachments, list):
        decoded_attachments = do_decode_attachments(attachments, uuid)
    return_message, return_code = do_send_message(
        recipients=[recipient],
        number=number,
        message=body.message,
        attachments=decoded_attachments,
        version=1,
    )
    return json(return_message, return_code)
