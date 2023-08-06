"""
groups handler
"""

from dataclasses import dataclass, field
from enum import Enum
from os import remove as os_remove
from typing import Dict, List, Optional
from uuid import uuid4

from sanic import Blueprint, Sanic
from sanic.log import logger
from sanic.response import json, text
from sanic_ext import openapi, validate

from python_signal_cli_rest_api.dataclasses import Error, GroupId
from python_signal_cli_rest_api.lib.helper import do_decode_attachments, get_groups
from python_signal_cli_rest_api.lib.jsonrpc import jsonrpc

create_group_v1 = Blueprint("create_group_v1", url_prefix="/groups")
delete_group_v1 = Blueprint("delete_group_v1", url_prefix="/groups")
groups_for_number_v1 = Blueprint("groups_of_number_v1", url_prefix="/groups")
group_details_v1 = Blueprint("group_details_v1", url_prefix="/groups")
join_group_v1 = Blueprint("join_group_v1", url_prefix="/groups")
quit_group_v1 = Blueprint("quit_group_v1", url_prefix="/groups")
update_group_v1 = Blueprint("update_group_v1", url_prefix="/groups")


@dataclass
class GroupsForNumberGetV1Params:
    """
    GroupsForNumberGetV1Params
    """

    number: str


@dataclass
class GroupsForNumberGetV1ResponseItem:  # pylint: disable=too-many-instance-attributes
    """
    GroupsForNumberGetV1ResponseItem
    """

    blocked: bool
    id: str  # pylint: disable=invalid-name
    invite_link: str
    members: List[str]
    name: str
    pending_invites: List[str]
    pending_requests: List[str]
    message_expiration_timer: int
    admins: List[str]
    description: str


@groups_for_number_v1.get("/<number:path>", version=1)
@openapi.tag("Groups")
@openapi.parameter(
    "number",
    str,
    required=True,
    location="path",
    description="Registered Phone Number",
)
@openapi.response(
    200,
    {"application/json": List[GroupsForNumberGetV1ResponseItem]},
    description="OK",
)
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("List all Signal Groups.")
async def groups_for_number_get(request, number):  # pylint: disable=unused-argument
    """
    List all Signal Groups.
    """
    try:
        success, data = get_groups(number)
        if not success:
            return json({"error": data}, 400)
        return json(data, 200)
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)


@group_details_v1.get("/<number:path>/<groupid:path>", version=1)
@openapi.tag("Groups")
@openapi.parameter(
    "number",
    str,
    required=True,
    location="path",
    description="Registered Phone Number",
)
@openapi.parameter(
    "groupid",
    str,
    required=True,
    location="path",
    description="Group ID",
)
@openapi.response(
    200,
    {"application/json": GroupsForNumberGetV1ResponseItem},
    description="OK",
)
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("List a Signal Group.")
async def groups_of_number_get(
    request, number: str, groupid: str
):  # pylint: disable=unused-argument
    """
    List a Signal Group.
    """
    try:
        success, data = get_groups(
            number=number,
            groupid=groupid,
        )
        if not success:
            return json({"error": data}, 400)
        return json(data, 200)
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)


@dataclass
class CreateGroupV1Permissions:
    """
    CreateGroupV1Permissions
    """

    add_members: str = "only-admins"
    edit_group: str = "only-admins"


@dataclass
class GroupLinkV1Choices(Enum):
    """
    GroupLinkV1Choices
    """

    DISABLED = "disabled"
    ENABLED = "enabled"
    ENABLED_WITH_APPROVAL = "enabled-with-approval"


@dataclass
class CreateGroupV1PostParamsDocs:  # pylint: disable=too-many-instance-attributes
    """
    CreateGroupV1PostParams
    """

    name: str
    members: List[str]
    permissions: Optional[CreateGroupV1Permissions]
    group_link: Optional[GroupLinkV1Choices]
    admins: Optional[List[str]] = field(default_factory=list)
    description: Optional[str] = field(default_factory=str)
    base64_avatar: Optional[str] = field(default_factory=str)
    message_expiration_timer: Optional[int] = 0


@dataclass
class CreateGroupV1PostParamsValidate(CreateGroupV1PostParamsDocs):
    """
    CreateGroupV1PostParamsValidate
    """

    group_link: str = "disabled"
    permissions: Optional[Dict[str, CreateGroupV1Permissions]] = field(
        default_factory=dict
    )

    def __post_init__(self):
        if isinstance(self.permissions, dict):
            self.permissions = CreateGroupV1Permissions(**self.permissions)


