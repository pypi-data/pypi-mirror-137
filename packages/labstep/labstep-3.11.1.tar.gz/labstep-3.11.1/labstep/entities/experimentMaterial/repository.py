#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.experimentMaterial.model import ExperimentMaterial
import labstep.generic.entity.repository as entityRepository
from labstep.constants import UNSPECIFIED


def getExperimentMaterial(user, experiment_material_id):
    return entityRepository.getEntity(
        user, ExperimentMaterial, id=experiment_material_id
    )


def getExperimentMaterials(user, experiment_id, count=100, extraParams={}):
    params = {
        'experiment_id': experiment_id,
        **extraParams
    }
    return entityRepository.getEntities(user, ExperimentMaterial, count, params)


def newExperimentMaterial(user, experiment_id, name, resource_id=UNSPECIFIED, resource_item_id=UNSPECIFIED, amount=UNSPECIFIED, units=UNSPECIFIED, extraParams={}):
    params = {
        "experiment_id": experiment_id,
        "name": name,
        "resource_id": resource_id,
        "resource_item_id": resource_item_id,
        "value": amount,
        "units": units,
        **extraParams,
    }

    if params["value"] is not UNSPECIFIED:
        params["value"] = str(params["value"])

    return entityRepository.newEntity(user, ExperimentMaterial, params)


def editExperimentMaterial(expermient_material, name=UNSPECIFIED, amount=UNSPECIFIED, units=UNSPECIFIED, resource_id=UNSPECIFIED, resource_item_id=UNSPECIFIED, extraParams={}):
    params = {
        "name": name,
        "value": amount,
        "units": units,
        "resource_id": resource_id,
        "resource_item_id": resource_item_id,
        **extraParams
    }

    return entityRepository.editEntity(expermient_material, params)
