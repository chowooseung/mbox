# -*- coding: utf-8 -*-

# maya
from pymel import core as pm


def get_uuid(node):
    if not node:
        node = pm.selected()[0] if pm.selected() else None
    if node:
        return pm.mel.ls(node, uuid=True)[0]


def set_uuid(uid, target=None):
    if target:
        if isinstance(target, str):
            target = pm.PyNode(target)
    else:
        target = pm.selected()
        if target:
            target = target[0]
    if not target:
        return
    old = pm.mel.ls(target, uuid=True)
    if old != uid:
        target.rename(uid, uuid=True)


def find(uid):
    return pm.ls(uid, uuid=True)[0] if pm.ls(uid, uuid=True) else None
