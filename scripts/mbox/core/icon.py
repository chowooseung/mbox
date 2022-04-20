# -*- coding:utf-8 -*-

# maya
import maya.api.OpenMaya as om

# mgear
from mgear.core.icon import *
from . import attribute, curve


def guideRootIcon(parent=None,
                    name="root",
                    width=.5,
                    color=[1, 0, 0],
                    m=datatypes.Matrix(),
                    pos_offset=None,
                    rot_offset=None):
    """from mgear.core.icon.guideRootIcon
    edit isGearGuide -> isBlueprintComponent"""
    rootIco = null(parent, name, width, color, m, pos_offset, rot_offset)
    cubeWidth = width / 2.0
    cubeIco = cube(parent,
                   name,
                   cubeWidth,
                   cubeWidth,
                   cubeWidth,
                   color,
                   m,
                   pos_offset,
                   rot_offset)

    for shp in cubeIco.listRelatives(shapes=True):
        rootIco.addChild(shp, add=True, shape=True)
    pm.delete(cubeIco)

    attribute.setNotKeyableAttributes(rootIco)
    attribute.addAttribute(rootIco, "is_guide_component", "bool", keyable=False)
    # Set the control shapes isHistoricallyInteresting
    for oShape in rootIco.getShapes():
        oShape.isHistoricallyInteresting.set(False)

    return rootIco


def guide_root_icon_2d(parent=None,
                       name="root",
                       width=.5,
                       color=[1, 0, 0],
                       m=datatypes.Matrix(),
                       pos_offset=None,
                       rot_offset=None):
    """Create a curve with a 2D ROOT GUIDE shape.
    Note:
        This icon is specially design for **Shifter** root guides
    Arguments:
        parent (dagNode): The parent object of the newly created curve.
        name (str): Name of the curve.
        width (float): Width of the shape.
        color (int or list of float): The color in index base or RGB.
        m (matrix): The global transformation of the curve.
        pos_offset (vector): The xyz position offset of the curve from
            its center.
        rot_offset (vector): The xyz rotation offset of the curve from
            its center. xyz in radians
    Returns:
        dagNode: The newly created icon.
    """
    rootIco = null(parent, name, width, color, m, pos_offset, rot_offset)
    pm.delete(rootIco.getShapes()[-1])  # Remove the z axis

    rot_offset_orig = datatypes.Vector(math.radians(90), 0, 0)
    if rot_offset:
        rot_offset_orig.rotateBy(rot_offset)

    squareWidth = width / 2.0
    squareIco = square(parent,
                       name,
                       squareWidth,
                       squareWidth,
                       color,
                       m,
                       pos_offset,
                       rot_offset_orig)

    for shp in squareIco.listRelatives(shapes=True):
        rootIco.addChild(shp, add=True, shape=True)
    pm.delete(squareIco)

    attribute.setNotKeyableAttributes(rootIco)
    attribute.addAttribute(rootIco, "is_guide", "bool", keyable=False)
    # Set the control shapes isHistoricallyInteresting
    for oShape in rootIco.getShapes():
        oShape.isHistoricallyInteresting.set(False)

    return rootIco


def guide_locator_icon(parent=None,
                       name="locator",
                       width=.5,
                       color=[1, 1, 0],
                       m=datatypes.Matrix(),
                       pos_offset=None,
                       rot_offset=None):
    """Create a curve with a LOCATOR GUIDE shape.
    Note:
        This icon is specially design for **Shifter** locator guides
    Arguments:
        parent (dagNode): The parent object of the newly created curve.
        name (str): Name of the curve.
        width (float): Width of the shape.
        color (int or list of float): The color in index base or RGB.
        m (matrix): The global transformation of the curve.
        pos_offset (vector): The xyz position offset of the curve from
            its center.
        rot_offset (vector): The xyz rotation offset of the curve from
            its center. xyz in radians
    Returns:
        dagNode: The newly created icon.
    """
    rootIco = null(parent, name, width, color, m, pos_offset, rot_offset)
    spheWidth = width / 2.0

    sphereIco = sphere(
        parent, name, spheWidth, color, m, pos_offset, rot_offset, degree=3)

    for shp in sphereIco.listRelatives(shapes=True):
        rootIco.addChild(shp, add=True, shape=True)
    pm.delete(sphereIco)

    attribute.setNotKeyableAttributes(rootIco)
    attribute.addAttribute(rootIco, "is_guide", "bool", keyable=False)
    # Set the control shapes isHistoricallyInteresting
    for oShape in rootIco.getShapes():
        oShape.isHistoricallyInteresting.set(False)

    return rootIco


def guide_blade_icon(parent=None,
                     aim=None,
                     name="blade",
                     lenX=1.0,
                     color=[1, 0, 0],
                     m=datatypes.Matrix(),
                     pos_offset=None,
                     rot_offset=None):
    """

    :param parent:
    :param aim:
    :param name:
    :param lenX:
    :param color:
    :param m:
    :param pos_offset:
    :param rot_offset:
    :return:
    """
    v0 = datatypes.Vector(0, 0, 0)
    v1 = datatypes.Vector(lenX, 0, 0)
    v2 = datatypes.Vector(0, lenX / 3, 0)

    points = get_point_array_with_offset(
        [v0, v1, v2], pos_offset, rot_offset)

    bladeIco = curve.addCurve(parent, name, points, True, 1, m)
    curve.set_color(bladeIco, color)

    attribute.addAttribute(bladeIco, "roll_offset", "float", 0)
    attribute.setNotKeyableAttributes(bladeIco, attributes=["roll_offset"])
    pm.pointConstraint(parent, bladeIco)
    aim_cons = pm.aimConstraint(aim,
                                bladeIco,
                                offset=(0, 0, 0),
                                aimVector=(1, 0, 0),
                                upVector=(0, 1, 0),
                                worldUpType="objectrotation",
                                worldUpVector=(0, 1, 0),
                                worldUpObject=parent)
    bladeIco.roll_offset >> aim_cons.offsetX
    attribute.setKeyableAttributes(bladeIco, [])
    attribute.addAttribute(bladeIco, "is_guide", "bool", keyable=False)
    # bladeIco.scale.set(1, 1, 1)
    # Set the control shapes isHistoricallyInteresting
    for oShape in bladeIco.getShapes():
        oShape.isHistoricallyInteresting.set(False)

    return bladeIco


def get_point_array_with_offset(point_pos, pos_offset=None, rot_offset=None):
    """Get Point array with offset
    Convert a list of vector to a List of float and add the position and
    rotation offset.
    Arguments:
        point_pos (list of vector): Point positions.
        pos_offset (vector):  The position offset of the curve from its
            center.
        rot_offset (vector): The rotation offset of the curve from its
            center. In radians.
    Returns:
        list of vector: the new point positions
    """
    points = list()
    for v in point_pos:
        if rot_offset:
            mv = om.MVector(v.x, v.y, v.z)
            mv = mv.rotateBy(om.MEulerRotation(rot_offset.x,
                                               rot_offset.y,
                                               rot_offset.z,
                                               om.MEulerRotation.kXYZ))
            v = datatypes.Vector(mv.x, mv.y, mv.z)
        if pos_offset:
            v = v + pos_offset

        points.append(v)

    return points
