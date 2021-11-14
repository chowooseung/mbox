# -*- coding: utf-8 -*-

# maya
from pymel import mayautils
from maya import cmds


def mbox_menu_install():
    """mbox menu install"""

    import mbox
    mbox.environ()
    mbox.mbox_menu()

    import mbox.lego.menu
    mbox.lego.menu.install()

    import mbox.menu
    mbox.menu.install_help(mbox.menu_id)


if not cmds.about(batch=True):
    mayautils.executeDeferred(mbox_menu_install)