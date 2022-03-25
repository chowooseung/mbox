# -*- coding: utf-8 -*-

# mbox
from mbox.rig import build
from . import Contributor


class Rig(build.Instance, Contributor):

    def __init__(self, context, component):
        super(Rig, self).__init__(context=context, component=component)

    def objects(self):
        """ rig object create """

    def features(self):
        """ rig feature create """

    def connector(self):
        """ specify parent component connector """

