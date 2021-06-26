# -*- coding:utf-8 -*-

#
import logging

#
from mbox import version

logger = logging.getLogger(__name__)


def mbox_info():
    logger.info("mbox Information")
    logger.info("version {0}".format(mbox_version()))


def mbox_version():
    return version.version


def mbox_menu():
    """mbox menu setup

    :return:
    """