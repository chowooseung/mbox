# -*- coding:utf-8 -*-

#
import math

# maya
import pymel.core as pm

# mbox
from mbox.core import vector


def get_transform_looking_at(pos, lookAt, normal, axis="xy", negate=False):
    """Return a transformation matrix using vector positions.
    Return the transformation matrix of the dagNode oriented looking to
    an specific point.
    Arguments:
        pos (vector): The position for the transformation
        lookAt (vector): The aiming position to stablish the orientation
        normal (vector): The normal control the transformation roll.
        axis (str): The 2 axis used for lookat and normal. Default "xy"
        negate (bool): If true, invert the aiming direction.
    Returns:
        matrix: The transformation matrix
    """
    normal.normalize()

    if negate:
        a = pos - lookAt
    else:
        a = lookAt - pos

    a.normalize()
    c = pm.util.cross(a, normal)
    c.normalize()
    b = pm.util.cross(c, a)
    b.normalize()

    if axis == "xy":
        X = a
        Y = b
        Z = c
    elif axis == "xz":
        X = a
        Z = b
        Y = -c
    elif axis == "x-z":
        X = a
        Z = -b
        Y = c
    elif axis == "yx":
        Y = a
        X = b
        Z = -c
    elif axis == "yz":
        Y = a
        Z = b
        X = c
    elif axis == "zx":
        Z = a
        X = b
        Y = c
    elif axis == "z-x":
        Z = a
        X = -b
        Y = -c
    elif axis == "zy":
        Z = a
        Y = b
        X = -c
    elif axis == "x-y":
        X = a
        Y = -b
        Z = -c
    elif axis == "-xz":
        X = -a
        Z = b
        Y = c
    elif axis == "-xy":
        X = -a
        Y = b
        Z = c

    m = pm.datatypes.Matrix()
    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def get_chain_transform(positions, normal, axis="xz", negate=False):
    """

    :param positions:
    :param normal:
    :param axis:
    :param negate:
    :return:
    """
    # Draw
    transforms = list()
    for i in range(len(positions) - 1):
        v0 = positions[i - 1]
        v1 = positions[i]
        v2 = positions[i + 1]

        # Normal Offset
        if i > 0:
            normal = vector.get_transposed_vector(
                normal, [v0, v1], [v1, v2])

        t = get_transform_looking_at(v1, v2, normal, axis, negate)
        transforms.append(t)

    return transforms


def get_chain_transform2(positions, normal, axis="xz", negate=False):
    """

    :param positions:
    :param normal:
    :param axis:
    :param negate:
    :return:
    """
    # Draw
    transforms = list()
    for i in range(len(positions)):
        if i == len(positions) - 1:
            v0 = positions[i - 1]
            v1 = positions[i]
            v2 = positions[i - 2]

        else:
            v0 = positions[i - 1]
            v1 = positions[i]
            v2 = positions[i + 1]

        # Normal Offset
        if i > 0 and i != len(positions) - 1:
            normal = vector.get_transposed_vector(
                normal, [v0, v1], [v1, v2])

        if i == len(positions) - 1:
            axis = "-" + axis
            t = get_transform_looking_at(v1, v0, normal, axis, negate)
        else:
            t = get_transform_looking_at(v1, v2, normal, axis, negate)
        transforms.append(t)

    return transforms


