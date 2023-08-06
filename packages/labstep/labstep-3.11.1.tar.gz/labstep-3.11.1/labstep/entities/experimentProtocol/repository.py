#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

import labstep.generic.entity.repository as entityRepository


def exportExperimentProtocol(experimentProtocol, rootPath, folderName):

    experimentProtocol.update()

    expDir = entityRepository.exportEntity(
        experimentProtocol, rootPath, folderName=folderName)

    # save materials
    materialsDir = expDir.joinpath('materials')
    materials = experimentProtocol.getMaterials()

    for material in materials:
        material.export(materialsDir)

    # save data
    dataDir = expDir.joinpath('data')
    data = experimentProtocol.getDataFields()

    for dat in data:
        dat.export(dataDir)
