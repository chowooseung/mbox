# -*- coding: utf-8 -*-

# mbox
from mbox.box import blueprint
from . import Contributor

# mgear
from mgear.core import attribute, primitive

# maya
from pymel import core as pm


class Guide(blueprint.Component, Contributor):

    def __init__(self, network=None, parent=None, data=None, chain_number=0):
        # if chain self["guide_transforms"] = "#"

        # load schema
        super(Guide, self).__init__(network=network, parent=parent, data=data, chain_number=chain_number)

        # specify attribute setup
        # ......

    def pull(self):
        # if no network
        if not self.network:
            return

        # common attribute pull
        super(Guide, self).pull()

        # specify attribute pull
        # ......

    def push(self):
        # if no network
        if not self.network:
            return

        # common attribute push
        super(Guide, self).push()

        # specify attribute push
        # ......

    def draw_network(self):
        # new network, add common attribute
        super(Guide, self).draw_network()

        # specify attribute create
        # ......

    def draw_guide(self):
        # If self._network is None, add network
        super(Guide, self).draw_guide()

        # draw guide
        # guide = self.add_root(...)
        # ...
        # return guide