@create_group_v1.post("/<number:path>", version=1)
@openapi.tag("Groups")
@openapi.parameter("number", str, required=True, location="path")
@openapi.body({"application/json": CreateGroupV1PostParamsDocs}, required=True)
@openapi.response(201, {"application/json": GroupId}, description="Created")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Create a new Signal Group.")
@validate(CreateGroupV1PostParamsValidate)
async def create_group_v1_post(
    request, number, body: CreateGroupV1PostParamsValidate
):  # pylint: disable=unused-argument
    """
    Create a new Signal Group with the specified members.
    """
    avatar = ""
    app = Sanic.get_app()
    try:
        number = number or app.config.ACCOUNT
    except AttributeError:
        return json(
            {"error": "number missing in request and PYTHON_SIGNAL_CLI_REST_API_ unset "},
            400,
        )
    uuid = str(uuid4())
    try:
        avatar = do_decode_attachments([body.base64_avatar], uuid)[0]
    # pylint: disable=broad-except
    except IndexError:
        pass
    try:
        params = {
            "account": number,
            "member": body.members,
            "admin": body.admins,
            "name": body.name,
            "description": body.description,
            "expiration": body.message_expiration_timer,
            "setPermissionAddMember": body.permissions.add_members,
            "setPermissionEditDetails": body.permissions.edit_group,
        }
        if avatar:
            params.update({"avatar": avatar})
        if body.group_link:
            params.update({"link": body.group_link})
        result = jsonrpc({"method": "updateGroup", "params": params}).get("result")
        groupid = result.get("groupId")
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
    finally:
        os_remove(avatar)
    return json({"id": groupid}, 201)


@delete_group_v1.delete("/<number:path>/<groupid:path>", version=1)
@openapi.tag("Groups")
@openapi.parameter("number", str, required=True, location="path")
@openapi.parameter("groupid", str, required=True, location="path")
@openapi.response(204, None, description="Deleted")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Delete a Signal Group.")
async def delete_group_v1_delete(
    request, number: str, groupid: str
):  # pylint: disable=unused-argument
    """
    Delete the specified Signal Group.
    """
    try:
        params = {
            "account": number,
            "groupId": groupid,
            "delete": True,
        }
        jsonrpc({"method": "quitGroup", "params": params})
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
    return text("", 204)


@dataclass
class UpdateGroupLinkV1Choices(Enum):
    """
    UpdateGroupLinkV1Choices
    """

    UNCHANGED = "unchanged"
    DISABLED = "disabled"
    ENABLED = "enabled"
    ENABLED_WITH_APPROVAL = "enabled-with-approval"


@dataclass
class UpdateGroupV1PatchParamsDocs:
    """
    UpdateGroupV1PatchParamsDocs
    """

    group_link: Optional[UpdateGroupLinkV1Choices]
    add_admins: Optional[List[str]] = field(default_factory=list)
    add_members: Optional[List[str]] = field(default_factory=list)


@dataclass
class UpdateGroupV1PatchParamsValidate(UpdateGroupV1PatchParamsDocs):
    """
    UpdateGroupV1PatchParamsValidate
    """

    group_link: str = "unchanged"


@update_group_v1.patch("/<number:path>/<groupid:path>", version=1)
@openapi.tag("Groups")
@openapi.parameter("number", str, required=True, location="path")
@openapi.parameter("groupid", str, required=True, location="path")
@openapi.body({"application/json": UpdateGroupV1PatchParamsDocs})
@openapi.response(
    200,
    {"application/json": GroupsForNumberGetV1ResponseItem},
    description="OK",
)
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Update an existing Signal Group.")
@validate(UpdateGroupV1PatchParamsValidate)
async def update_group_v1_patch(
    request, number: str, groupid: str, body: UpdateGroupV1PatchParamsValidate
):  # pylint: disable=unused-argument
    """
    Update an existing Signal Group.
    """
    try:
        params = {
            "account": number,
            "member": body.add_members,
            "admin": body.add_admins,
            "name": body.name,
            "description": body.description,
            "expiration": body.message_expiration_timer,
            "setPermissionAddMember": body.permissions.add_members,
            "setPermissionEditDetails": body.permissions.edit_group,
        }
        if body.group_link != UpdateGroupLinkV1Choices.UNCHANGED:
            params.update({"link": body.group_link})
        jsonrpc({"method": "updateGroup", "params": params})
        success, data = get_groups(
            number=number,
            groupid=groupid,
        )
        if not success:
            return json({"error": data}, 400)
        return json(data, 200)
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
    return json(data, 200)


@quit_group_v1.post("/<number:path>/<groupid:path>/quit", version=1)
@openapi.tag("Groups")
@openapi.parameter("number", str, required=True, location="path")
@openapi.parameter("groupid", str, required=True, location="path")
@openapi.response(204, description="OK")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Quit (leave) a Signal Group.")
async def quit_group_v1_post(
    request, number: str, groupid: str
):  # pylint: disable=unused-argument
    """
    Quit (leave) a Signal Group.
    """
    try:
        params = {
            "account": number,
            "groupId": groupid,
        }
        jsonrpc({"method": "quitGroup", "params": params})
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
    return text("", 204)


@join_group_v1.post("/<number:path>/<groupid:path>/join", version=1)
@openapi.tag("Groups")
@openapi.parameter("number", str, required=True, location="path")
@openapi.parameter(
    "groupid",
    str,
    required=True,
    location="path",
    description="Group invite link like https://signal.group/#...",
)
@openapi.response(204, description="OK")
@openapi.response(400, {"application/json": Error}, description="Bad Request")
@openapi.description("Join a Signal Group.")
async def join_group_v1_post(
    request, number: str, groupid: str
):  # pylint: disable=unused-argument
    """
    Join a Signal Group.
    """
    try:
        params = {
            "account": number,
            "uri": groupid,
        }
        jsonrpc({"method": "joinGroup", "params": params})
    # pylint: disable=broad-except
    except Exception as err:
        error = getattr(err, "message", repr(err))
        logger.error(error)
        return json({"error": error}, 400)
    return text("", 204)
