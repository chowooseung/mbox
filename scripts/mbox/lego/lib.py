# -*- coding: utf-8 -*-

# maya
import pymel.core as pm
import maya.api.OpenMaya as om

# mbox
import mbox
from mbox.lego import (
    utils,
    naming)

# built-in
import os
import uuid
import logging
import itertools
from collections import OrderedDict

# mgear
from mgear.core import (
    pyqt,
    attribute,
    primitive,
    transform,
    icon,
    node)

# json
import json

logger = logging.getLogger(__name__)


def get_component_guide(component):
    if component.hasAttr("is_guide"):
        while True:
            parent = component.getParent() if component.getParent().hasAttr("is_guide_component") else None
            component = parent
            if parent:
                break
    elif component.hasAttr("is_guide_root"):
        return [component]

    repeated = [component]
    guides = list()
    guides += repeated
    while True:
        children = list()
        for r in repeated:
            children += [x for x in r.getChildren(type="transform") if x.hasAttr("is_guide")]
        guides += children
        if not children:
            break
        repeated = children
    return guides


def get_child_component(component):
    guides = get_component_guide(component)

    return [x for y in guides for x in y.getChildren(type="transform") if x.hasAttr("is_guide_component")]


def get_hierarchy_from_guide(component, data):
    children = get_child_component(component)
    child = OrderedDict().fromkeys([x.message.outputs(type="network")[0] for x in children], None)
    data[component.message.outputs(type="network")[0]] = child if child else None

    for child in children:
        get_hierarchy_from_guide(child, data[component.message.outputs(type="network")[0]])
    return data


def get_hierarchy_from_network(_network, data):
    children = _network.affects[0].outputs(type="network")
    child = OrderedDict().fromkeys(children, None)
    data[_network] = child if child else None

    for child in children:
        get_hierarchy_from_network(child, data[_network])
    return data


def blueprint_from_guide(selected):
    if not selected:
        raise RuntimeError
    elif isinstance(selected, list):
        selected = selected[0]

    hierarchy = None
    if selected.hasAttr("is_guide_root"):
        hierarchy = get_hierarchy_from_guide(selected, OrderedDict())
    elif selected.hasAttr("is_guide_component"):
        hierarchy = OrderedDict()
        network = selected.getParent(generations=-1).message.outputs(type="network")[0]
        hierarchy[network] = get_hierarchy_from_guide(selected, OrderedDict())
    elif selected.hasAttr("is_guide"):
        selected = [x for x in get_component_guide(selected) if x.hasAttr("is_guide_component")][0]
        hierarchy = OrderedDict()
        network = selected.getParent(generations=-1).message.outputs(type="network")[0]
        hierarchy[network] = get_hierarchy_from_guide(selected, OrderedDict())

    return blueprint_from_network(hierarchy)


def blueprint_from_network(hierarchy):
    # recursive
    def get_blueprint(_p_block, _network, children):
        mod = utils.load_block_module(_network.attr("comp_type").get(), guide=True)
        block = mod.Block(parent=_p_block)
        block.network = _network
        if children:
            for _key, _value in children.items():
                get_blueprint(block, _key, _value)

    #   ----

    network = next(itertools.islice(hierarchy.keys(), 1))
    blueprint = RootBlock()
    blueprint.network = network

    for key, value in hierarchy[network].items():
        get_blueprint(blueprint, key, value)

    blueprint.from_network()
    return blueprint


def blueprint_from_rig():
    rig_root = utils.select_guide().getParent(generations=-1)
    root_network = rig_root.message.outputs(type="network")[0]

    hierarchy = get_hierarchy_from_network(root_network, OrderedDict())
    return blueprint_from_network(hierarchy)


def blueprint_from_file(path):
    """TODO: get blueprint from file"""
    check = True
    if not os.path.exists(path):
        logger.info(f"Don't exists path : {path}")
    elif os.path.splitext(path)[-1] != ".mbox":
        logger.info(f"This file not .mbox ext")
    else:
        check = False

    if check:
        return

    with open(path, "r") as f:
        data = json.load(f)

    # recursive
    def get_blueprint(_block, _data):
        for child in _data["blocks"]:
            mod = utils.load_block_module(child["comp_type"], guide=True)
            _b = mod.Block(_block)
            get_blueprint(_b, child)

    #   ----

    blueprint = RootBlock()
    get_blueprint(blueprint, data)
    blueprint.update(data)
    return blueprint


def draw_specify_component_guide(parent, component):
    if not parent:
        # root block
        blueprint = RootBlock()

        # component block
        mod = utils.load_block_module(component, guide=True)
        mod.Block(parent=blueprint)

        blueprint.guide()
    else:
        parent = get_component_guide(parent)[0]

        blueprint = blueprint_from_guide(parent.getParent(generations=-1))
        mod = utils.load_block_module(component, guide=True)
        parent_network = parent.message.outputs(type="network")[0]
        parent_block = blueprint.find_block_with_oid(parent_network.attr("oid").get())
        block = mod.Block(parent_block)
        if parent_block is not blueprint:
            block["comp_side"] = parent_block["comp_side"]
            parent = parent_network.attr("transforms").inputs(type="transform")[-1]
        comp_index = blueprint.solve_index(mod.NAME, block["comp_side"], 0, block)
        block["comp_index"] = comp_index

        # translation offset
        offset_t = parent.getTranslation(space="world")
        for index, t in enumerate(block["transforms"]):
            m = pm.datatypes.Matrix(t)
            block["transforms"][index] = transform.setMatrixPosition(m, m.translate + offset_t)

        pm.select(block.guide())


def inspect_settings(guide=None, network=None):
    selected = pm.selected(type="transform")
    if selected:
        root = selected[0]
    else:
        pm.displayWarning(
            "please select one object from the component guide")
        return

    comp_type = False
    guide_root = False
    while root:
        if pm.attributeQuery("is_guide_component", node=root, exists=True):
            network = root.message.outputs(type="network")[0]
            comp_type = network.attr("comp_type").get()
            break
        elif pm.attributeQuery("is_guide_root", node=root, exists=True):
            guide_root = root
            network = guide_root.message.outputs(type="network")[0]
            break
        root = root.getParent()

    if comp_type:
        mod = utils.load_block_module(comp_type, guide=True)
        window = pyqt.showDialog(mod.BlockSettings, dockable=True)
        window.tabs.setCurrentIndex(0)

    elif guide_root:
        module_name = "mbox.lego.box.settings"
        mod = __import__(module_name, globals(), locals(), ["*"], 0)
        window = pyqt.showDialog(mod.RootSettings, dockable=True)
        window.tabs.setCurrentIndex(0)

    else:
        pm.displayError("The selected object is not part of component guide")


def log_window():
    """"""
    log_window_name = "mbox_lego_build_log_window"
    log_window_field_reporter = "mbox_lego_build_log_field_reporter"
    if not pm.window(log_window_name, exists=True):
        logWin = pm.window(log_window_name, title="Lego Build Log", iconName="Shifter Log")
        pm.columnLayout(adjustableColumn=True)
        pm.cmdScrollFieldReporter(log_window_field_reporter, width=800, height=500, clear=True)
        pm.button(label="Close",
                  command=("import pymel.core as pm\npm.deleteUI('{logWin}', window=True)".format(logWin=logWin)))
        pm.setParent('..')
        pm.showWindow(logWin)
    else:
        pm.cmdScrollFieldReporter(log_window_field_reporter, edit=True, clear=True)
        pm.showWindow(log_window_name)


def export_blueprint(guide, path):
    """TODO:blueprint json file export"""
    if not path:
        path = _file_dialog(path, mode=0)
        if not path:
            pm.displayWarning("File path None")
            return
    if not guide:
        try:
            guide = pm.selected(type="transform")[0]
            if not guide.hasAttr("is_guide_root"):
                raise RuntimeError("select mbox root guide")
        except IndexError as e:
            pm.displayWarning(e)
            return
        except RuntimeError as e:
            pm.displayWarning(e)
            return

    root_block = blueprint_from_guide(guide)
    root_block.save(root_block, path)


