# -*- coding:utf-8 -*-

#
import logging
import os

# mbox
from mbox import version
from mbox import menu

# maya
import pymel.core as pm

logger = logging.getLogger(__name__)

menu_id = "mBox"


def environ():
    os.environ["MBOX_ROOT"] = os.path.dirname(__file__)
    os.environ["MBOX_BOX"] = os.path.join(os.environ["MBOX_ROOT"], "lego", "box")
    os.environ["MBOX_CUSTOM_BOX"] = ""


def mbox_menu():
    """mbox menu setup

    :return:
    """
    menu.create(menu_id)


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
