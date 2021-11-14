# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
import mbox
from mbox.core.attribute import add_attribute
from mbox.lego import utils

#
import uuid
import os
import logging
from collections import OrderedDict
import itertools

# mgear
from mgear.core import pyqt, attribute, primitive, transform

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
    else:
        raise RuntimeError

    return blueprint_from_network(hierarchy)


def blueprint_from_network(hierarchy):
    def get_blueprint(_p_block, _network, children):
        mod = utils.load_block_module(_network.attr("component").get(), guide=True)
        block = mod.Block(parent=_p_block)
        block.network = _network
        if children:
            for _key, _value in children.items():
                get_blueprint(block, _key, _value)

    network = next(itertools.islice(hierarchy.keys(), 1))
    blueprint = TopBlock()
    blueprint.network = network

    for key, value in hierarchy[network].items():
        get_blueprint(blueprint, key, value)

    blueprint.from_network()
    return blueprint


def blueprint_from_rig():
    rig_root = pm.selected(type="transform")[0].getParent(generations=-1)
    if not rig_root.hasAttr("is_rig_root"):
        raise RuntimeError("you don't select mbox rig")
    root_network = rig_root.message.outputs(type="network")[0]

    hierarchy = get_hierarchy_from_network(root_network, OrderedDict())
    return blueprint_from_network(hierarchy)


def blueprint_from_file(path):
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

    def get_blueprint(_block, _data):
        for child in _data["blocks"]:
            mod = utils.load_block_module(child["component"], guide=True)
            _b = mod.Block(_block)
            get_blueprint(_b, child)

    blueprint = TopBlock()
    get_blueprint(blueprint, data)
    blueprint.update(data)
    return blueprint


def draw_specify_component_guide(parent, component):
    if not parent:
        # root block
        blueprint = TopBlock()

        # component block
        mod = utils.load_block_module(component, guide=True)
        block = mod.Block(parent=blueprint)

        blueprint.guide()
    else:
        parent = get_component_guide(parent)[0]

        blueprint = blueprint_from_guide(parent.getParent(generations=-1))
        mod = utils.load_block_module(component, guide=True)

        if parent.hasAttr("is_guide_root"):
            block = mod.Block(blueprint)
        else:
            parent_network = parent.message.outputs(type="network")[0]
            parent_block = blueprint.find_block_with_oid(parent_network.attr("oid").get())
            block = mod.Block(parent_block)

            # translation offset
            offset_t = parent.getTranslation(space="world")
            for index, t in enumerate(block["transforms"]):
                block["transforms"][index] = transform.setMatrixPosition(t, offset_t)

        block["index"] = blueprint.valid_index(block["name"], block["direction"])
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
            comp_type = network.attr("component").get()
            break
        elif pm.attributeQuery("is_guide_root", node=root, exists=True):
            guide_root = root
            break
        root = root.getParent()

    if comp_type:
        mod = utils.load_block_module(comp_type, guide=True)
        window = pyqt.showDialog(mod.BlockSettings, dockable=True)
        window.tabs.setCurrentIndex(0)
        window.guide = guide
        window.network = network

    elif guide_root:
        module_name = "mbox.lego.box.settings"
        mod = __import__(module_name, globals(), locals(), ["*"], 0)
        window = pyqt.showDialog(mod.RootSettings, dockable=True)
        window.tabs.setCurrentIndex(0)
        window.guide = guide
        window.network = network

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


def export_blueprint(node, path):
    """blueprint json file export"""
    if not path:
        path = _file_dialog(path, mode=0)
        if not path:
            pm.displayWarning("File path None")
            return
    if not node:
        try:
            selected = pm.selected(type="transform")[0]
            if not selected.hasAttr("is_guide_root"):
                raise RuntimeError("select mbox root guide")
        except IndexError as e:
            pm.displayWarning(e)
            return
        except RuntimeError as e:
            pm.displayWarning(e)
            return
    else:
        selected = node

    root_block = blueprint_from_guide(selected)
    root_block.save(root_block, path)


def import_blueprint(path, draw=True):
    """blueprint json file import"""
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


