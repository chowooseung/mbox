# -*- coding:utf-8 -*-

# mgear
from mgear.core.curve import *


def add_cns_curve(parent, name, centers, degree=1):
    """edit mgear.core.curve.addCnsCurve"""
    # rebuild list to avoid input list modification
    centers = centers[:]
    if degree == 3:
        if len(centers) == 2:
            centers.insert(0, centers[0])
            centers.append(centers[-1])
        elif len(centers) == 3:
            centers.append(centers[-1])

    points = [pm.datatypes.Vector() for center in centers]

    node = addCurve(parent, name, points, False, degree)

    for index, center in enumerate(centers):
        mult = pm.createNode("multMatrix")
        decompose = pm.createNode("decomposeMatrix")
        pm.connectAttr(center.attr("worldMatrix")[0], mult.attr("matrixIn")[0])
        pm.connectAttr(node.attr("worldInverseMatrix")[0], mult.attr("matrixIn")[1])
        pm.connectAttr(mult.attr("matrixSum"), decompose.attr("inputMatrix"))
        pm.connectAttr(decompose.attr("outputTranslate"), node.attr("controlPoints")[index])
    node.attr("overrideEnabled").set(1)
    node.attr("overrideDisplayType").set(1)
    return node
