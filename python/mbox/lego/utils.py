# -*- coding: utf-8 -*-

# built-in
import os
import sys
import importlib
from types import ModuleType

# maya
import pymel.core as pm


# mbox.__init__.py
MBOX_ROOT = os.getenv("MBOX_ROOT")
MBOX_BOX = os.getenv("MBOX_BOX")
MBOX_CUSTOM_BOX = os.getenv("MBOX_CUSTOM_BOX")

# sys path append
# load_block_module import component
if MBOX_BOX not in sys.path:
    sys.path.append(MBOX_BOX)
for path in MBOX_CUSTOM_BOX.split(";"):
    if path not in sys.path:
        sys.path.append(path)


def get_blocks_directory() -> dict:
    result = dict()
    msg = "same name block exists"
    default_block_dir = [d for d in os.listdir(MBOX_BOX)
                         if os.path.isdir(os.path.join(MBOX_BOX, d)) and "__pycache__" not in d]
    assert len(set(default_block_dir)) == len(default_block_dir), msg
    result[MBOX_BOX] = list(set(default_block_dir))
    if os.path.exists(MBOX_CUSTOM_BOX):
        custom_block_dir = [d for d in os.listdir(MBOX_CUSTOM_BOX)
                            if os.path.isdir(os.path.join(MBOX_CUSTOM_BOX, d)) and "__pycache__" not in d]
        assert len(set(custom_block_dir)) == len(custom_block_dir), msg
        assert len(set(default_block_dir+custom_block_dir)) == len(default_block_dir+custom_block_dir), msg
        result[MBOX_CUSTOM_BOX] = list(set(custom_block_dir))
    return result


def load_block_module(component: str, guide: bool) -> ModuleType:
    blocks_dir = get_blocks_directory()
    check = None
    for box_path, blocks in blocks_dir.items():
        if component in blocks:
            check = True
    assert check is True, f"{component} don't exists in box"
    mod = importlib.import_module(f"{component}.guide" if guide else f"{component}")
    return mod


def load_build_step(block) -> tuple:
    mod = load_block_module(block["component"], guide=False)
    objects = mod.Objects(block)
    attributes = mod.Attributes(block)
    operators = mod.Operators(block)
    connection = mod.Connection(block)
    return objects, attributes, operators, connection


def select_guide() -> pm.nodetypes.Transform:
    msg = "selected node is not mbox guide node"
    selected = pm.selected(type="transform")
    assert len(selected) > 0, msg
    assert selected[0].hasAttr("is_guide") is True \
           or selected[0].hasAttr("is_guide_component") is True \
           or selected[0].hasAttr("is_guide_root") is True, msg
    return selected[0]

