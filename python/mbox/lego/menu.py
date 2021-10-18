# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
import mbox

# mgear
import mgear.menu

#
import logging

logger = logging.getLogger(__name__)


def install():
    """

    """
    commands = (
        ("Lego Box", str_lego_box),
        ("", None),
        ("Settings", str_settings),
        ("Extract Controls", str_extract_controls),
        ("", None),
        ("Build from selection", str_build_from_selection),
        ("Build from blueprint", str_build_from_blueprint),
        ("", None),
        ("Import blueprint", str_import_blueprint),
        ("Export blueprint", str_export_blueprint),
        ("", None),
        ("Reload lego box", str_reload_lego_box)
    )
    mgear.menu.install("Lego", commands, parent=mbox.menu_id)


str_lego_box = """
from mbox.lego import legoboxui
legoboxui.show_lego_box()"""

str_settings = """
from mbox.lego import lib
lib.inspect_settings()"""

str_extract_controls = """
from mbox.lego import lib
lib.extract_controls()"""

str_build_from_selection = """
"""

str_build_from_blueprint = """
"""

str_import_blueprint = """
from mbox.lego import lib
lib.import_blueprint(None)"""

str_export_blueprint = """
from mbox.lego import lib
lib.export_blueprint(None, None)"""

str_reload_lego_box = """
"""