# -*- coding:utf-8 -*-
"""from mgear.core.attribute"""

# mgear
import mgear


def add_attribute(node,
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
    """edit mgear.core.attribute.addAttribute
    add multi option"""
    if node.hasAttr(longName):
        mgear.log("Attribute already exists", mgear.sev_error)
        return

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