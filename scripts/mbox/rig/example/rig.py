# -*- coding: utf-8 -*-

# mbox
from mbox.rig import build
from . import Contributor

# mgear
from mgear.core import attribute, primitive

# maya
from pymel import core as pm


class Rig(build.Instance, Contributor):

    def objects(self):
        """ rig object create """

    def attributes(self):
        """ rig attributes create """

    def operators(self):
        """ rig operators create """

    def connector(self):
        """ specify parent component connector """

