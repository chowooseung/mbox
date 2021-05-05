# -*- coding:utf-8 -*-

# maya

# mbox


def add(node,
        longName,
        attributeType,
        value=None,
        niceName=None,
        shortName=None,
        minValue=None,
        maxValue=None,
        multi=None,
        keyable=True,
        readable=True,
        storable=True,
        writable=True,
        channelBox=None):
    """
    add attribute

    :param node:
    :param longName:
    :param attributeType:
    :param value:
    :param niceName:
    :param shortName:
    :param minValue:
    :param maxValue:
    :param keyable:
    :param multi:
    :param readable:
    :param storable:
    :param writable:
    :param channelBox:
    :return: attribute
    """

    # if node.hasAttr(longName):
    #     log.log("Attribute : {0} Already exists".format(longName), log.error)
    #     return

    data = dict()

    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName
    if attributeType == "string":
        data["dataType"] = attributeType
    else:
        data["attributeType"] = attributeType

    if minValue is not None and minValue is not False:
        data["minValue"] = minValue
    if maxValue is not None and maxValue is not False:
        data["maxValue"] = maxValue

    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable

    if value is not None and attributeType not in ["string"]:
        data["defaultValue"] = value

    if isinstance(multi, bool) or isinstance(multi, int):
        data["multi"] = multi

    node.addAttr(longName, **data)

    if value is not None:
        node.setAttr(longName, value)

    if channelBox:
        node.attr(longName).set(channelBox=True)
    return node.attr(longName)


def add_color(node,
              longName,
              value=None,
              keyable=None,
              multi=None,
              readable=None,
              storable=None,
              writable=None,
              niceName=None,
              shortName=None):
    """
    add color attribute

    :param node:
    :param longName:
    :param value:
    :param keyable:
    :param multi:
    :param readable:
    :param storable:
    :param writable:
    :param niceName:
    :param shortName:
    :return:
    """


def add_enum(node,
             longName,
             value,
             enum,
             niceName=None,
             shortName=None,
             keyable=True,
             readable=True,
             storable=True,
             writable=True):
    """
    add enum attribute

    :param node:
    :param longName:
    :param value:
    :param enum:
    :param niceName:
    :param shortName:
    :param keyable:
    :param readable:
    :param storable:
    :param writable:
    :return:
    """
    # if node.hasAttr(longName):
    #     mgear.log("Attribute '" + longName + "' already exists",
    #               mgear.sev_warning)
    #     return

    data = dict()

    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName

    data["attributeType"] = "enum"
    data["en"] = ":".join(enum)

    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable

    node.addAttr(longName, **data)
    node.setAttr(longName, value)

    return node.attr(longName)


def add_proxy(sourceAttrs, targets, duplicatedPolicy=None):
    """
    proxy attribute

    :param sourceAttrs:
    :param targets:
    :param duplicatedPolicy:
    :return:
    """


def move(attr, sourceNode, targetNode):
    """
    source -> target attribute move

    :param attr:
    :param sourceNode:
    :param targetNode:
    :return:
    """


def lock(nodes, attrs):
    """
    attribute lock

    :param nodes: transform or transform list
    :param attrs: attribute or attribute list
    :return:
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    if not isinstance(attrs, list):
        attrs = [attrs]

    for node in nodes:
        for attr in attrs:
            node.setAttr(attr, lock=True)


def unlock(nodes, attrs):
    """
    attribute unlock

    :param nodes: transform or transform list
    :param attrs: attribute or attribute list
    :return:
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    if not isinstance(attrs, list):
        attrs = [attrs]

    for node in nodes:
        for attr in attrs:
            node.setAttr(attr, lock=False)


def hide(nodes, attrs):
    """

    :param nodes:
    :param attrs:
    :return:
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    if not isinstance(attrs, list):
        attrs = [attrs]

    for node in nodes:
        for attr in attrs:
            node.setAttr(attr, keyable=False, channelBox=False)


def key(nodes, attrs):
    """
    attribute keyable

    :param nodes: transform or transform list
    :param attrs: attribute or attribute list
    :return:
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    if not isinstance(attrs, list):
        attrs = [attrs]

    for node in nodes:
        for attr in attrs:
            node.setAttr(attr, keyable=True)


def non_key(nodes, attrs):
    """
    attribute

    :param nodes: transform or transform list
    :param attrs: attribute or attribute list
    :return:
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    if not isinstance(attrs, list):
        attrs = [attrs]

    for node in nodes:
        for attr in attrs:
            node.setAttr(attr, keyable=False, channelBox=True)


def change_rotate_order(node, rotateOrder):
    """
    when rotateOrder change, euler revalue

    :param node:
    :param rotateOrder:
    :return:
    """

