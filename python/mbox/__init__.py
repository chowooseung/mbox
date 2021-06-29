# -*- coding:utf-8 -*-

#
import logging
import os

# mbox
from mbox import version

# maya
import pymel.core as pm

logger = logging.getLogger(__name__)


def log_information():
    logger.info("mbox Information")
    logger.info("mbox version : {0}".format(version.mbox))
    logger.info("schema version : {0}".format(version.schema))


def mbox_menu():
    """mbox menu setup

    :return:
    """


def about():
    """

    :return:
    """
    mbox_msg = ("\nmbox version : {0}\n\n"
                "mbox started with the aim of studying mgear. Therefore, most core functions come from mgear. "
                "mgear is the best rigging framework. But mgear's inheritance was a bit complicated for me. "
                "So I think I revised it in an easier way. "
                "My programming level is still low, so things I've changed may have gone in the wrong direction.\n\n"
                "".format(version.mbox))

    mbox_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    license_file = os.path.join(mbox_dir, "LICENSE")
    with open(license_file, "r") as f:
        license_msg = f.readlines()
    for l_msg in license_msg:
        mbox_msg += "{0}".format(l_msg)

    pm.confirmDialog(title="About mbox",
                     message=mbox_msg,
                     button=["OK"],
                     defaultButton="OK",
                     cancelButton="OK",
                     dismissString="OK")