class AbstractBlock(dict):

    def __init__(self, parent=None):
        self._network = None
        self._parent = parent
        if self._parent:
            self._parent["blocks"].append(self)
        self["oid"] = str(uuid.uuid4())
        self["blocks"] = _List()
        self.attributes = list()

    def __setitem__(self, key, value):
        if key == "blocks":
            assert isinstance(value, _List)
        super().__setitem__(key, value)

    def update(self, _d, **kwargs):
        for key, value in kwargs.items():
            _d[key] = value

        def __recursive(_block, _dict):
            for k, v in _dict.items():
                if k == "blocks":
                    continue
                _block[k] = v

            for index, b_data in enumerate(_dict["blocks"]):
                mod = utils.load_block_module(b_data["component"], guide=True)
                _block["blocks"].append(mod.Block(_block))
                __recursive(_block["blocks"][index], b_data)

        __recursive(self, _d)

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

    def from_network(self):

        def __recursive(_block):
            _block.from_network()

            for _b in _block["blocks"]:
                __recursive(_b)

        for block in self["blocks"]:
            __recursive(block)

    def to_network(self):

        def __recursive(_block):
            _block.to_netwrok()

            for _b in _block["blocks"]:
                __recursive(_b)

        for block in self["blocks"]:
            __recursive(block)

    def guide(self):

        def __recursive(_block):
            root = _block.guide()

            if not _block["blocks"]:
                return root

            for _b in _block["blocks"]:
                return __recursive(_b)

        node = None
        for block in self["blocks"]:
            node = __recursive(block)

        return node


