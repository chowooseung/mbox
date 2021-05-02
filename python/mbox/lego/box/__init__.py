# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.core import transform


def blueprint(info, context):
    root, shapes, blocks, joints = [pm.group(name=x, empty=True) for x in
                                    ["blueprint", "shapes", "blocks", "joints"]]

    root, shapes, blocks, joints