def import_blueprint(path, draw=True):
    """TODO:blueprint json file import"""
    if not path:
        path = _file_dialog(path, mode=1)
        if not path:
            pm.displayWarning("File path None")
            return

    root_block = blueprint_from_file(path)
    if draw:
        pm.select(root_block.draw_guide())

    return root_block


def _file_dialog(path=None, mode=0):
    """from mgear.shifter.io._get_file
    mode [0:save, 1:open]"""
    file_path = pm.fileDialog2(
        startingDirectory=path if path else pm.workspace(query=True, rootDirectory=True),
        fileMode=mode,
        fileFilter='mBox Guide Template .mbox (*%s)' % ".mbox")

    if not file_path:
        return

    return file_path[0]


class _List(list):

    def append(self, obj):
        assert isinstance(obj, AbstractBlock)
        super(_List, self).append(obj)


class Context(list):

    def __init__(self, blueprint):
        self._blueprint = blueprint

    def instance(self, name):
        for ins in self:
            if name == ins.name:
                return ins
        ins = Instance(name)
        self.append(ins)
        return ins

    @property
    def blueprint(self):
        return self._blueprint


class Instance(dict):

    def __init__(self, name):
        assert isinstance(name, str)

        self._name = name

        self["root"] = None
        self["ctls"] = list()
        self["jnts"] = list()
        self["refs"] = list()
        self["script_node"] = list()

    def __repr__(self):
        return f"ins(\"{self.name}\")"

    @property
    def name(self):
        return self._name


class AbstractBlock(dict):

    def __init__(self, parent=None):
        self._network = None
        self._parent = parent
        if self._parent:
            self._parent["blocks"].append(self)
        self["oid"] = str(uuid.uuid4())
        self["blocks"] = _List()
        #  self.attributes = list()

    def __setitem__(self, key, value):
        if key == "blocks":
            assert isinstance(value, _List)
        super().__setitem__(key, value)

    def update(self, _d, **kwargs):
        # recursive
        def _update(_block, _dict):
            for k, v in _dict.items():
                if k == "blocks" or k == "oid":
                    continue
                _block[k] = v

            for index, b_data in enumerate(_dict["blocks"]):
                mod = utils.load_block_module(b_data["comp_type"], guide=True)
                _b = mod.Block(_block)
                _update(_b, b_data)

        #   ----

        for key, value in kwargs.items():
            _d[key] = value

        self["blocks"] = _List()
        _update(self, _d)

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    @property
    def build_step(self):
        return utils.load_build_step(self)

    @property
    def top(self):
        if not self.parent:
            return self
        parent = self.parent
        while parent.parent:
            parent = parent.parent
        return parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent:
            self._parent["blocks"].remove(self)
        self._parent = parent
        self._parent["blocks"].append(self)

    @property
    def ins_name(self):
        if isinstance(self, RootBlock):
            return f"{self['comp_type']}"
        elif isinstance(self, SubBlock):
            return f"{self['comp_name']}_{self['comp_side']}_{self['comp_index']}"

    @property
    def negate(self):
        return True if self['comp_side'] == "right" else False

    def from_network(self):
        # recursive
        def _from_network(_block):
            _block.from_network()

            for _b in _block["blocks"]:
                _from_network(_b)

        #   ----

        for block in self["blocks"]:
            _from_network(block)

    def to_network(self):
        # recursive
        def _to_network(_block):
            _block.to_netwrok()

            for _b in _block["blocks"]:
                _to_network(_b)

        #   ----

        for block in self["blocks"]:
            _to_network(block)

    def guide(self):
        # recursive
        def _guide(_block):
            root = _block.guide()

            if not _block["blocks"]:
                return root

            for _b in _block["blocks"]:
                return _guide(_b)

        #   ----

        root = None
        for block in self["blocks"]:
            root = _guide(block)

        return root


