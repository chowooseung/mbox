# -*- coding: utf-8 -*-

# mbox
from mbox.rig.build import Instance
from . import Contributor


class Rig(Instance, Contributor):

    def __init__(self):
        super(Rig, self).__init__()

    def objects(self, context):
        super(Rig, self).objests(context)

    def features(self, context):
        super(Rig, self).features(context)

    def connector(self, context):
        super(Rig, self).connector(context)
