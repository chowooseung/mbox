# -*- coding:utf-8 -*-

#
import math

# maya
from maya.api.OpenMaya import MTransformationMatrix, MMatrix, MVector, MQuaternion
import pymel.core as pm


def get_distance(input1, input2):
    """

    :param input1:
    :param input2:
    :return:
    """
    # Handles MVector case
    if (isinstance(input1, MVector)
            and isinstance(input2, MVector)):
        _vector = input2 - input1
    # Handles PyNodes case
    elif (isinstance(input1, pm.nodetypes.Transform)
          and isinstance(input2, pm.nodetypes.Transform)):
        vector_1 = input1.getTranslation(space="world")
        vector_2 = input2.getTranslation(space="world")
        _vector = vector_2 - vector_1
    # Handles list case
    elif isinstance(input1, list) and isinstance(input2, list):
        # Calculates distance
        return math.sqrt(sum([(vec_a - vec_b) ** 2
                              for vec_a, vec_b in zip(input1, input2)]))

    distance = _vector.length()
    return distance


def get_3point_normal(input1, input2, input3):
    """

    :param input1:
    :param input2:
    :param input3:
    :return:
    """
    # Handles PyNodes case
    if (isinstance(input1, pm.nodetypes.Transform)
            and isinstance(input2, pm.nodetypes.Transform)
            and isinstance(input3, pm.nodetypes.Transform)):
        input1 = input1.getTranslation()
        input2 = input2.getTranslation()
        input3 = input3.getTranslation()
    # Handles list case
    elif (isinstance(input1, list) and isinstance(input2, list)
          and isinstance(input3, list)):
        input1 = MVector(input1[0], input1[1], input1[2])
        input2 = MVector(input2[0], input2[1], input2[2])
        input3 = MVector(input3[0], input3[1], input3[2])

    # Calculates normal vector
    vector_a = input2 - input1
    vector_b = input3 - input1
    vector_a.normalize()
    vector_b.normalize()
    normal = vector_b ^ vector_a
    normal.normalize()

    return normal


def get_3point_binormal(input1, input2, input3):
    """

    :param input1:
    :param input2:
    :param input3:
    :return:
    """
    # Get plane normal vector
    normal_vector = get_3point_normal(input1, input2, input3)

    # Calculate binormal vector
    vector_a = input2 - input1
    binormal = normal_vector ^ vector_a
    binormal.normalize()

    return binormal


def linear_interpolation(input1, input2, blend=0.5):
    """

    :param input1:
    :param input2:
    :param blend:
    :return:
    """
    # Handles PyNodes case
    if (isinstance(input1, pm.nodetypes.Transform)
            and isinstance(input2, pm.nodetypes.Transform)):
        input1 = input1.getTranslation()
        input2 = input2.getTranslation()
    # Handles list case
    elif isinstance(input1, list) and isinstance(input2, list):
        input1 = MVector(input1[0], input1[1], input1[2])
        input2 = MVector(input2[0], input2[1], input2[2])

    # Calculates interpolated vector
    vector = input2 - input1
    vector *= blend
    vector += input1

    return MVector(vector[0], vector[1], vector[2])


def get_transposed_vector(vector, origin, result, inverse=False):
    """

    :param vector:
    :param origin:
    :param result:
    :param inverse:
    :return:
    """
    v0 = origin[1] - origin[0]
    v0.normalize()

    v1 = result[1] - result[0]
    v1.normalize()

    ra = v0.angle(v1)

    if inverse:
        ra = -ra

    axis = v0 ^ v1

    vector = rotate_vector_by_quaternion(vector, axis, ra)

    # Check if the rotation has been set in the right order
    # ra2 = (math.pi *.5 ) - v1.angle(vector)
    # vector = rotateAlongAxis(v, axis, -ra2)

    return vector


def rotate_vector_by_quaternion(vector, axis, radius):
    """

    :param vector:
    :param axis:
    :param radius:
    :return:
    """
    sa = math.sin(radius / 2.0)
    ca = math.cos(radius / 2.0)

    q1 = MQuaternion(vector.x, vector.y, vector.z, 0)
    q2 = MQuaternion(axis.x * sa, axis.y * sa, axis.z * sa, ca)
    q2n = MQuaternion(-axis.x * sa, -axis.y * sa, -axis.z * sa, ca)
    q = q2 * q1
    q *= q2n

    out = MVector(q.x, q.y, q.z)

    return out


class Blade(object):
    """The Blade object for shifter guides"""

    def __init__(self, t=pm.datatypes.Matrix()):

        self.transform = t

        d = [t.data[j][i]
             for j in range(len(t.data))
             for i in range(len(t.data[0]))]

        m = MMatrix(d)
        m = MTransformationMatrix(m)

        x = MVector(1, 0, 0).rotateBy(m.rotation())
        y = MVector(0, 1, 0).rotateBy(m.rotation())
        z = MVector(0, 0, 1).rotateBy(m.rotation())

        self.x = pm.datatypes.Vector(x.x, x.y, x.z)
        self.y = pm.datatypes.Vector(y.x, y.y, y.z)
        self.z = pm.datatypes.Vector(z.x, z.y, z.z)