def get_transform_from_pos(pos):
    """Create a transformation Matrix from a given position.
    Arguments:
        pos (vector): Position for the transformation matrix
    Returns:
        matrix: The newly created transformation matrix
    >>>  t = tra.getTransformFromPos(self.guide.pos["root"])
    """
    m = pm.datatypes.Matrix()
    m[0] = [1.0, 0, 0, 0.0]
    m[1] = [0, 1.0, 0, 0.0]
    m[2] = [0, 0, 1.0, 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def get_offset_position(node, offset=[0, 0, 0]):
    """Get an offset position from dagNode
    Arguments:
        node (dagNode): The dagNode with the original position.
        offset (list of float): Ofsset values for xyz.
            exp : [1.2, 4.6, 32.78]
    Returns:
        list of float: the new offset position.
    Example:
        .. code-block:: python
            self.root = self.addRoot()
            vTemp = tra.getOffsetPosition( self.root, [0,-3,0.1])
            self.knee = self.addLoc("knee", self.root, vTemp)
    """
    offsetVec = pm.datatypes.Vector(offset[0], offset[1], offset[2])
    return offsetVec + node.get_translation(space="world")


def get_position_from_matrix(in_m):
    """Get the position values from matrix
    Arguments:
        in_m (matrix): The input Matrix.
    Returns:
        list of float: The position values for xyz.
    """
    pos = in_m[3][:3]

    return pos


def get_rotation_from_matrix(in_m):
    """Get the Rotation values from matrix

    :param in_m:
    :return:
    """


def set_matrix_position(in_m, pos):
    """Set the position for a given matrix
    Arguments:
        in_m (matrix): The input Matrix.
        pos (list of float): The position values for xyz
    Returns:
        matrix: The matrix with the new position
    >>> tnpo = tra.setMatrixPosition(tOld, tra.get_position_from_matrix(t))
    >>> t = tra.setMatrixPosition(t, self.guide.apos[-1])
    """
    m = pm.datatypes.Matrix()
    m[0] = in_m[0]
    m[1] = in_m[1]
    m[2] = in_m[2]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def set_matrix_rotation(in_m, rot_m):
    """Set the rotation for a given matrix

    :param in_m:
    :param rot_m:
    :return:
    """
    X = rot_m[0]
    Y = rot_m[1]
    Z = rot_m[2]

    in_m[0] = [X[0], X[1], X[2], 0.0]
    in_m[1] = [Y[0], Y[1], Y[2], 0.0]
    in_m[2] = [Z[0], Z[1], Z[2], 0.0]

    return in_m


def set_matrix_scale(in_m, scl=[1, 1, 1]):
    """Set the scale for a given matrix
    Arguments:
        in_m (matrix): The input Matrix.
        scl (list of float): The scale values for xyz
    Returns:
        matrix: The matrix with the new scale
    """
    tm = pm.datatypes.TransformationMatrix(in_m)
    tm.setScale(scl, space="world")

    m = pm.datatypes.Matrix(tm)

    return m


def get_filtered_transform(m,
                           translation=True,
                           rotation=True,
                           scaling=True):
    """Retrieve a transformation filtered.
    Arguments:
        m (matrix): the reference matrix
        translation (bool): If true the return matrix will match the
            translation.
        rotation (bool): If true the return matrix will match the
            rotation.
        scaling (bool): If true the return matrix will match the
            scaling.
    Returns:
        matrix : The filtered matrix
    """

    t = pm.datatypes.Vector(m[3][0], m[3][1], m[3][2])
    x = pm.datatypes.Vector(m[0][0], m[0][1], m[0][2])
    y = pm.datatypes.Vector(m[1][0], m[1][1], m[1][2])
    z = pm.datatypes.Vector(m[2][0], m[2][1], m[2][2])

    out = pm.datatypes.Matrix()

    if translation:
        out = set_matrix_position(out, t)

    if rotation and scaling:
        out = set_matrix_rotation(out, [x, y, z])
    elif rotation and not scaling:
        out = set_matrix_rotation(out, [x.normal(), y.normal(), z.normal()])
    elif not rotation and scaling:
        out = set_matrix_rotation(out, [pm.datatypes.Vector(1, 0, 0) * x.length(),
                                        pm.datatypes.Vector(0, 1, 0) * y.length(),
                                        pm.datatypes.Vector(0, 0, 1) * z.length()])

    return out


##########################################################
# ROTATION
##########################################################


def getRotationFromAxis(in_a, in_b, axis="xy", negate=False):
    """Get the matrix rotation from a given axis.
    Arguments:
        in_a (vector): Axis A
        in_b (vector): Axis B
        axis (str): The axis to use for the orientation. Default: "xy"
        negate (bool): negates the axis orientation.
    Returns:
        matrix: The newly created matrix.
    Example:
        .. code-block:: python
            x = pm.datatypes.Vector(0,-1,0)
            x = x * tra.getTransform(self.eff_loc)
            z = pm.datatypes.Vector(self.normal.x,
                                 self.normal.y,
                                 self.normal.z)
            z = z * tra.getTransform(self.eff_loc)
            m = tra.getRotationFromAxis(x, z, "xz", self.negate)
    """
    a = pm.datatypes.Vector(in_a.x, in_a.y, in_a.z)
    b = pm.datatypes.Vector(in_b.x, in_b.y, in_b.z)
    c = pm.datatypes.Vector()

    if negate:
        a *= -1

    a.normalize()
    c = a ^ b
    c.normalize()
    b = c ^ a
    b.normalize()

    if axis == "xy":
        x = a
        y = b
        z = c
    elif axis == "xz":
        x = a
        z = b
        y = -c
    elif axis == "yx":
        y = a
        x = b
        z = -c
    elif axis == "yz":
        y = a
        z = b
        x = c
    elif axis == "zx":
        z = a
        x = b
        y = c
    elif axis == "zy":
        z = a
        y = b
        x = -c

    m = pm.datatypes.Matrix()
    setMatrixRotation(m, [x, y, z])

    return m


def get_symmetrical_transform(matrix, axis="yz"):
    """

    :param matrix:
    :param axis:
    :return:
    """
    mirror = None
    if axis == "yz":
        mirror = pm.datatypes.Matrix(-1.0, 0.0, 0.0, 0.0,
                                     0.0, 1.0, 0.0, 0.0,
                                     0.0, 0.0, 1.0, 0.0,
                                     0.0, 0.0, 0.0, 1.0)

    if axis == "xy":
        mirror = pm.datatypes.Matrix(1.0, 0.0, 0.0, 0.0,
                                     0.0, 1.0, 0.0, 0.0,
                                     0.0, 0.0, -1.0, 0.0,
                                     0.0, 0.0, 0.0, 1.0)
    if axis == "zx":
        mirror = pm.datatypes.Matrix(1.0, 0.0, 0.0, 0.0,
                                     0.0, -1.0, 0.0, 0.0,
                                     0.0, 0.0, 1.0, 0.0,
                                     0.0, 0.0, 0.0, 1.0)
    matrix *= mirror

    return matrix


def reset_transform(node, t=True, r=True, s=True):
    """Reset the scale, rotation and translation for a given dagNode.
    Arguments:
        node(dagNode): The object to reset the transforms.
        t (bool): If true translation will be reseted.
        r (bool): If true rotation will be reseted.
        s (bool): If true scale will be reseted.
    Returns:
        None
    """
    trs_dict = {"tx": 0,
                "ty": 0,
                "tz": 0,
                "rx": 0,
                "ry": 0,
                "rz": 0,
                "sx": 1,
                "sy": 1,
                "sz": 1}

    t_axis = ["tx", "ty", "tz"]
    r_axis = ["rx", "ry", "rz"]
    s_axis = ["sx", "sy", "sz"]
    axis = []

    if t:
        axis = axis + t_axis
    if r:
        axis = axis + r_axis
    if s:
        axis = axis + s_axis

    for a in axis:
        try:
            node.attr(a).set(trs_dict[a])
        except Exception:
            pass


def matchWorldTransform(source, target):
    """Match 2 dagNode transformations in world space.
    Arguments:
        source (dagNode): The source dagNode
        target (dagNode): The target dagNode
    Returns:
        None
    """
    sWM = source.getMatrix(worldSpace=True)
    target.setMatrix(sWM, worldSpace=True)


def quaternionDotProd(q1, q2):
    """Get the dot product of 2 quaternion.
    Arguments:
        q1 (quaternion): Input quaternion 1.
        q2 (quaternion): Input quaternion 2.
    Returns:
        quaternion: The dot proct quaternion.
    """
    dot = q1.x * q2.x + q1.y * q2.y + q1.z * q2.z + q1.w * q2.w
    return dot


def quaternionSlerp(q1, q2, blend):
    """Get an interpolate quaternion based in slerp function.
    Arguments:
        q1 (quaternion): Input quaternion 1.
        q2 (quaternion): Input quaternion 2.
        blend (float): Blending value.
    Returns:
        quaternion: The interpolated quaternion.
    Example:
        .. code-block:: python
            q = quaternionSlerp(pm.datatypes.Quaternion(
                                t1.getRotationQuaternion()),
                                pm.datatypes.Quaternion(
                                    t2.getRotationQuaternion()), blend)
    """
    dot = quaternionDotProd(q1, q2)
    if dot < 0.0:
        dot = quaternionDotProd(q1, q2.negateIt())

    arcos = math.acos(round(dot, 10))
    sin = math.sin(arcos)

    if sin > 0.001:
        w1 = math.sin((1.0 - blend) * arcos) / sin
        w2 = math.sin(blend * arcos) / sin
    else:
        w1 = 1.0 - blend
        w2 = blend

    result = (pm.datatypes.Quaternion(q1).scaleIt(w1)
              + pm.datatypes.Quaternion(q2).scaleIt(w2))

    return result


def convert2TransformMatrix(tm):
    """Convert a transformation Matrix
    Convert a transformation Matrix or a matrix to a transformation
    matrix in world space.
    Arguments:
        tm (matrix): The input matrix.
    Returns:
        matrix: The transformation matrix in worldSpace
    """
    if isinstance(tm, pm.nodetypes.Transform):
        tm = pm.datatypes.TransformationMatrix(tm.getMatrix(worldSpace=True))
    if isinstance(tm, pm.datatypes.Matrix):
        tm = pm.datatypes.TransformationMatrix(tm)

    return tm


def getInterpolateTransformMatrix(t1, t2, blend=.5):
    """Interpolate 2 matrix.
    Arguments:
        t1 (matrix): Input matrix 1.
        t2 (matrix): Input matrix 2.
        blend (float): The blending value. Default 0.5
    Returns:
        matrix: The newly interpolated transformation matrix.
    >>> t = tra.getInterpolateTransformMatrix(self.fk_ctl[0],
                                              self.tws1A_npo,
                                              .3333)
    """
    # check if the input transforms are transformMatrix
    t1 = convert2TransformMatrix(t1)
    t2 = convert2TransformMatrix(t2)

    if blend == 1.0:
        return t2
    elif blend == 0.0:
        return t1

    # translate
    pos = vector.linearlyInterpolate(t1.get_translation(space="world"),
                                     t2.get_translation(space="world"),
                                     blend)

    # scale
    scaleA = pm.datatypes.Vector(*t1.getScale(space="world"))
    scaleB = pm.datatypes.Vector(*t2.getScale(space="world"))

    vs = vector.linearlyInterpolate(scaleA, scaleB, blend)

    # rotate
    q = quaternionSlerp(pm.datatypes.Quaternion(t1.getRotationQuaternion()),
                        pm.datatypes.Quaternion(t2.getRotationQuaternion()),
                        blend)

    # out
    result = pm.datatypes.TransformationMatrix()

    result.setTranslation(pos, space="world")
    result.setRotationQuaternion(q.x, q.y, q.z, q.w)
    result.setScale([vs.x, vs.y, vs.z], space="world")

    return result


def interpolate_rotation(obj, targets, blends):
    rot = [0, 0, 0]
    for t, b in zip(targets, blends):
        rot[0] += t.rx.get() * b
        rot[1] += t.ry.get() * b
        rot[2] += t.rz.get() * b

    obj.rotate.set(rot)


def interpolate_scale(obj, targets, blends):
    s = [0, 0, 0]
    for t, b in zip(targets, blends):
        s[0] += t.sx.get() * b
        s[1] += t.sy.get() * b
        s[2] += t.sz.get() * b

    obj.scale.set(s)


def getDistance2(obj0, obj1):
    """Get the distance between 2 objects.
    Arguments:
        obj0 (dagNode): Object A
        obj1 (dagNode): Object B
    Returns:
        float: Distance length
    """
    v0 = obj0.get_translation(space="world")
    v1 = obj1.get_translation(space="world")

    v = v1 - v0

    return v.length()


# TODO: Maybe better just return a list of the closes ordered trasform?
def get_closes_transform(target_transform, source_transforms):
    """Summary
    Args:
        target_transform (dagNode): target transform
        source_transforms ([dagNode]): objects to check distance
    Returns:
        list: ordered transform list
    """
    distances = {}
    for t in source_transforms:
        dist = getDistance2(t, target_transform)
        distances[t.name()] = [t, dist]
    sorted_dist = sorted(distances.items(), key=lambda kv: kv[1][1])

    return sorted_dist
