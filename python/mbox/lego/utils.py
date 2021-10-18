# -*- coding: utf-8 -*-

#
import os

# mbox
from mbox.lego import box
from mgear.core import utils


def get_blocks_directory():
    return utils.gatherCustomModuleDirectories(
        "MBOX_CUSTOM_BOX_PATH",
        [os.path.join(os.path.dirname(box.__file__))])


def load_block_init(block):
    dirs = get_blocks_directory()
    defFmt = "mbox.lego.box.{}"
    customFmt = "{}"

    mod = utils.importFromStandardOrCustomDirectories(dirs, defFmt, customFmt, block)
    return mod


def load_block_blueprint(block):
    """Import the Component """
    dirs = get_blocks_directory()
    defFmt = "mbox.lego.box.{}.blueprint"
    customFmt = "{}.blueprint"

    mod = utils.importFromStandardOrCustomDirectories(dirs, defFmt, customFmt, block)
    return mod


def load_block_setting(block):
    """Import the Component """
    dirs = get_blocks_directory()
    defFmt = "mbox.lego.box.{}.setting"
    customFmt = "{}.setting"

    mod = utils.importFromStandardOrCustomDirectories(dirs, defFmt, customFmt, block)
    return mod