# -*- coding: utf-8 -*-

# mbox
from mbox import blueprint
from . import Contributor


class Guide(blueprint.Guide, Contributor):

    def __init__(self):
        # load schema
        super(Guide, self).__init__()

        # default settings...
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

    def draw(self):
        # new network, add common attribute
        super(Guide, self).draw()

        # specify attribute
        # ......

        # draw
        # guide = guide root
        # return guide
