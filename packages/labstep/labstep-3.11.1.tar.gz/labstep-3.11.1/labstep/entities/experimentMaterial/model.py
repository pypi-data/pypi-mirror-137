#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.generic.entity.model import Entity
from labstep.constants import UNSPECIFIED


class ExperimentMaterial(Entity):
    __entityName__ = "experiment-value"

    def __init__(self, data, user):
        super().__init__(data, user)
        self.amount = self.value

    def edit(self, name=UNSPECIFIED, amount=UNSPECIFIED, units=UNSPECIFIED, resource_id=UNSPECIFIED, resource_item_id=UNSPECIFIED, extraParams={}):
        """
        Edit an existing Experiment Material.

        Parameters
        ----------
        amount (str)
            The amount of the Experiment Material.
        units (str)
            The units of the amount.
        resource_id (int)
            The :class:`~labstep.entities.resource.model.Resource` of the Experiment Material.
        resource_item_id (int)
            The id of the :class:`~labstep.entities.resource.model.ResourceItem`
            of the Experiment Material.

        Returns
        -------
        :class:`~labstep.entities.experimentMaterial.model.ExperimentMaterial`
            An object representing the edited Experiment Material.

        Example
        -------
        ::

            experiment = user.getExperiment(17000)
            exp_protocol = experiment.getProtocols()[0]
            exp_protocol_materials = exp_protocol.getMaterials()
            exp_protocol_materials[0].edit(amount=1.7, units='ml')
        """
        import labstep.entities.experimentMaterial.repository as experimentMaterialRepository

        return experimentMaterialRepository.editExperimentMaterial(self,
                                                                   name=name,
                                                                   amount=amount,
                                                                   units=units,
                                                                   resource_id=resource_id,
                                                                   resource_item_id=resource_item_id,
                                                                   extraParams=extraParams)
