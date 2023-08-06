#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

import json
from labstep.service.helpers import url_join, getHeaders
from labstep.service.config import configService
from labstep.service.request import requestService
from labstep.entities.permission.model import Permission
from labstep.generic.entityList.model import EntityList


def newPermission(entity, workspace_id, permission):
    entityName = entity.__entityName__

    headers = getHeaders(entity.__user__)
    url = url_join(configService.getHost(), "api/generic/", "acl")

    params = {
        "id": entity.id,
        "entity_class": entityName.replace("-", "_"),
        "action": "grant",
        "group_id": workspace_id,
        "permission": permission,
    }
    requestService.post(url, headers=headers, json=params)
    return entity


def editPermission(entity, workspace_id, permission):
    entityName = entity.__entityName__

    headers = getHeaders(entity.__user__)
    url = url_join(configService.getHost(), "api/generic/", "acl")

    params = {
        "id": entity.id,
        "entity_class": entityName.replace("-", "_"),
        "action": "set",
        "group_id": workspace_id,
        "group_owner_id": workspace_id,
        "permission": permission,
    }
    requestService.post(url, headers=headers, json=params)
    return entity


def revokePermission(entity, workspace_id):
    entityName = entity.__entityName__

    headers = getHeaders(entity.__user__)
    url = url_join(configService.getHost(), "api/generic/", "acl")

    params = {
        "id": entity.id,
        "entity_class": entityName.replace("-", "_"),
        "action": "revoke",
        "group_id": workspace_id,
    }
    requestService.post(url, headers=headers, json=params)
    return entity


def getPermissions(entity):
    entityName = entity.__entityName__
    headers = getHeaders(entity.__user__)
    url = url_join(
        configService.getHost(),
        "api/generic/",
        "acl",
        entityName.replace("-", "_"),
        str(entity.id),
    )
    response = requestService.get(url, headers=headers)
    resp = json.loads(response.content)
    return EntityList(resp["group_permissions"], Permission, entity)


def transferOwnership(entity, workspace_id):
    entityName = entity.__entityName__
    headers = getHeaders(entity.__user__)
    url = url_join(
        configService.getHost(), "api/generic/", entityName, str(entity.id), "transfer-ownership"
    )
    params = {"group_id": workspace_id}
    requestService.post(url, headers=headers, json=params)
