# -*- coding:utf-8 -*-

# maya
import pymel.core as pm


def add_cns_curve(parent, name, centers, degree=1):
    """Create a curve attached to given centers. One point per center
    Arguments:
        parent (dagNode): Parent object.
        name (str): Name
        centers (list of dagNode): Object that will drive the curve.
        degree (int): 1 for linear curve, 3 for Cubic.
    Returns:
        dagNode: The newly created curve.
    """
    # rebuild list to avoid input list modification
    centers = centers[:]
    if degree == 3:
        if len(centers) == 2:
            centers.insert(0, centers[0])
            centers.append(centers[-1])
        elif len(centers) == 3:
            centers.append(centers[-1])

    points = [pm.datatypes.Vector() for center in centers]

    node = add_curve(parent, name, points, False, degree)

    for index, center in enumerate(centers):
        mult = pm.createNode("multMatrix")
        decompose = pm.createNode("decomposeMatrix")
        center.worldMatrix >> mult.matrixIn[0]
        node.worldInverseMatrix >> mult.matrixIn[1]
        mult.matrixSum >> decompose.inputMatrix
        decompose.outputTranslate >> node.controlPoints[index]

    return node


def add_curve(parent,
              name,
              points,
              close=False,
              degree=3,
              m=pm.datatypes.Matrix()):
    """Create a NurbsCurve with a single subcurve.
    Arguments:
        parent (dagNode): Parent object.
        name (str): Name
        points (list of float): points of the curve in a one dimension array
            [point0X, point0Y, point0Z, 1, point1X, point1Y, point1Z, 1, ...].
        close (bool): True to close the curve.
        degree (bool): 1 for linear curve, 3 for Cubic.
        m (matrix): Global transform.
    Returns:
        dagNode: The newly created curve.
    """
    if close:
        points.extend(points[:degree])
        knots = range(len(points) + degree - 1)
        node = pm.curve(n=name, d=degree, p=points, per=close, k=knots)
    else:
        node = pm.curve(n=name, d=degree, p=points)

    if m is not None:
        node.setTransformation(m)

    if parent is not None:
        parent.addChild(node)

    return node


def get_color(node):
    """Get the color from shape node
    Args:
        node (TYPE): shape
    Returns:
        TYPE: Description
    """
    shp = node.getShape()
    if shp:
        if shp.overrideRGBColors.get():
            color = shp.overrideColorRGB.get()
        else:
            color = shp.overrideColor.get()

        return color


def set_color(node, color):
    """Set the color in the Icons.
    Arguments:
        node(dagNode): The object
        color (int or list of float): The color in index base or RGB.
    """
    if isinstance(color, int):
        for shp in node.listRelatives(shapes=True):
            shp.overrideEnabled.set(True)
            shp.overrideColor.set(color)
    else:
        for shp in node.listRelatives(shapes=True):
            shp.overrideEnabled.set(True)
            shp.overrideRGBColors.set(True)
            shp.overrideColorRGB.set(color[0], color[1], color[2])
