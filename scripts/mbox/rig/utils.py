# -*- coding: utf-8 -*-

# maya
from pymel import core as pm


class Naming:

    def __init__(self):
        pass


class Selection:

    def __init__(self, node):
        self.node = pm.PyNode(node)