class TopBlock(AbstractBlock):

    def __init__(self):
        super(TopBlock, self).__init__(parent=None)

        # component
        self["component"] = "mbox"

        # version
        self["version"] = mbox.version.mbox

        # WIP or PUB
        self["process"] = "WIP"

        # "all", "preScripts", "objects", "attributes", "operators", "connection", "additionalFunc", "postScripts"
        self["step"] = "all"

        # Asset name
        self["name"] = "rig"

        # Direction string
        self["joint_direction"] = ["C", "L", "R"]
        self["controls_direction"] = ["C", "L", "R"]

        # Extension
        self["joint_extension"] = "jnt"
        self["controls_extension"] = "con"

        # Convention
        self["joint_convention"] = "{name}_{direction}{index}_{description}_{extension}"
        self["controls_convention"] = "{name}_{direction}{index}_{description}_{extension}"

        # default, lower, upper, capitalize
        self["joint_description_letter_case"] = "default"
        self["controls_description_letter_case"] = "default"

        # padding
        self["joint_padding"] = 0
        self["controls_padding"] = 0

        # bool
        self["run_scripts"] = False

        # Scripts path
        self["scripts"] = list()

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
        self["l_RGB_fk"] = [0, 0, 1]
        self["l_RGB_ik"] = [0, 0.25, 1]
        self["r_RGB_fk"] = [1, 0, 0]
        self["r_RGB_ik"] = [1, 0.1, 0.25]
        self["c_RGB_fk"] = [1, 1, 0]
        self["c_RGB_ik"] = [0, 0.6, 0]

        # notes
        self["notes"] = ""

    @property
    def ins_name(self):
        return f"{self['component']}"

    def control_name(self, name="", direction="", index="", description="", extension=""):
        index = str(index).zfill(self["controls_padding"])
        if self["controls_description_letter_case"] == "lower":
            description = description.lower()
        elif self["controls_description_letter_case"] == "upper":
            description = description.upper()
        elif self["controls_description_letter_case"] == "capitalize":
            description = description.capitalize()
        rename = self["controls_convention"].format(
            name=name, direction=direction, index=index, description=description, extension=extension)
        c_name = "_".join([x for x in rename.split("_") if x])
        return c_name

    def joint_name(self, name="", direction="", index="", description="", extension=""):
        index = str(index).zfill(self["joints_padding"])
        if self["joint_description_letter_case"] == "lower":
            description = description.lower()
        elif self["joint_description_letter_case"] == "upper":
            description = description.upper()
        elif self["joint_description_letter_case"] == "capitalize":
            description = description.capitalize()
        rename = self["joints_convention"].format(
            name=name, direction=direction, index=index, description=description, extension=extension)
        j_name = "_".join([x for x in rename.split("_") if x])
        return j_name

    def from_network(self):
        self["oid"] = self.network.attr("oid").get()
        self["name"] = self.network.attr("name").get()
        self["version"] = self.network.attr("version").get()
        self["schema"] = self.network.attr("schema").get()
        self["process"] = self.network.attr("process").get(asString=True)
        self["step"] = self.network.attr("step").get(asString=True)
        self["joint_direction"] = self.network.attr("joint_direction").get()
        self["controls_direction"] = self.network.attr("controls_direction").get()
        self["joint_extension"] = self.network.attr("joint_extension").get()
        self["controls_extension"] = self.network.attr("controls_extension").get()
        self["joint_convention"] = self.network.attr("joint_convention").get()
        self["controls_convention"] = self.network.attr("controls_convention").get()
        self["joint_description_letter_case"] = self.network.attr("joint_description_letter_case").get(asString=True)
        self["controls_description_letter_case"] = \
            self.network.attr("controls_description_letter_case").get(asString=True)
        self["joint_padding"] = self.network.attr("joint_padding").get()
        self["controls_padding"] = self.network.attr("controls_padding").get()
        self["run_scripts"] = self.network.attr("run_scripts").get()
        self["scripts"] = self.network.attr("scripts").get()
        self["l_color_fk"] = self.network.attr("l_color_fk").get()
        self["l_color_ik"] = self.network.attr("l_color_ik").get()
        self["r_color_fk"] = self.network.attr("r_color_fk").get()
        self["r_color_ik"] = self.network.attr("r_color_ik").get()
        self["c_color_fk"] = self.network.attr("c_color_fk").get()
        self["c_color_ik"] = self.network.attr("c_color_ik").get()
        self["use_RGB_Color"] = self.network.attr("use_RGB_Color").get()
        self["l_RGB_fk"] = self.network.attr("l_RGB_fk").get()
        self["l_RGB_ik"] = self.network.attr("l_RGB_ik").get()
        self["r_RGB_fk"] = self.network.attr("r_RGB_fk").get()
        self["r_RGB_ik"] = self.network.attr("r_RGB_ik").get()
        self["c_RGB_fk"] = self.network.attr("c_RGB_fk").get()
        self["c_RGB_ik"] = self.network.attr("c_RGB_ik").get()
        self["notes"] = self.network.attr("notes").get()

        super(TopBlock, self).from_network()

    def to_network(self):
        self.network.attr("oid").set(self["oid"])
        self.network.attr("name").set(self["name"])
        self.network.attr("version").set(self["version"])
        self.network.attr("schema").set(self["schema"])
        self.network.attr("process").set(self["process"])
        self.network.attr("step").set(self["step"])
        [self.network.attr("joint_direction")[i].set(x) for i, x in enumerate(self["joint_direction"])]
        [self.network.attr("controls_direction")[i].set(x) for i, x in enumerate(self["controls_direction"])]
        self.network.attr("joint_extension").set(self["joint_extension"])
        self.network.attr("controls_extension").set(self["controls_extension"])
        self.network.attr("joint_convention").set(self["joint_convention"])
        self.network.attr("controls_convention").set(self["controls_convention"])
        self.network.attr("joint_description_letter_case").set(self["joint_description_letter_case"])
        self.network.attr("controls_description_letter_case").set(self["controls_description_letter_case"])
        self.network.attr("joint_padding").set(self["joint_padding"])
        self.network.attr("controls_padding").set(self["controls_padding"])
        self.network.attr("run_scripts").set(self["run_scripts"])
        [self.network.attr("scripts")[i].set(script) for i, script in enumerate(self["scripts"])]
        self.network.attr("l_color_fk").set(self["l_color_fk"])
        self.network.attr("l_color_ik").set(self["l_color_ik"])
        self.network.attr("r_color_fk").set(self["r_color_fk"])
        self.network.attr("r_color_ik").set(self["r_color_ik"])
        self.network.attr("c_color_fk").set(self["c_color_fk"])
        self.network.attr("c_color_ik").set(self["c_color_ik"])
        self.network.attr("use_RGB_Color").set(self["use_RGB_Color"])
        self.network.attr("l_RGB_fk").set(self["l_RGB_fk"])
        self.network.attr("l_RGB_ik").set(self["l_RGB_ik"])
        self.network.attr("r_RGB_fk").set(self["r_RGB_fk"])
        self.network.attr("r_RGB_ik").set(self["r_RGB_ik"])
        self.network.attr("c_RGB_fk").set(self["c_RGB_fk"])
        self.network.attr("c_RGB_ik").set(self["c_RGB_ik"])
        self.network.attr("notes").set(self["notes"])

        super(TopBlock, self).to_network()

    def guide(self):
        self.network = pm.createNode("network")
        n = self.network
        attribute.addAttribute(n, "oid", "string", self["oid"])
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "component", "string", self["component"])
        attribute.addAttribute(n, "name", "string", self["name"])
        attribute.addAttribute(n, "version", "string", self["version"])
        attribute.addAttribute(n, "schema", "string", self["schema"])
        attribute.addEnumAttribute(n, "process", self["process"], ["WIP", "PUB"], keyable=False)
        attribute.addEnumAttribute(n, "step", self["step"],
                                   ["all", "preScripts", "objects", "attributes", "operators", "connection",
                                    "additionalFunc", "postScripts"], keyable=False)
        add_attribute(n, "joint_direction", "string", multi=True)
        add_attribute(n, "controls_direction", "string", multi=True)
        [n.attr("joint_direction")[i].set(direction) for i, direction in enumerate(self["joint_direction"])]
        [n.attr("controls_direction")[i].set(direction) for i, direction in enumerate(self["controls_direction"])]
        attribute.addAttribute(n, "joint_extension", "string", self["joint_extension"])
        attribute.addAttribute(n, "controls_extension", "string", self["controls_extension"])
        attribute.addAttribute(n, "joint_convention", "string", self["joint_convention"])
        attribute.addAttribute(n, "controls_convention", "string", self["controls_convention"])
        attribute.addEnumAttribute(n, "joint_description_letter_case", self["joint_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addEnumAttribute(n, "controls_description_letter_case", self["controls_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addAttribute(n, "joint_padding", "long", self["joint_padding"], keyable=False)
        attribute.addAttribute(n, "controls_padding", "long", self["controls_padding"], keyable=False)
        attribute.addAttribute(n, "run_scripts", "bool", self["run_scripts"], keyable=False)
        add_attribute(n, "scripts", "string", multi=True)
        [n.attr("scripts")[index].set(script) for index, script in enumerate(self["scripts"])]
        attribute.addAttribute(n, "l_color_fk", "long", self["l_color_fk"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "l_color_ik", "long", self["l_color_ik"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "r_color_fk", "long", self["r_color_fk"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "r_color_ik", "long", self["r_color_ik"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "c_color_fk", "long", self["c_color_fk"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "c_color_ik", "long", self["c_color_ik"], minValue=0, maxValue=31)
        attribute.addAttribute(n, "use_RGB_Color", "bool", self["use_RGB_color"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_fk", self["l_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_ik", self["l_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_fk", self["r_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_ik", self["r_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_fk", self["c_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_ik", self["c_RGB_ik"], keyable=False)
        attribute.addAttribute(n, "notes", "string", str(self["notes"]))

        guide = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())

        # attribute
        attribute.lockAttribute(guide)
        attribute.setKeyableAttributes(guide, list())
        attribute.addAttribute(guide, "is_guide_root", "bool", keyable=False)

        # connection
        pm.connectAttr(guide.message, n.guide, force=True)

        sel = super(TopBlock, self).guide()
        pm.select(sel)

    def find_block_with_oid(self, oid):

        def __find(_block, _oid):
            if _block["oid"] == _oid:
                return _block

            for _b in _block["blocks"]:
                __b = __find(_b, _oid)
                if __b:
                    return __b

        return __find(self, oid)

    def find_block_with_ins_name(self, ins_name):

        def __find(_block, _ins_name):
            if _block.ins_name == _ins_name:
                return _block

            for _b in _block["blocks"]:
                __b = __find(_b, _ins_name)
                if __b:
                    return __b

        return __find(self, ins_name)

    def valid_index(self, name, direction):
        indexes = list()

        def __index(_block, _indexes, _name, _direction):
            if _block["name"] == _name and _block["direction"] == _direction:
                _indexes.append(_block["index"])

            for _b in _block["blocks"]:
                __index(_b, _indexes, _name, _direction)

        for block in self["blocks"]:
            __index(block, indexes, name, direction)

        number = 0
        while True:
            if number not in indexes:
                break
            number += 1
        return number


class SubBlock(AbstractBlock):

    def __init__(self, parent=None):
        super(SubBlock, self).__init__(parent=parent)

        # what kind of box
        self["component"] = None

        # block version
        self["version"] = None

        # module name # arm... leg... spine...
        self["name"] = None

        # "center", "left", "right"
        self["direction"] = "center"

        # index
        self["index"] = 0

        # True - create joint / False
        self["joint_rig"] = True

        # primary axis, secondary axis, offset XYZ
        # self["joint_settings"] = [["x", "y", (0, 0, 0)], ]

        # guide transform matrix list
        # self["transforms"] = list()

        # parent node name
        self["controls_ref_index"] = -1
        self["joint_ref_index"] = -1

    @property
    def ins_name(self):
        return f"{self['name']}.{self['direction']}.{self['index']}"

    def from_network(self):
        self["oid"] = self.network.attr("oid").get()
        self["component"] = self.network.attr("component").get()
        self["version"] = self.network.attr("version").get()
        self["name"] = self.network.attr("name").get()
        self["direction"] = self.network.attr("direction").get(asString=True)
        self["index"] = self.network.attr("index").get()
        self["joint_rig"] = self.network.attr("joint_rig").get()
        self["joint_settings"] = zip([x for x in self.network.attr("primary_axis").get()],
                                     [x for x in self.network.attr("secondary_axis").get()],
                                     [x for x in self.network.attr("offset_XYZ").get()])
        self["transforms"] = [x.tolist() for x in self.network.attr("transforms").get()]
        self["controls_ref_index"] = self.network.attr("controls_ref_index").get()
        self["joint_ref_index"] = self.network.attr("joint_ref_index").get()

    def to_network(self):
        self.network.attr("oid").set(self["oid"])
        self.network.attr("component").set(self["component"])
        self.network.attr("version").set(self["version"])
        self.network.attr("name").set(self["name"])
        self.network.attr("direction").set(self["direction"])
        self.network.attr("index").set(self["index"])
        self.network.attr("joint_rig").set(self["joint_rig"])
        [self.network.attr("primary_axis")[i].set(settings[0]) for i, settings in enumerate(self["joint_settings"])]
        [self.network.attr("secondary_axis")[i].set(settings[1]) for i, settings in enumerate(self["joint_settings"])]
        [self.network.attr("offset_XYZ")[i].set(settings[2]) for i, settings in enumerate(self["joint_settings"])]
        [self.network.attr("transforms")[i].set(t) for i, t in enumerate(self["transforms"])]
        self.network.attr("controls_ref_index").set(self["controls_ref_index"])
        self.network.attr("joint_ref_index").set(self["joint_ref_index"])

    def guide(self):
        self.network = pm.createNode("network")
        n = self.network
        attribute.addAttribute(n, "oid", "string", self["oid"])
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "component", "string", self["component"])
        attribute.addAttribute(n, "name", "string", self["name"])
        attribute.addAttribute(n, "version", "string", self["version"])
        attribute.addEnumAttribute(n, "direction", self["direction"], ["center", "left", "right"], keyable=False)
        attribute.addAttribute(n, "index", "long", self["index"], keyable=False)
        attribute.addAttribute(n, "joint_rig", "bool", self["joint_rig"], keyable=False)
        add_attribute(n, "primary_axis", "string", multi=True)
        add_attribute(n, "secondary_axis", "string", multi=True)
        n.addAttr("offset_XYZ", type="double3", multi=True, keyable=False)
        add_attribute(n, "transforms", "matrix", multi=True)
        attribute.addAttribute(n, "controls_ref_index", "long", self["controls_ref_index"], keyable=False)
        attribute.addAttribute(n, "joint_ref_index", "long", self["joint_ref_index"], keyable=False)
        add_attribute(n, "controls", "message", multi=True)
        add_attribute(n, "joints", "message", multi=True)


class Context(list):

    def instance(self, name):
        for ins in self:
            if name == ins.name:
                return ins
        ins = Instance(name)
        self.append(ins)
        return ins


class Instance(dict):

    def __init__(self, name):
        assert isinstance(name, str)

        self._name = name

    def __repr__(self):
        return f"ins(\"{self.name}\")"

    @property
    def name(self):
        return self._name


class PreScripts:
    order = 0

    def __init__(self):
        self.msg = f"Process {self.__module__}.{self.__class__}"


class AbstractRig:

    def __init__(self, block):
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


class AbstractAttributes(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractAttributes, self).__init__(block=block)


class AbstractOperators(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractRig)
        super(AbstractOperators, self).__init__(block=block)


class AbstractConnection(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractConnection, self).__init__(block=block)


class AdditionalFunc:

    def __init__(self, blueprint):
        self.msg = "Process Additional Func"
        self.blueprint = blueprint

    def process(self, context):
        self.cleanup(context)
        self.draw_controls_shape(context)
        self.skinning(context)
        self.deformers(context)

    def cleanup(self, context):

        def __network(_block):
            _ins = context.instance(_block.ins_name)
            pm.connectAttr(_ins["root"].attr("message"), _block.network.attr("rig"))
            if _block.parent:
                pm.connectAttr(_block.parent.network.attr("affects")[0], _block.network.attr("affectedBy")[0])
            if _ins.get("controls"):
                for index, con in enumerate(_ins["controls"]):
                    pm.connectAttr(con.attr("message"), _block.network.attr("controls")[index])
            if _ins.get("joints"):
                for index, jnt in enumerate(_ins["joints"]):
                    pm.connectAttr(jnt.attr("message"), _block.network.attr("joints")[index])
            for _b in _block["blocks"]:
                __controller(_b)

        __network(self.blueprint)

        def __set(_block):
            _ins = context.instance(_block.ins_name)
            _top_ins = context.instance(_block.top.ins_name)
            if _ins.get("controls") is not None:
                pm.sets(_top_ins["controller_set"], addElement=_ins["controls"])
            if _ins.get("joints") is not None:
                pm.sets(_top_ins["deformer_set"], addElement=_ins["joints"])
            for _b in _block["blocks"]:
                __set(_b)

        __set(self.blueprint)

        def __controller(_block):
            if _block.parent:
                _ins = context.instance(_block.ins_name)
                _parent_ins = context.instance(_block.parent.ins_name)
                pm.controller([x for x in _ins["controls"] if pm.controller(x, query=True, parent=True)],
                              _parent_ins["controls"][-1], parent=True)
            for _b in _block["blocks"]:
                __controller(_b)

        __controller(self.blueprint)

        def __joints(_block):
            if _block.parent:
                _top_ins = context.instance(_block.top.ins_name)
                _ins = context.instance(_block.ins_name)
                if _ins.get("joints"):
                    _convention = _block.top["joint_convention"].split("_")
                    _description_index = None
                    for _i, _c in enumerate(_convention.split("_")):
                        if "description" in _c:
                            _description_index = _i
                    for _jnt in _ins["joints"]:
                        _description = _jnt.split("_")[_description_index]
                        _label = f"{_block['name']}_{_block['index']}_{_description}"
                        _jnt.attr("side").set(_block["direction"])
                        _jnt.attr("type").set("Other")
                        _jnt.attr("otherType").set(_label)
                        _jnt.attr("radius").set(0.5)
                        pm.connectAttr(_top_ins["root"].attr("joints_label_vis"), _jnt.attr("drawLabel"))
            for _b in _block["blocks"]:
                __joints(_b)

        __joints(self.blueprint)

    def draw_controls_shape(self, context):
        pass

    def support_joint(self, context):
        pass

    def skinning(self, context):
        pass

    def deformers(self, context):
        pass


class PostScripts:
    order = 0

    def __init__(self):
        self.msg = f"Process {self.__module__}.{self.__class__}"