class SubBlock(AbstractBlock):

    def __init__(self, parent=None):
        super(SubBlock, self).__init__(parent=parent)

        # block version
        self["version"] = None

        # what kind of block
        self["comp_type"] = None

        # module name # arm... leg... spine...
        self["comp_name"] = None

        # "center", "left", "right"
        self["comp_side"] = "center"

        # index
        self["comp_index"] = 0

        # ui host
        self["ui_host"] = str()

        #
        self["joint_names"] = str()

        # gimmick joint
        self["blend_joint"] = str()
        self["support_joint"] = str()

        # ctl color
        self["override_color"] = False
        self["use_RGB_color"] = False
        self["color_fk"] = 6
        self["color_ik"] = 18
        self["RGB_fk"] = (0.0, 0.0, 1.0)
        self["RGB_ik"] = (0.0, 0.25, 1.0)

        # primary axis, secondary axis, offset XYZ
        # self["joint_settings"] = [["x", "y", (0, 0, 0)], ]

        # guide transform matrix list
        # self["transforms"] = list()

        # parent node name
        self["ref_index"] = -1

        # ctl shapes
        self["ctl_shapes"] = dict()

        # Joints Axis
        self["joints_axis"] = list()

        # connector
        self["connector"] = "standard"

    def from_network(self):
        self["oid"] = self.network.attr("oid").get()
        self["version"] = self.network.attr("version").get()
        self["comp_type"] = self.network.attr("comp_type").get()
        self["comp_name"] = self.network.attr("comp_name").get()
        self["comp_side"] = self.network.attr("comp_side").get(asString=True)
        self["comp_index"] = self.network.attr("comp_index").get()
        self["ui_host"] = self.network.attr("ui_host").get()
        self["joint_names"] = self.network.attr("joint_names").get()
        self["blend_joint"] = self.network.attr("blend_joint").get()
        self["support_joint"] = self.network.attr("support_joint").get()
        self["use_RGB_color"] = self.network.attr("use_RGB_color").get()
        self["override_color"] = self.network.attr("override_color").get()
        self["color_fk"] = self.network.attr("color_fk").get()
        self["color_ik"] = self.network.attr("color_ik").get()
        self["RGB_fk"] = self.network.attr("RGB_fk").get()
        self["RGB_ik"] = self.network.attr("RGB_ik").get()
        self["transforms"] = [x.tolist() for x in self.network.attr("transforms").get()]
        # TODO: control shapes curve info
        if self.network.attr("ctls").elements():
            shape_dict = dict()
            for index, attr in enumerate(self.network.attr("ctls").elements()):
                shapes_network = self.network.attr(attr).outputs(type="network")
                if shapes_network:
                    shape_dict[index] = dict()
                for shape_index, network in enumerate(sorted(shapes_network, key=lambda x: x.attr("order"))):
                    shape_dict[index][shape_index] = dict()
                    shape_dict[index][shape_index]["degree"] = 3
                    shape_dict[index][shape_index]["form"] = 0
                    shape_dict[index][shape_index]["form_id"] = 0
                    shape_dict[index][shape_index]["points"] = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
                    shape_dict[index][shape_index]["knots"] = []
            self["ctl_shapes"] = shape_dict
        else:
            self["ctl_shapes"] = dict()
        # TODO: specify joints axis
        self["joints_axis"] = [x.tolist() if x else list() for x in self.network.attr("joints_axis").get().split(",")]
        self["connector"] = self.network.attr("connector").get()

    def to_network(self):
        self.network.attr("oid").set(self["oid"])
        self.network.attr("version").set(self["version"])
        self.network.attr("comp_type").set(self["comp_type"])
        self.network.attr("comp_name").set(self["comp_name"])
        self.network.attr("comp_side").set(self["comp_side"])
        self.network.attr("comp_index").set(self["comp_index"])
        self.network.attr("ui_host").set(self["ui_host"])
        self.network.attr("joint_names").set(self["joint_names"])
        self.network.attr("blend_joint").set(self["blend_joint"])
        self.network.attr("support_joint").set(self["support_joint"])
        self.network.attr("override_color").set(self["override_color"])
        self.network.attr("use_RGB_color").set(self["use_RGB_color"])
        self.network.attr("color_fk").set(self["color_fk"])
        self.network.attr("color_ik").set(self["color_ik"])
        self.network.attr("RGB_fk").set(self["RGB_fk"])
        self.network.attr("RGB_ik").set(self["RGB_ik"])
        [self.network.attr("transforms")[i].set(t)
         if not self.network.attr("transforms")[i].inputs()
         else self.network.attr("transforms")[i].inputs()[0].setMatrix(pm.datatypes.Matrix(t), worldSpace=True)
         for i, t in enumerate(self["transforms"])]
        # TODO: control shapes curve info
        shapes_network = self.network.attr("ctls").outputs(type="network")
        pm.delete(shapes_network) if shapes_network else None
        for index in sorted(list(self["ctl_shapes"].keys())):
            for order in sorted(list(self["ctl_shapes"][index].keys())):
                data = self["ctl_shapes"][index][order]
                network = pm.createNode("network")
                attribute.addAttribute(network, "order", "long", order, keyable=False)
                attribute.addAttribute(network, "degree", "long", data["degree"], keyable=False)
                attribute.addAttribute(network, "points", "string", data["points"])
                attribute.addAttribute(network, "form", "long", data["form"], keyable=False)
                attribute.addAttribute(network, "form_id", "long", data["form_id"], keyable=False)
                attribute.addAttribute(network, "knots", "string", data["knots"])
        # TODO: specify joints axis
        joints_axis = [pm.datatypes.Matrix(x) if x else "" for x in self["joints_axis"]]
        joints_axis = ",".join(joints_axis)
        self.network.attr("joints_axis").set(joints_axis)
        self.network.attr("connector").set(self["connector"])

    def guide(self):
        self.network = pm.createNode("network")
        n = self.network
        attribute.addAttribute(n, "oid", "string", self["oid"])
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "version", "string", self["version"])
        attribute.addAttribute(n, "comp_type", "string", self["comp_type"])
        attribute.addAttribute(n, "comp_name", "string", self["comp_name"])
        attribute.addEnumAttribute(n, "comp_side", self["comp_side"],
                                   ["center", "left", "right"], keyable=False)
        attribute.addAttribute(n, "comp_index", "long", self["comp_index"], keyable=False)
        attribute.addAttribute(n, "ui_host", "string", self["ui_host"])
        attribute.addAttribute(n, "joint_names", "string", self["joint_names"])
        attribute.addAttribute(n, "blend_joint", "string", self["blend_joint"])
        attribute.addAttribute(n, "support_joint", "string", self["support_joint"])
        attribute.addAttribute(n, "override_color", "bool", self["override_color"], keyable=False)
        attribute.addAttribute(n, "use_RGB_color", "bool", self["use_RGB_color"], keyable=False)
        attribute.addAttribute(n, "color_fk", "long", self["color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "color_ik", "long", self["color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addColorAttribute(n, "RGB_fk", self["RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "RGB_ik", self["RGB_ik"], keyable=False)
        pm.addAttr(n, longName="transforms", type="matrix", multi=True)
        pm.addAttr(n, longName="ctls", type="message", multi=True)
        pm.addAttr(n, longName="jnts", type="message", multi=True)
        # TODO: control shapes curve info
        for index in sorted(list(self["ctl_shapes"].keys())):
            for order in sorted(list(self["ctl_shapes"][index].keys())):
                data = self["ctl_shapes"][index][order]
                network = pm.createNode("network")
                attribute.addAttribute(network, "order", "long", order, keyable=False)
                attribute.addAttribute(network, "degree", "long", data["degree"], keyable=False)
                attribute.addAttribute(network, "points", "string", data["points"])
                attribute.addAttribute(network, "form", "long", data["form"], keyable=False)
                attribute.addAttribute(network, "form_id", "long", data["form_id"], keyable=False)
                attribute.addAttribute(network, "knots", "string", data["knots"])
        # TODO: specify joints axis
        joints_axis = [pm.datatypes.Matrix(x) if x else "" for x in self["joints_axis"]]
        joints_axis = ",".join(joints_axis)
        attribute.addAttribute(n, "joints_axis", "string", joints_axis)
        attribute.addAttribute(n, "connector", "string", self["connector"])
        attribute.addAttribute(n, "script_node", "message")

    def update_guide(self):
        """update guide naming"""
        guide = self.network.attr("guide").inputs(type="transform")
        if not guide:
            return

        guides = get_component_guide(guide[0])
        for guide in guides:
            suffix_list = guide.nodeName().split("_")[2:]
            suffix = "_".join(suffix_list)
            name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}"
            guide.rename(f"{name}_{suffix}")
        pm.select(guides[0])

    def duplicate(self, blueprint, parent, mirror=False):
        mod = utils.load_block_module(self["comp_type"], guide=True)
        copy_block = mod.Block(parent)
        copy_block.update(self)

        def _duplicate(_blueprint, _block, _mirror):
            if _mirror and _block["comp_side"] != "center":
                for index, m in enumerate(_block["transforms"]):
                    m = pm.datatypes.Matrix(m)
                    _block["transforms"][index] = transform.getSymmetricalTransform(m).tolist()
                if _block["comp_side"] == "left":
                    _block["comp_side"] = "right"
                elif _block["comp_side"] == "right":
                    _block["comp_side"] = "left"
            index = _blueprint.solve_index(_block["comp_name"], _block["comp_side"], _block["comp_index"], _block)
            _block["comp_index"] = index
            guide = _block.guide()
            for _b in _block["blocks"]:
                _duplicate(_blueprint, _b, _mirror)
            return guide

        return _duplicate(blueprint, copy_block, mirror)


class RootBlock(AbstractBlock):

    def __init__(self):
        super(RootBlock, self).__init__(parent=None)

        # component
        self["comp_type"] = "mbox"

        # version
        self["version"] = mbox.version.mbox

        # WIP or PUB
        self["process"] = "WIP"

        # "all", "preScripts", "objects", "attributes", "operators", "connection", "additionalFunc", "postScripts"
        self["step"] = "all"

        # Asset name
        self["name"] = "rig"

        # Name side
        self["joint_left_name"] = naming.DEFAULT_JOINT_SIDE_L_NAME
        self["joint_right_name"] = naming.DEFAULT_JOINT_SIDE_R_NAME
        self["joint_center_name"] = naming.DEFAULT_JOINT_SIDE_C_NAME
        self["ctl_left_name"] = naming.DEFAULT_SIDE_L_NAME
        self["ctl_right_name"] = naming.DEFAULT_SIDE_R_NAME
        self["ctl_center_name"] = naming.DEFAULT_SIDE_C_NAME

        # Name extension
        self["joint_name_ext"] = naming.DEFAULT_JOINT_EXT_NAME
        self["ctl_name_ext"] = naming.DEFAULT_CTL_EXT_NAME

        # Name rule
        self["joint_name_rule"] = naming.DEFAULT_NAMING_RULE
        self["ctl_name_rule"] = naming.DEFAULT_NAMING_RULE

        # default, lower, upper, capitalize
        self["joint_description_letter_case"] = "default"
        self["ctl_description_letter_case"] = "default"

        # padding
        self["joint_index_padding"] = 0
        self["ctl_index_padding"] = 0

        # world ctl
        self["world_ctl"] = False
        self["world_ctl_name"] = "world_ctl"

        # joint rig
        self["joint_rig"] = True
        self["connect_joints"] = False

        # uni scale
        self["force_uni_scale"] = False

        # bool
        self["run_pre_custom_step"] = False
        self["run_post_custom_step"] = False

        # Scripts path
        self["pre_custom_step"] = str()
        self["post_custom_step"] = str()

        # Schema version
        self["schema"] = mbox.version.schema

        # controls index color
        self["l_color_fk"] = 6
        self["l_color_ik"] = 18
        self["r_color_fk"] = 23
        self["r_color_ik"] = 14
        self["c_color_fk"] = 13
        self["c_color_ik"] = 17

        # use RGB color
        self["use_RGB_color"] = False

        # controls RGB color
        self["l_RGB_fk"] = (0, 0, 1)
        self["l_RGB_ik"] = (0, 0.25, 1)
        self["r_RGB_fk"] = (1, 0, 0)
        self["r_RGB_ik"] = (1, 0.1, 0.25)
        self["c_RGB_fk"] = (1, 1, 0)
        self["c_RGB_ik"] = (0, 0.6, 0)

        # notes
        self["notes"] = "Rig Info\n\ndescription :"

    def from_network(self):
        self["oid"] = self.network.attr("oid").get()
        self["name"] = self.network.attr("name").get()
        self["version"] = self.network.attr("version").get()
        self["schema"] = self.network.attr("schema").get()
        self["process"] = self.network.attr("process").get(asString=True)
        self["step"] = self.network.attr("step").get(asString=True)
        self["joint_left_name"] = self.network.attr("joint_left_name").get()
        self["joint_right_name"] = self.network.attr("joint_right_name").get()
        self["joint_center_name"] = self.network.attr("joint_center_name").get()
        self["ctl_left_name"] = self.network.attr("ctl_left_name").get()
        self["ctl_right_name"] = self.network.attr("ctl_right_name").get()
        self["ctl_center_name"] = self.network.attr("ctl_center_name").get()
        self["joint_name_ext"] = self.network.attr("joint_name_ext").get()
        self["ctl_name_ext"] = self.network.attr("ctl_name_ext").get()
        self["joint_name_rule"] = self.network.attr("joint_name_rule").get()
        self["ctl_name_rule"] = self.network.attr("ctl_name_rule").get()
        self["joint_description_letter_case"] = self.network.attr("joint_description_letter_case").get(asString=True)
        self["ctl_description_letter_case"] = \
            self.network.attr("ctl_description_letter_case").get(asString=True)
        self["joint_index_padding"] = self.network.attr("joint_index_padding").get()
        self["ctl_index_padding"] = self.network.attr("ctl_index_padding").get()
        self["world_ctl"] = self.network.attr("world_ctl").get()
        self["world_ctl_name"] = self.network.attr("world_ctl_name").get()
        self["joint_rig"] = self.network.attr("joint_rig").get()
        self["connect_joints"] = self.network.attr("connect_joints").get()
        self["force_uni_scale"] = self.network.attr("force_uni_scale").get()
        self["run_pre_custom_step"] = self.network.attr("run_pre_custom_step").get()
        self["pre_custom_step"] = self.network.attr("pre_custom_step").get()
        self["run_post_custom_step"] = self.network.attr("run_post_custom_step").get()
        self["post_custom_step"] = self.network.attr("post_custom_step").get()
        self["l_color_fk"] = self.network.attr("l_color_fk").get()
        self["l_color_ik"] = self.network.attr("l_color_ik").get()
        self["r_color_fk"] = self.network.attr("r_color_fk").get()
        self["r_color_ik"] = self.network.attr("r_color_ik").get()
        self["c_color_fk"] = self.network.attr("c_color_fk").get()
        self["c_color_ik"] = self.network.attr("c_color_ik").get()
        self["use_RGB_color"] = self.network.attr("use_RGB_color").get()
        self["l_RGB_fk"] = self.network.attr("l_RGB_fk").get()
        self["l_RGB_ik"] = self.network.attr("l_RGB_ik").get()
        self["r_RGB_fk"] = self.network.attr("r_RGB_fk").get()
        self["r_RGB_ik"] = self.network.attr("r_RGB_ik").get()
        self["c_RGB_fk"] = self.network.attr("c_RGB_fk").get()
        self["c_RGB_ik"] = self.network.attr("c_RGB_ik").get()
        self["notes"] = self.network.attr("notes").get()

        # recursive block
        super(RootBlock, self).from_network()

    def to_network(self):
        self.network.attr("oid").set(self["oid"])
        self.network.attr("name").set(self["name"])
        self.network.attr("version").set(self["version"])
        self.network.attr("schema").set(self["schema"])
        self.network.attr("process").set(self["process"])
        self.network.attr("step").set(self["step"])
        self.network.attr("joint_left_name").set(self["joint_left_name"])
        self.network.attr("joint_right_name").set(self["joint_right_name"])
        self.network.attr("joint_center_name").set(self["joint_center_name"])
        self.network.attr("ctl_left_name").set(self["ctl_left_name"])
        self.network.attr("ctl_right_name").set(self["ctl_right_name"])
        self.network.attr("ctl_center_name").set(self["ctl_center_name"])
        self.network.attr("joint_name_ext").set(self["joint_name_ext"])
        self.network.attr("ctl_name_ext").set(self["ctl_name_ext"])
        self.network.attr("joint_name_rule").set(self["joint_name_rule"])
        self.network.attr("ctl_name_rule").set(self["ctl_name_rule"])
        self.network.attr("joint_description_letter_case").set(self["joint_description_letter_case"])
        self.network.attr("ctl_description_letter_case").set(self["ctl_description_letter_case"])
        self.network.attr("joint_index_padding").set(self["joint_index_padding"])
        self.network.attr("ctl_index_padding").set(self["ctl_index_padding"])
        self.network.attr("world_ctl").set(self["world_ctl"])
        self.network.attr("world_ctl_name").set(self["world_ctl_name"])
        self.network.attr("joint_rig").set(self["joint_rig"])
        self.network.attr("connect_joints").set(self["connect_joints"])
        self.network.attr("force_uni_scale").set(self["force_uni_scale"])
        self.network.attr("run_pre_custom_step").set(self["run_pre_custom_step"])
        self.network.attr("pre_custom_step").set(self["pre_custom_step"])
        self.network.attr("run_post_custom_step").set(self["run_post_custom_step"])
        self.network.attr("post_custom_step").set(self["post_custom_step"])
        self.network.attr("l_color_fk").set(self["l_color_fk"])
        self.network.attr("l_color_ik").set(self["l_color_ik"])
        self.network.attr("r_color_fk").set(self["r_color_fk"])
        self.network.attr("r_color_ik").set(self["r_color_ik"])
        self.network.attr("c_color_fk").set(self["c_color_fk"])
        self.network.attr("c_color_ik").set(self["c_color_ik"])
        self.network.attr("use_RGB_color").set(self["use_RGB_color"])
        self.network.attr("l_RGB_fk").set(self["l_RGB_fk"])
        self.network.attr("l_RGB_ik").set(self["l_RGB_ik"])
        self.network.attr("r_RGB_fk").set(self["r_RGB_fk"])
        self.network.attr("r_RGB_ik").set(self["r_RGB_ik"])
        self.network.attr("c_RGB_fk").set(self["c_RGB_fk"])
        self.network.attr("c_RGB_ik").set(self["c_RGB_ik"])
        self.network.attr("notes").set(self["notes"])

        # recursive block
        super(RootBlock, self).to_network()

    def guide(self):
        self.network = pm.createNode("network")
        n = self.network
        attribute.addAttribute(n, "oid", "string", self["oid"])
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "comp_type", "string", self["comp_type"])
        attribute.addAttribute(n, "name", "string", self["name"])
        attribute.addAttribute(n, "version", "string", self["version"])
        attribute.addAttribute(n, "schema", "string", self["schema"])
        attribute.addEnumAttribute(n, "process", self["process"], ["WIP", "PUB"], keyable=False)
        attribute.addEnumAttribute(n, "step", self["step"],
                                   ["all", "preScripts", "objects", "attributes", "operators", "connection",
                                    "additionalFunc", "postScripts"], keyable=False)
        attribute.addAttribute(n, "joint_left_name", "string", self["joint_left_name"])
        attribute.addAttribute(n, "joint_right_name", "string", self["joint_right_name"])
        attribute.addAttribute(n, "joint_center_name", "string", self["joint_center_name"])
        attribute.addAttribute(n, "ctl_left_name", "string", self["ctl_left_name"])
        attribute.addAttribute(n, "ctl_right_name", "string", self["ctl_right_name"])
        attribute.addAttribute(n, "ctl_center_name", "string", self["ctl_center_name"])
        attribute.addAttribute(n, "joint_name_ext", "string", self["joint_name_ext"])
        attribute.addAttribute(n, "ctl_name_ext", "string", self["ctl_name_ext"])
        attribute.addAttribute(n, "joint_name_rule", "string", self["joint_name_rule"])
        attribute.addAttribute(n, "ctl_name_rule", "string", self["ctl_name_rule"])
        attribute.addEnumAttribute(n, "joint_description_letter_case", self["joint_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addEnumAttribute(n, "ctl_description_letter_case", self["ctl_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addAttribute(n, "joint_index_padding", "long", self["joint_index_padding"], keyable=False)
        attribute.addAttribute(n, "ctl_index_padding", "long", self["ctl_index_padding"], keyable=False)
        attribute.addAttribute(n, "world_ctl", "bool", self["world_ctl"], keyable=False)
        attribute.addAttribute(n, "world_ctl_name", "string", self["world_ctl_name"])
        attribute.addAttribute(n, "joint_rig", "bool", self["joint_rig"], keyable=False)
        attribute.addAttribute(n, "connect_joints", "bool", self["connect_joints"], keyable=False)
        attribute.addAttribute(n, "force_uni_scale", "bool", self["force_uni_scale"], keyable=False)
        attribute.addAttribute(n, "run_pre_custom_step", "bool", self["run_pre_custom_step"], keyable=False)
        attribute.addAttribute(n, "pre_custom_step", "string", self["pre_custom_step"])
        attribute.addAttribute(n, "run_post_custom_step", "bool", self["run_post_custom_step"], keyable=False)
        attribute.addAttribute(n, "post_custom_step", "string", self["post_custom_step"])
        attribute.addAttribute(n, "l_color_fk", "long", self["l_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "l_color_ik", "long", self["l_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "r_color_fk", "long", self["r_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "r_color_ik", "long", self["r_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "c_color_fk", "long", self["c_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "c_color_ik", "long", self["c_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "use_RGB_color", "bool", self["use_RGB_color"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_fk", self["l_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_ik", self["l_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_fk", self["r_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_ik", self["r_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_fk", self["c_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_ik", self["c_RGB_ik"], keyable=False)
        attribute.addAttribute(n, "notes", "string", str(self["notes"]))
        pm.addAttr(n, longName="ctls", type="message", multi=True)
        pm.addAttr(n, longName="jnts", type="message", multi=True)
        attribute.addAttribute(n, "script_node", "message")

        guide = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())

        # attribute
        attribute.lockAttribute(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        attribute.addAttribute(guide, "is_guide_root", "bool", keyable=False)

        # connection
        pm.connectAttr(guide.attr("message"), n.attr("guide"), force=True)

        # recursive block
        sel = super(RootBlock, self).guide()

        # last created block select
        pm.select(sel)

    def find_block_with_oid(self, oid):
        # recursive
        def _find(_block, _oid):
            if _block["oid"] == _oid:
                return _block

            for _b in _block["blocks"]:
                __b = _find(_b, _oid)
                if __b:
                    return __b

        #   ----

        sub_block = None
        if self["oid"] == oid:
            return self

        for block in self["blocks"]:
            sub_block = _find(block, oid)

            if sub_block:
                break

        return sub_block

    def find_block_with_ins_name(self, ins_name):
        # recursive
        def _find(_block, _ins_name):
            if _block.ins_name == _ins_name:
                return _block

            for _b in _block["blocks"]:
                __b = _find(_b, _ins_name)
                if __b:
                    return __b

        #   ----

        sub_block = None
        if self.ins_name == ins_name:
            return self

        for block in self["blocks"]:
            sub_block = _find(block, ins_name)

            if sub_block:
                break

        return sub_block

    def solve_index(self, name, side, index=0, target_block=None) -> int:
        indexes = list()

        # get index list
        # recursive
        def _solve_index(_block, _indexes, _name, _side):
            if _block["comp_name"] == _name and _block["comp_side"] == _side:
                # target block index remove
                # in case already exists target block
                if _block is not target_block:
                    _indexes.append(_block["comp_index"])

            for _b in _block["blocks"]:
                _solve_index(_b, _indexes, _name, _side)

        #   ----
        for block in self["blocks"]:
            _solve_index(block, indexes, name, side)

        # next index
        while True:
            if index not in indexes:
                break
            index += 1

        return index


class PreScript:

    def __init__(self):
        self.msg = f"Process {self.__module__}.{self.__class__}"


class AbstractRig:

    def __init__(self, block: SubBlock):
        self._ins = None
        self._parent_ins = None
        self._top_ins = None
        self._block = block
        self._ins_name = block.ins_name
        self._parent_ins_name = block.parent.ins_name if block.parent else None
        self._top_ins_name = block.top.ins_name
        self.msg = f"Process {self.__class__.__name__} {self._ins_name}"

    def process(self, context):
        self._ins = context.instance(self._ins_name)
        self._parent_ins = context.instance(self._parent_ins_name) if self._parent_ins_name else None
        self._top_ins = context.instance(self._top_ins_name)

    @property
    def top_ins(self):
        return self._top_ins

    @property
    def parent_ins(self):
        return self._parent_ins

    @property
    def ins(self):
        return self._ins

    @property
    def block(self):
        return self._block


class AbstractObjects(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractObjects, self).__init__(block=block)

    def get_name(self,
                 typ: bool,
                 description: str = "",
                 extension: str = "") -> str:
        root_block = self.block.top
        if typ:
            rule = root_block["joint_name_rule"]
            padding = root_block["joint_index_padding"]
            description_letter_case = root_block["joint_description_letter_case"]
            side_set = [root_block["joint_left_name"], root_block["joint_right_name"], root_block["joint_center_name"]]
            if not extension:
                extension = root_block["joint_name_ext"]
        else:
            rule = root_block["ctl_name_rule"]
            padding = root_block["ctl_index_padding"]
            description_letter_case = root_block["ctl_description_letter_case"]
            side_set = [root_block["ctl_left_name"], root_block["ctl_right_name"], root_block["ctl_center_name"]]
            if not extension:
                extension = root_block["ctl_name_ext"]

        if description_letter_case == "lower":
            description = description.lower()
        elif description_letter_case == "upper":
            description = description.upper()
        elif description_letter_case == "capitalize":
            description = description.capitalize()

        index_filter = ["left", "right", "center"]
        side = side_set[index_filter.index(self.block["comp_side"])]
        name = rule.format(name=self.block["comp_name"],
                           side=side,
                           index=str(self.block["comp_index"]).zfill(padding),
                           description=description,
                           extension=extension)
        name = "_".join([x for x in name.split("_") if x])
        return name

    def get_ctl_color(self, ik_fk):
        color = None
        if self.block["override_color"]:
            if self.block["use_RGB_color"]:
                if ik_fk == "ik":
                    color = self.block["RGB_ik"]
                else:
                    color = self.block["RGB_fk"]
            else:
                if ik_fk == "ik":
                    color = self.block["color_ik"]
                else:
                    color = self.block["RGB_fk"]
        else:
            if self.block.top["use_RGB_color"]:
                if self.block["comp_side"] == "left":
                    if ik_fk == "ik":
                        color = self.block.top["l_RGB_ik"]
                    else:
                        color = self.block.top["l_RGB_fk"]
                elif self.block["comp_side"] == "right":
                    if ik_fk == "ik":
                        color = self.block.top["r_RGB_ik"]
                    else:
                        color = self.block.top["r_RGB_fk"]
                elif self.block["comp_side"] == "center":
                    if ik_fk == "ik":
                        color = self.block.top["c_RGB_ik"]
                    else:
                        color = self.block.top["c_RGB_fk"]
            else:
                if self.block["comp_side"] == "left":
                    if ik_fk == "ik":
                        color = self.block.top["l_color_ik"]
                    else:
                        color = self.block.top["l_color_fk"]
                elif self.block["comp_side"] == "right":
                    if ik_fk == "ik":
                        color = self.block.top["r_color_ik"]
                    else:
                        color = self.block.top["r_color_fk"]
                elif self.block["comp_side"] == "center":
                    if ik_fk == "ik":
                        color = self.block.top["c_color_ik"]
                    else:
                        color = self.block.top["c_color_fk"]
        return color

    def create_root(self,
                    context: Context,
                    m: pm.datatypes.Matrix) -> pm.nodetypes.Transform:
        instance = context.instance(self.block.ins_name)
        if self.block["comp_type"] == "mbox":
            parent = None
            name = self.block["name"]
            attr_name = "is_rig_root"
        else:
            parent_block = self.block.parent
            while True:
                parent_instance = context.instance(parent_block.ins_name)
                if parent_instance["refs"]:
                    break
                parent_block = parent_block.parent
            parent = parent_instance["refs"][0] \
                if isinstance(self.block.parent, RootBlock) \
                else parent_instance["refs"][self.block["ref_index"]]
            name = self.get_name(False, extension="root")
            attr_name = "is_rig_component"
        root = primitive.addTransform(parent, name, m=m)
        attribute.addAttribute(root, attr_name, "bool", keyable=False)
        attribute.setKeyableAttributes(root, [])

        instance["root"] = root
        return root

    def create_ctl(self,
                   context: Context,
                   parent: None or pm.nodetypes.Transform,
                   m: pm.datatypes.Matrix,
                   parent_ctl: None or pm.nodetypes.Transform,
                   color: list or int,
                   ctl_attr: list = ["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz"],
                   npo_attr: list = [],
                   description: str = "",
                   size: float = 1.0,
                   shape: str = "cube",
                   cns: bool = False) -> pm.nodetypes.Transform:
        instance = context.instance(self.block.ins_name)
        if cns:
            cns = primitive.addTransform(parent, self.get_name(False, description=description, extension="cns"), m=m)
            parent = cns
        npo = primitive.addTransform(parent, self.get_name(False, description=description, extension="npo"), m=m)
        ctl = icon.create(npo,
                          self.get_name(False, description=description, extension=self.block.top["ctl_name_ext"]),
                          m=m,
                          color=color,
                          icon=shape,
                          w=size,
                          h=size,
                          d=size)
        attribute.setKeyableAttributes(ctl, ctl_attr)
        attribute.setKeyableAttributes(npo, npo_attr)
        attribute.addAttribute(ctl, "is_ctl", "bool", keyable=False)

        top_instance = context.instance(self.block.top.ins_name)
        condition = top_instance["root"].attr("controls_mouseover").outputs(type="condition")[0]
        tag = node.add_controller_tag(ctl, parent_ctl)
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))

        instance["ctls"].append(ctl)
        return ctl

    def create_ref(self,
                   context: Context,
                   parent: None or pm.nodetypes.Transform,
                   description: str,
                   m: pm.datatypes.Matrix) -> pm.nodetypes.Transform:
        instance = context.instance(self.block.ins_name)
        ref = primitive.addTransform(parent, self.get_name(False, description=description, extension="ref"), m=m)
        attribute.setKeyableAttributes(ref, [])
        attribute.addAttribute(ref, "is_ref", "bool", keyable=False)

        instance["refs"].append(ref)
        return ref

    def create_jnt(self,
                   context: Context,
                   parent: None or pm.nodetypes.Joint,
                   description: str,
                   ref: pm.nodetypes.Transform) -> pm.nodetypes.Joint:
        instance = context.instance(self.block.ins_name)

        joint_name = None
        if self.block["joint_names"]:
            name_list = self.block["joint_names"].split(",")
            if len(name_list) >= len(instance["jnts"]):
                joint_name = name_list[len(instance["jnts"])]
        name = joint_name \
            if joint_name \
            else self.get_name(True, description=description, extension=self.block.top["joint_name_ext"])

        if parent is None:
            index = self.block["ref_index"]
            block = self.block
            top_ins = context.instance(self.block.top.ins_name)
            while parent is None:
                parent_b = block.parent
                if isinstance(parent_b, RootBlock):
                    parent = top_ins["joints_root"]
                    break

                parent_ins = context.instance(parent_b.ins_name)
                if parent_ins["jnts"]:
                    parent = parent_ins["jnts"][index]
                    break

                block = parent_b

        if self.block.top["connect_joints"] and pm.objExists(name):
            jnt = pm.PyNode(name)
            rotate = jnt.rotate.get()
            assert rotate == [0, 0, 0], f"{jnt} rotation is not zero\nrotation : {rotate}"
            pm.parent(jnt, parent)
            if isinstance(ref, pm.nodetypes.Transform):
                attribute.setKeyableAttributes(ref)
                attribute.setRotOrder(ref, jnt.attr("rotateOrder").get(asString=True).upper())
                pm.matchTransform(ref, jnt, position=True, rotation=True, scale=True)
                attribute.setKeyableAttributes(ref, [])
            elif isinstance(ref, pm.datatypes.Matrix):
                attribute.lockAttribute(jnt)
                attribute.setNotKeyableAttributes(jnt, ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"])
                instance["jnts"].append(jnt)
                return jnt
        elif isinstance(ref, pm.datatypes.Matrix):
            jnt = primitive.addJoint(parent, name, ref)
            jnt.setMatrix(ref, worldSpace=True)
            jnt.attr("jointOrientX").set(jnt.attr("rx").get())
            jnt.attr("jointOrientY").set(jnt.attr("ry").get())
            jnt.attr("jointOrientZ").set(jnt.attr("rz").get())
            jnt.attr("rotate").set((0, 0, 0))
            attribute.lockAttribute(jnt)
            attribute.setNotKeyableAttributes(jnt, ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"])
            instance["jnts"].append(jnt)
            return jnt
        else:
            jnt = primitive.addJoint(parent, name, ref.getMatrix(worldSpace=True))

        m_m = node.createMultMatrixNode(ref.attr("worldMatrix"), jnt.attr("parentInverseMatrix"), jnt, "st")

        m = m_m.attr("matrixSum").get()
        m_i = m.inverse()

        tm = pm.datatypes.TransformationMatrix(m)
        jo = pm.datatypes.degrees(tm.getRotation())

        jnt.attr("jointOrientX").set(jo[0])
        jnt.attr("jointOrientY").set(jo[1])
        jnt.attr("jointOrientZ").set(jo[2])

        m_m2 = node.createMultMatrixNode(m_m.attr("matrixSum"), m_i, jnt, "r")
        if jnt.attr("sz").get() < 0:
            plugs = jnt.attr("s").inputs(plugs=True)[0]
            pm.disconnectAttr(plugs, jnt.attr("s"))
            node.createMulDivNode(plugs, [1, 1, -1], 1, [jnt.attr("sx"), jnt.attr("sy"), jnt.attr("sz")])
            plugs = jnt.attr("r").inputs(plugs=True)[0]
            pm.disconnectAttr(plugs, jnt.attr("r"))
            m_d = node.createMulDivNode([], [-1, -1, 1], 1, [jnt.attr("rx"), jnt.attr("ry"), jnt.attr("rz")])
            pm.connectAttr(plugs, m_d.attr("input1"))

        attribute.lockAttribute(jnt)
        attribute.setNotKeyableAttributes(jnt, ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"])
        if not jnt.hasAttr("is_jnt"):
            attribute.addAttribute(jnt, "is_jnt", "bool", keyable=False)
        instance["jnts"].append(jnt)
        return jnt


class AbstractAttributes(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractAttributes, self).__init__(block=block)

    def process(self, context):
        super(AbstractAttributes, self).process(context=context)
        if isinstance(self.block, RootBlock):
            return
        if self.block["ui_host"]:
            _, index, oid = self.block["ui_host"].split(",")
            ui_host_block = self.block.top.find_block_with_oid(oid)
            host_instance = context.instance(ui_host_block.ins_name)
            if host_instance["ctls"]:
                ui_host = host_instance["ctls"][int(index)]
        else:
            ui_host = self.top_ins["ctls"][0]
        self.ins["ui_host"] = ui_host
        attribute.addEnumAttribute(self.ins["ui_host"], self.block.ins_name, " ", [" "])
        attribute.setNotKeyableAttributes(self.ins["ui_host"], [self.block.ins_name])

        if self.ins["script_node"]:
            attribute.addAttribute(self.ins["script_node"], "oid", "string")
            attribute.addAttribute(self.ins["script_node"], "target", "message")
            attribute.addAttribute(self.ins["script_node"], "script_node", "message")
            self.ins["script_node"].attr("oid").set(self.block["oid"])

    def create_attr(self, context, longName, attType, \
                    value, niceName=None, minValue=None, maxValue=None, keyable=True, \
                    readable=True, storable=True, writable=True, uihost=None):
        if not uihost:
            uihost = self.ins["ui_host"]
        if uihost.hasAttr(longName):
            attr = uihost.attr(longName)
        else:
            attr = attribute.addAttribute(uihost,
                                          longName, attType,
                                          value, niceName,
                                          minValue=minValue,
                                          maxValue=maxValue,
                                          keyable=keyable,
                                          readable=readable,
                                          storable=storable,
                                          writable=writable)
        return attr

    def create_enum_attr(self, context, longName, value, \
                         enum, niceName=None, keyable=True, readable=True, \
                         storable=True, writable=True, uihost=None):
        if not uihost:
            uihost = self.ins["ui_host"]
        if uihost.hasAttr(longName):
            attr = uihost.attr(longName)
        else:
            attr = attribute.addEnumAttribute(uihost,
                                              longName, value,
                                              enum, niceName, None,
                                              keyable=keyable,
                                              readable=readable,
                                              storable=storable,
                                              writable=writable)
        return attr


class AbstractOperators(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractOperators, self).__init__(block=block)

    def process(self, context):
        super(AbstractOperators, self).process(context=context)

    def space_switch(self, context, ctl, target, attr_name):
        script_node = pm.createNode("script", name=f"{self.block.ins_name}_sc")
        self.ins["script_node"].append(script_node)

        attribute.addAttribute(script_node, "oid", "string")
        attribute.addAttribute(script_node, "target", "message")
        attribute.addAttribute(script_node, "script_node", "message")
        script_node.attr("oid").set(self.block["oid"])
        script_node.attr("sourceType").set(1)
        script_node.attr("scriptType").set(0)
        match_attr_name = f"{attr_name}_match"
        array = [x.split(" | ") for x in self.block["ik_ref_array"].split(",")]
        ik_ref_ctls = list()
        for index, oid in array:
            block = self.block.top.find_block_with_oid(oid)
            target_instance = context.instance(block.ins_name)
            ik_ref_ctls.append(target_instance["ctls"][int(index)])
        enum = [x.nodeName() for x in ik_ref_ctls]
        attribute.addEnumAttribute(target,
                                   attr_name,
                                   value="self",
                                   enum=["self"] + enum,
                                   keyable=True)
        attribute.addEnumAttribute(target,
                                   match_attr_name,
                                   value="self",
                                   enum=["self"] + enum,
                                   keyable=True)
        target.attr(match_attr_name).set(keyable=True, lock=False, channelBox=True)
        cns = ctl.getParent().getParent()
        cons = pm.parentConstraint(ik_ref_ctls + [cns], maintainOffset=True)
        attrs = pm.parentConstraint(cons, query=True, weightAliasList=True)
        for index, attr in enumerate(attrs):
            condition = pm.createNode("condition")
            pm.connectAttr(target.attr(attr_name), condition.attr("firstTerm"))
            condition.attr("secondTerm").set(index + 1)
            condition.attr("colorIfTrueR").set(1)
            condition.attr("colorIfFalseR").set(0)
            pm.connectAttr(condition.attr("outColorR"), attr)
        script_code = f"""import pymel.core as pm
import maya.api.OpenMaya as om2
import uuid

oid = '{self.block["oid"]}'

class SpaceSwitch:

    def __init__(self, node):
        self.node = pm.PyNode(node)
        namespace = self.node.namespace()
        split_name = [x for x in '{ctl.fullPath()}'.split('|') if x]
        self.ctl = '|'.join([namespace + x for x in split_name if x])

    def switch(self):
        current_time = pm.currentTime()
        destination_value = self.node.attr('{match_attr_name}').get()
        temp_obj = pm.group(name=str(uuid.uuid4()), empty=True)
        pm.matchTransform(temp_obj, self.ctl, position=True, rotation=True)
        pm.setKeyframe(self.ctl, attribute=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'], time=current_time - 1)
        self.node.attr('{attr_name}').set(destination_value)
        pm.setKeyframe(self.node, attribute='{attr_name}')
        pm.matchTransform(self.ctl, temp_obj, position=True, rotation=True)
        pm.delete(temp_obj)
        pm.setKeyframe(self.ctl, attribute=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])

    def space_switch(self):
        with pm.UndoChunk():
            selected = pm.selected()
            value = self.node.attr('{match_attr_name}').get()
            if value not in {range(len(enum) + 1)}:
                return
            switch_value = self.node.attr('{attr_name}').get()
            if value != switch_value:
                self.switch()
            pm.select(selected)

def cb_run(msg, plug1, plug2, client_data):
    if msg != 2056:
        return
    if plug1.partialName(includeNodeName=False) != '{match_attr_name}':
        return
    client_data.space_switch()

def register_cb(node):
    sel_list = om2.MGlobal.getSelectionListByName(node)
    node_dag = sel_list.getDagPath(0)
    node_obj = sel_list.getDependNode(0)
    node_full_name = node_dag.fullPathName()
    cb_id = om2.MNodeMessage.addAttributeChangedCallback(node_obj,
                                                         cb_run,
                                                         clientData=SpaceSwitch(node))
    return (node_dag, cb_id)

def run_block_script():
    global mbox_character_cb_registry
    global mbox_character_namespace_registry

    all_script_node = [x for x in pm.ls(type='script') if x.hasAttr('oid')]
    mbox_script_node = [x for x in all_script_node if x.attr('oid').get() == oid]

    check = False
    for node in mbox_script_node:
        namespace = node.namespace()
        if namespace:
            namespace = namespace[:-1]
        if namespace not in mbox_character_namespace_registry:
            check = True
            break
    if not check:
        return
    target = node.attr('target').inputs(type='transform')
    if target:
        target = target[0]
        try:
            mbox_character_cb_registry.append(register_cb(target.fullPath()))
        except:
            mbox_character_cb_registry = list()
            mbox_character_cb_registry.append(register_cb(target.fullPath()))

run_block_script()"""
        pm.scriptNode(script_node, edit=True, beforeScript=script_code)
        pm.connectAttr(target.attr("message"), script_node.attr("target"), force=True)


class AbstractConnection(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractConnection, self).__init__(block=block)

    def process(self, context):
        super(AbstractConnection, self).process(context=context)


class AdditionalFunc:

    def __init__(self):
        self.msg = "Process Additional Func"

    def process(self, context):
        logger.info("{0:<50}".format(self.msg + "(clean up)"))
        self.cleanup(context)
        logger.info("{0:<50}".format(self.msg + "(draw controls shape)"))
        self.draw_controls_shape(context)
        logger.info("{0:<50}".format(self.msg + "(script node)"))
        self.script_node(context)
        logger.info("{0:<50}".format(self.msg + "(skinning)"))
        self.skinning(context)
        logger.info("{0:<50}".format(self.msg + "(deformer)"))
        self.deformers(context)

    def cleanup(self, context):
        blueprint = context.blueprint

        # recursive
        def _connect_network(_block):
            _ins = context.instance(_block.ins_name)
            if _ins["root"]:
                pm.connectAttr(_ins["root"].attr("message"), _block.network.attr("rig"), force=True)
            if _block.parent:
                dfs_list = pm.connectionInfo(_block.parent.network.attr("affects")[0], destinationFromSource=True)
                if _block.network.attr("affectedBy")[0].name() not in dfs_list:
                    pm.connectAttr(_block.parent.network.attr("affects")[0],
                                   _block.network.attr("affectedBy")[0], force=True)
            if _ins.get("ctls"):
                for index, con in enumerate(_ins["ctls"]):
                    pm.connectAttr(con.attr("message"), _block.network.attr("ctls")[index], force=True)
            if _ins.get("jnts"):
                for index, jnt in enumerate(_ins["jnts"]):
                    pm.connectAttr(jnt.attr("message"), _block.network.attr("jnts")[index], force=True)
            for _b in _block["blocks"]:
                _connect_network(_b)

        #   ----

        _connect_network(blueprint)

        # recursive
        def _create_set(_block):
            _ins = context.instance(_block.ins_name)
            _top_ins = context.instance(_block.top.ins_name)
            if _ins.get("ctls"):
                pm.sets(_top_ins["controls_set"], addElement=_ins["ctls"])
            if _ins.get("jnts"):
                pm.sets(_top_ins["deformer_set"], addElement=_ins["jnts"])
            for _b in _block["blocks"]:
                _create_set(_b)

        #   ----

        _create_set(blueprint)

        # recursive
        def _cleanup_controls(_block):
            if _block.parent:
                _ins = context.instance(_block.ins_name)
                _parent_block = _block.parent
                while True:
                    _parent_ins = context.instance(_parent_block.ins_name)
                    if _parent_ins["ctls"]:
                        break
                    _parent_block = _parent_block.parent
                for x in _ins["ctls"]:
                    if not pm.controller(x, query=True, parent=True):
                        node.add_controller_tag(x, _parent_ins["ctls"][-1])
            for _b in _block["blocks"]:
                _cleanup_controls(_b)

        #   ----

        _cleanup_controls(blueprint)

        # recursive
        def _cleanup_joints(_block):
            if _block.parent:
                _top_ins = context.instance(_block.top.ins_name)
                _ins = context.instance(_block.ins_name)
                if _ins.get("jnts"):
                    for _index, _jnt in enumerate(_ins["jnts"]):
                        _label = f"{_block['comp_name']}_center{_block['comp_index']}_{_index}" \
                            if _block["comp_side"] == "center" \
                            else f"{_block['comp_name']}_side{_block['comp_index']}_{_index}"

                        _jnt.attr("side").set(side_set[_block["comp_side"]])
                        _jnt.attr("type").set("Other")
                        _jnt.attr("otherType").set(_label)
                        _jnt.attr("radius").set(0.5)
                        _jnt.attr("segmentScaleCompensate").set(False)
                        pm.connectAttr(_top_ins["root"].attr("joints_label_vis"), _jnt.attr("drawLabel"))
            for _b in _block["blocks"]:
                _cleanup_joints(_b)

        #   ----
        side_set = {"center": 0, "left": 1, "right": 2}
        _cleanup_joints(blueprint)

    def draw_controls_shape(self, context):
        blueprint = context.blueprint
        top_ins = context.instance(blueprint.ins_name)
        root = top_ins["root"]
        for member in top_ins["controls_set"].members():
            for index, shape in enumerate(member.getShapes()):
                shape.rename(f"temp{index}")
            for index, shape in enumerate(member.getShapes()):
                shape.rename(f"{shape.getParent().nodeName()}{index if index else str()}Shape")
                shape.attr("isHistoricallyInteresting").set(0)
                pm.connectAttr(root.attr("controls_x_ray"), shape.attr("alwaysDrawOnTop"))

    def script_node(self, context):
        blueprint = context.blueprint
        if blueprint.network.attr("script_node").outputs():
            root_script_node = blueprint.network.attr("script_node").outputs()[0]
            block_script_node = root_script_node.attr("script_node").outputs()
            pm.delete([root_script_node] + block_script_node)

        script_nodes = list()

        def _get_script_node(_block):
            nonlocal script_nodes
            _ins = context.instance(_block.ins_name)
            if _ins.get("script_node"):
                script_nodes += _ins.get("script_node")
            for __b in _block["blocks"]:
                _get_script_node(__b)

        _get_script_node(blueprint)

        if not script_nodes:
            return
        root_script_node = pm.createNode("script", name="mbox_sc")
        root_script_node.attr("sourceType").set(1)
        root_script_node.attr("scriptType").set(1)
        attribute.addAttribute(root_script_node, "script_node", "message")
        for node in script_nodes:
            pm.connectAttr(root_script_node.attr("script_node"), node.attr("script_node"))
        pm.connectAttr(blueprint.network.attr("script_node"), root_script_node.attr("script_node"))
        before_script_code = f"""import pymel.core as pm
import maya.api.OpenMaya as om2
import traceback
import logging

logger = logging.getLogger()

def destory_cb(*args): # all callback clear
    global mbox_destory_new_id
    global mbox_destory_open_id
    global mbox_destory_remove_ref_id
    global mbox_destory_unload_ref_id
    global mbox_character_cb_registry
    global mbox_character_namespace_registry
    logger.info("destory_cb")

    try:
        for array in mbox_character_cb_registry:
            om2.MNodeMessage.removeCallback(array[1])
        om2.MSceneMessage.removeCallback(mbox_destory_new_id)
        om2.MSceneMessage.removeCallback(mbox_destory_open_id)
        om2.MSceneMessage.removeCallback(mbox_destory_remove_ref_id)
        om2.MSceneMessage.removeCallback(mbox_destory_unload_ref_id)
        del mbox_character_cb_registry
        del mbox_character_namespace_registry
        del mbox_destory_new_id
        del mbox_destory_open_id
        del mbox_destory_remove_ref_id
        del mbox_destory_unload_ref_id
    except:
        logger.error("destory_cb")
        traceback.print_exc()


def refresh_registry(*argc): # refresh registry at reference unload, remove
    global mbox_character_cb_registry
    global mbox_character_namespace_registry

    remove_list = list()
    for ns in mbox_character_namespace_registry:
        if not pm.namespaceInfo(ns, listNamespace=True):
            remove_list.append(ns)
    for rm in remove_list:
        mbox_character_namespace_registry.remove(rm)

    for array in mbox_character_cb_registry:
        if array[0].fullPathName == "":
            om2.MNodeMessage.removeCallback(array[1])
    mbox_character_cb_registry = [x for x in mbox_character_cb_registry if x[0].fullPathName() != ""]


def run_script_node():
    global mbox_destory_id
    global mbox_character_cb_registry
    global mbox_character_namespace_registry

    try:
        mbox_character_namespace_registry
    except:
        mbox_character_namespace_registry = list()

    oid = '{blueprint["oid"]}'
    all_network = [network for network in pm.ls(type="network") if network.hasAttr("oid")]
    networks = [network for network in all_network if network.attr("oid").get() == oid]
    namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    if "" in mbox_character_namespace_registry:
        mbox_character_namespace_registry.remove("")
    if not networks:
        return
    for network in networks:
        this_node = network.attr("script_node").outputs(type="script")
        namespace = network.namespace()
        if namespace:
            namespace = namespace[:-1]
        if this_node and namespace not in mbox_character_namespace_registry:
            block_scripts = this_node[0].attr("script_node").outputs(type="script")
            for sn in block_scripts:
                pm.scriptNode(sn, executeBefore=True)
            mbox_character_namespace_registry.append(namespace)

run_script_node()

try:
    om2.MSceneMessage.removeCallback(mbox_destory_new_id)
except:
    pass
finally:
    mbox_destory_new_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterNew, destory_cb)
try:
    om2.MSceneMessage.removeCallback(mbox_destory_open_id)
except:
    pass
finally:
    mbox_destory_open_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterOpen, destory_cb)
try:
    om2.MSceneMessage.removeCallback(mbox_destory_remove_ref_id)
except:
    pass
finally:
    mbox_destory_remove_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterRemoveReference, refresh_registry)
try:
    om2.MSceneMessage.removeCallback(mbox_destory_unload_ref_id)
except:
    pass
finally:
    mbox_destory_unload_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterUnloadReference, refresh_registry)"""
        pm.scriptNode(root_script_node, edit=True, beforeScript=before_script_code)
        pm.scriptNode(root_script_node, executeBefore=True)

    def skinning(self, context):
        pass

    def deformers(self, context):
        pass


class PostScript:

    def __init__(self):
        self.msg = f"Process {self.__module__}.{self.__class__}"
