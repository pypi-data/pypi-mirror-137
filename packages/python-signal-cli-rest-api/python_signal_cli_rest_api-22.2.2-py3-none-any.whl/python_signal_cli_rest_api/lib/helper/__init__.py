"""
helpers
"""

from base64 import b64decode
from binascii import Error as binascii_Error
from io import BytesIO
from mimetypes import guess_extension
from tempfile import mkstemp

from jmespath import search
from magic import from_buffer
from sanic.log import logger

from python_signal_cli_rest_api.lib.jsonrpc import jsonrpc


def is_groupid(recipient: str, version: int = 2):
    """
    try to decode base64. If succesful, recipient is a groupid
    """
    if version == 1:
        recipient = recipient.replace("_", "/")
    try:
        b64decode(recipient, validate=True)
        return True
    except binascii_Error:
        return False


def is_phone_number(recipients: list, number: str):
    """
    check if recipient is a valid phone number
    """
    if not isinstance(recipients, list):
        return None
    if isinstance(recipients[0], bytes):
        return None
    for recipient in recipients:
        if not (recipient.startswith("0") or recipient.startswith("+")):
            recipient = f"+{recipient}"
        if (
            not jsonrpc(
                {
                    "method": "getUserStatus",
                    "params": {
                        "account": number,
                        "recipient": recipient,
                    },
                }
            )
            .get("result", [{}])[0]
            .get("isRegistered", False)
        ):
            return None
    return recipients


def get_group_response(group: dict):
    """
    create reponse for group details
    """
    return {
        "blocked": group.get("isBlocked"),
        "id": group.get("id"),
        "invite_link": group.get("groupInviteLink"),
        "members": list(map(lambda d: d["number"], group.get("members"))),
        "name": group.get("name"),
        "pending_invites": group.get("pendingMembers"),
        "pending_requests": group.get("requestingMembers"),
        "message_expiration_timer": group.get("messageExpirationTimer"),
        "admins": list(map(lambda d: d["number"], group.get("admins"))),
        "description": group.get("description"),
    }


def get_groups(number: str, groupid: str = ""):
    """
    get groups
    """
    if not number:
        return (False, "Missing number")
    try:
        groups = jsonrpc(
            {
                "method": "listGroups",
                "params": {
                    "account": number,
                },
            }
        ).get("result", [])
        if groupid:
            match = search(f"[?id==`{groupid}`]", groups)
            if match:
                return (True, get_group_response(match[0]))
        result = []
        for group in groups:
            result.append(get_group_response(group))
        return (True, result)
    # pylint: disable=broad-except
    except Exception as err:
        return (False, err)


def do_decode_attachments(attachments, uuid):
    """
    decode base64 attachments and dump the decoded
    content to disk for sending out later
    """
    decoded_attachments = []
    for index, attachment in enumerate(attachments):
        try:
            attachment_io_bytes = BytesIO()
            attachment_io_bytes.write(b64decode(attachment))
            extension = guess_extension(
                from_buffer(attachment_io_bytes.getvalue(), mime=True)
            )
            _, filename = mkstemp(prefix=f"{uuid}_{index}_", suffix=f".{extension}")
            with open(filename, "wb") as f_h:
                f_h.write(b64decode(attachment))
            decoded_attachments.append(filename)
        # pylint: disable=broad-except
        except Exception as err:
            logger.error("unable to decode attachment: %s", err)
    return decoded_attachments
