# -*- coding: utf-8 -*-

# mbox
from mbox.rig import blueprint
from . import Contributor


class Guide(blueprint.Component, Contributor):

    def __init__(self):
        # load schema
        super(Guide, self).__init__()

        # specify attribute setup
        # ......

    def pull(self):
        # common attribute pull
        super(Guide, self).pull()

        # specify attribute pull
        # ......

    def push(self):
        # common attribute push
        super(Guide, self).push()

        # specify attribute push
        # ......

    def draw_network(self):
        # new network, add common attribute
        super(Guide, self).draw_network()

        # specify attribute create
        # ......

        # draw network
        # n = pm.createNode("network")
        # ...
        # self._network = n

    def draw_guide(self):
        # If self._network is None, add network
        super(Guide, self).draw_guide()

        # draw guide
        # guide = self.add_root(...)
        # ...
        # return guide
