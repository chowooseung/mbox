# -*- coding:utf-8 -*-
"""lego rig module"""

# maya
import pymel.core as pm

# json
import json
from mbox.vendor import jsonschema

# mbox
from mbox.core import transform

#
import os
import sys
import copy
import logging
import imp
from collections import OrderedDict

logger = logging.getLogger(__name__)


def prepare(context):
    """prepare to rig building
    preScripts run

    :return:
    """
    logger.info("Step. prepare")

    # scripts
    try:
        for script in context["preScripts"]:
            logger.info("import. {0}".format(script))
            mod = imp.load_source(pm.Path(script).namebase, pm.Path(script).rstrip())
            logger.info("Run. {0}".format(script))
            mod.main(context)
    except ImportError as e:
        logger.error("ImportError {0}".format(e))
    except RuntimeError as e:
        logger.error("RuntimeError {0}".format(e))
    except SyntaxError as e:
        logger.error("SyntaxError {0}".format(e))


def objects(context):
    """generate nodes

    :return:
    """
    logger.info("Step. objects")


def attributes(context):
    """generate attributes

    :return:
    """
    logger.info("Step. attributes")


def operate(context):
    """apply operation

    :return:
    """
    logger.info("Step. operate")


def finalize(context):
    """set, unused node delete, other cleanup
    poseScripts run

    :return:
    """
    logger.info("Step. finalize")


def lego(bp):
    """

    :return:
    """
    context = OrderedDict()
    context["process"] = bp["process"]
    context["name"] = bp["name"]
    context["direction"] = bp["direction"]
    context["controllerExp"] = bp["nameRule"]["controllerExp"]
    context["jointExp"] = bp["nameRule"]["jointExp"]
    context["commonConvention"] = bp["nameRule"]["convention"]["common"]
    context["jointConvention"] = bp["nameRule"]["convention"]["joint"]
    context["jointDescriptionLetterCase"] = bp["nameRule"]["jointDescriptionLetterCase"]
    context["controllerDescriptionLetterCase"] = bp["nameRule"]["controllerDescriptionLetterCase"]
    context["runPreScripts"] = bp["runPreScripts"]
    context["runPostScripts"] = bp["runPostScripts"]
    context["preScripts"] = bp["preScripts"]
    context["postScripts"] = bp["postScripts"]

    prepare(context)
    objects(context)
    attributes(context)
    finalize(context)
