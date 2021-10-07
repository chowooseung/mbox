# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mgear
from mgear.core.curve import addCurve


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
        center.worldMatrix >> mult.matrixIn[0]
        node.worldInverseMatrix >> mult.matrixIn[1]
        mult.matrixSum >> decompose.inputMatrix
        decompose.outputTranslate >> node.controlPoints[index]

    return node