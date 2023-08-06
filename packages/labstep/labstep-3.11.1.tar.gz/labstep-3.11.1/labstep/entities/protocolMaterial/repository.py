#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.protocolMaterial.model import ProtocolMaterial
import labstep.generic.entity.repository as entityRepository
from labstep.constants import UNSPECIFIED


def getProtocolMaterial(user, protocol_material_id):
    return entityRepository.getEntity(
        user, ProtocolMaterial, id=protocol_material_id
    )


def getProtocolMaterials(user, protocol_id, count=100, extraParams={}):
    params = {
        'protocol_id': protocol_id,
        **extraParams
    }
    return entityRepository.getEntities(user, ProtocolMaterial, count, params)


def newProtocolMaterial(user, protocol_id, name, resource_id=UNSPECIFIED, amount=UNSPECIFIED, units=UNSPECIFIED, extraParams={}):
    params = {
        "protocol_id": protocol_id,
        "name": name,
        "resource_id": resource_id,
        "value": amount,
        "units": units,
        **extraParams,
    }

    if params["value"] is not UNSPECIFIED:
        params["value"] = str(params["value"])

    return entityRepository.newEntity(user, ProtocolMaterial, params)


def editProtocolMaterial(protocol_material, name=UNSPECIFIED, amount=UNSPECIFIED, units=UNSPECIFIED, resource_id=UNSPECIFIED, extraParams={}):
    params = {
        "name": name,
        "value": amount,
        "units": units,
        "resource_id": resource_id,
        **extraParams
    }

    return entityRepository.editEntity(protocol_material, params)
