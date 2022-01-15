# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
import mbox
from mbox.lego import (
    utils,
    naming
)

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
    node,
)

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
        comp_index = blueprint.solve_index(mod.NAME, "center")

        parent_network = parent.message.outputs(type="network")[0]
        parent_block = blueprint.find_block_with_oid(parent_network.attr("oid").get())
        block = mod.Block(parent_block)
        block["comp_index"] = comp_index

        # translation offset
        offset_t = parent.getTranslation(space="world")
        for index, t in enumerate(block["transforms"]):
            block["transforms"][index] = transform.setMatrixPosition(t, offset_t)

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
        self.attributes = list()

    def __setitem__(self, key, value):
        if key == "blocks":
            assert isinstance(value, _List)
        super().__setitem__(key, value)

    def update(self, _d, **kwargs):
        # recursive
        def _update(_block, _dict):
            for k, v in _dict.items():
                if k == "blocks":
                    continue
                _block[k] = v

            for index, b_data in enumerate(_dict["blocks"]):
                mod = utils.load_block_module(b_data["comp_type"], guide=True)
                _block["blocks"].append(mod.Block(_block))
                _update(_block["blocks"][index], b_data)

        #   ----

        for key, value in kwargs.items():
            _d[key] = value

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
            return f"{self['comp_name']}.{self['comp_side']}.{self['comp_index']}"

    @property
    def negate(self):
        return True if {self['comp_side']} == "right" else False

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

    def get_name(self,
                 typ: bool,
                 description: str = "",
                 extension: str = "") -> str:
        root_block = self.top
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
        side = side_set[index_filter.index(self["comp_side"])]
        name = rule.format(name=self["comp_name"],
                           side=side,
                           index=str(self["comp_index"]).zfill(padding),
                           description=description,
                           extension=extension)
        name = "_".join([x for x in name.split("_") if x])
        return name

    def get_ctl_color(self, ik_fk):
        color = None
        if self["override_color"]:
            if self["use_RGB_color"]:
                if ik_fk == "ik":
                    color = self["RGB_ik"]
                else:
                    color = self["RGB_fk"]
            else:
                if ik_fk == "ik":
                    color = self["color_ik"]
                else:
                    color = self["RGB_fk"]
        else:
            if self.top["use_RGB_color"]:
                if self["comp_side"] == "left":
                    if ik_fk == "ik":
                        color = self.top["l_RGB_ik"]
                    else:
                        color = self.top["l_RGB_fk"]
                elif self["comp_side"] == "right":
                    if ik_fk == "ik":
                        color = self.top["r_RGB_ik"]
                    else:
                        color = self.top["r_RGB_fk"]
                elif self["comp_side"] == "center":
                    if ik_fk == "ik":
                        color = self.top["c_RGB_ik"]
                    else:
                        color = self.top["c_RGB_fk"]
            else:
                if self["comp_side"] == "left":
                    if ik_fk == "ik":
                        color = self.top["l_color_ik"]
                    else:
                        color = self.top["l_color_fk"]
                elif self["comp_side"] == "right":
                    if ik_fk == "ik":
                        color = self.top["r_color_ik"]
                    else:
                        color = self.top["r_color_fk"]
                elif self["comp_side"] == "center":
                    if ik_fk == "ik":
                        color = self.top["c_color_ik"]
                    else:
                        color = self.top["c_color_fk"]
        return color

    def create_root(self,
                    context: Context,
                    m: pm.datatypes.Matrix) -> pm.nodetypes.Transform:
        instance = context.instance(self.ins_name)
        parent_instance = context.instance(self.parent.ins_name)
        parent = parent_instance["refs"][0] \
            if isinstance(self.parent, RootBlock) \
            else parent_instance["refs"][self["ref_index"]]
        root = primitive.addTransform(parent, self.get_name(False, extension="root"), m=m)
        attribute.setNotKeyableAttributes(root)

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
                   shape: str = "cube") -> pm.nodetypes.Transform:
        instance = context.instance(self.ins_name)
        npo = primitive.addTransform(parent, self.get_name(False, description=description, extension="npo"), m=m)
        ctl = icon.create(npo,
                          self.get_name(False, description=description, extension=self.top["ctl_name_ext"]),
                          m=m,
                          color=color,
                          icon=shape,
                          w=size,
                          h=size,
                          d=size)
        attribute.setKeyableAttributes(ctl, ctl_attr)
        attribute.setKeyableAttributes(npo, npo_attr)

        pm.controller(ctl)
        tag = pm.PyNode(pm.controller(ctl, query=True)[0])
        top_instance = context.instance(self.top.ins_name)
        condition = top_instance["root"].attr("controls_mouseover").outputs(type="condition")[0]
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))

        if parent_ctl:
            node.add_controller_tag(ctl, parent_ctl)
        instance["ctls"].append(ctl)
        return ctl

    def create_ref(self,
                   context: Context,
                   parent: None or pm.nodetypes.Transform,
                   description: str,
                   m: pm.datatypes.Matrix) -> pm.nodetypes.Transform:
        instance = context.instance(self.ins_name)
        ref = primitive.addTransform(parent, self.get_name(False, description=description, extension="ref"), m=m)
        attribute.setKeyableAttributes(ref, [])

        instance["refs"].append(ref)
        return ref

    def create_jnt(self,
                   context: Context,
                   parent: pm.nodetypes.Transform or pm.nodetypes.Joint,
                   description: str,
                   ref: pm.nodetypes.Transform) -> pm.nodetypes.Joint:
        instance = context.instance(self.ins_name)

        joint_name = self["joint_names"].split(",")[len(instance["jnts"])]
        name = joint_name \
            if joint_name \
            else self.get_name(True, description=description, extension=self.top["joint_name_ext"])

        if self.top["connect_joints"] and pm.objExists(name):
            jnt = pm.PyNode(name)
            attribute.setKeyableAttributes(ref)
            attribute.setRotOrder(ref, jnt.attr("rotateOrder").get(asString=True).upper())
            pm.matchTransform(ref, jnt, position=True, rotation=True, scale=True)
            attribute.setKeyableAttributes(ref, [])
        else:
            jnt = primitive.addJoint(parent, name, ref.getMatrix(worldSpace=True))

        if isinstance(ref, pm.datatypes.Matrix):
            jnt.setMatrix(ref, worldSpace=True)
            jnt.attr("jointOrientX").set(jnt.attr("rx").get())
            jnt.attr("jointOrientY").set(jnt.attr("ry").get())
            jnt.attr("jointOrientZ").set(jnt.attr("rz").get())
        m_m = node.createMultMatrixNode(ref.attr("worldMatrix"), jnt.attr("parentInverseMatrix"))
        d_m = node.createDecomposeMatrixNode(m_m.attr("matrixSum"))

        i_m = m_m.attr("matrixSum").get().inverse()

        pm.connectAttr(d_m.attr("outputTranslate"), jnt.attr("t"), force=True)
        pm.connectAttr(d_m.attr("outputRotate"), jnt.attr("r"), force=True)
        pm.connectAttr(d_m.attr("outputScale"), jnt.attr("s"), force=True)

        jnt.attr("jointOrientX").set(jnt.attr("rx").get())
        jnt.attr("jointOrientY").set(jnt.attr("ry").get())
        jnt.attr("jointOrientZ").set(jnt.attr("rz").get())

        m_m2 = node.createMultMatrixNode(m_m.attr("matrixSum"), i_m)
        m_m2.attr("matrixIn[2]").set(m_m2.attr("matrixSum").get().inverse())
        d_m2 = node.createDecomposeMatrixNode(m_m2.attr("matrixSum"))

        pm.connectAttr(d_m2.attr("outputRotate"), jnt.attr("r"), force=True)
        attribute.lockAttribute(jnt)
        attribute.setNotKeyableAttributes(jnt, ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"])
        instance["jnts"].append(jnt)
        return jnt


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
        self["notes"] = ""

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

        guide = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())

        # attribute
        attribute.lockAttribute(guide)
        attribute.setKeyableAttributes(guide, list())
        attribute.addAttribute(guide, "is_guide_root", "bool", keyable=False)

        # connection
        pm.connectAttr(guide.attr("message"), n.attr("guide"), force=True)

        # recursive block
        sel = super(RootBlock, self).guide()

        # last created block select
        pm.select(sel)

    def find_block_with_oid(self, oid) -> SubBlock or None:
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
        for block in self["blocks"]:
            sub_block = _find(block, oid)

            if sub_block:
                break

        return sub_block

    def find_block_with_ins_name(self, ins_name) -> SubBlock or None:
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
                if _block != target_block:
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


class AbstractAttributes(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractAttributes, self).__init__(block=block)


class AbstractOperators(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractOperators, self).__init__(block=block)


class AbstractConnection(AbstractRig):

    def __init__(self, block):
        assert issubclass(type(block), AbstractBlock)
        super(AbstractConnection, self).__init__(block=block)


class AdditionalFunc:

    def __init__(self):
        self.msg = "Process Additional Func"

    def process(self, context):
        self.cleanup(context)
        self.draw_controls_shape(context)
        self.skinning(context)
        self.deformers(context)

    def cleanup(self, context):
        blueprint = context.blueprint

        # recursive
        def _connect_network(_block):
            _ins = context.instance(_block.ins_name)
            pm.connectAttr(_ins["root"].attr("message"), _block.network.attr("rig"), force=True)
            if _block.parent:
                pm.connectAttr(_block.parent.network.attr("affects")[0], _block.network.attr("affectedBy")[0], force=True)
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
            if _ins.get("ctls") is not None:
                pm.sets(_top_ins["controls_set"], addElement=_ins["ctls"])
            if _ins.get("jnts") is not None:
                pm.sets(_top_ins["deformer_set"], addElement=_ins["jnts"])
            for _b in _block["blocks"]:
                _create_set(_b)

        #   ----

        _create_set(blueprint)

        # recursive
        def _cleanup_controls(_block):
            if _block.parent:
                _ins = context.instance(_block.ins_name)
                _parent_ins = context.instance(_block.parent.ins_name)
                for x in _ins["ctls"]:
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
        for member in top_ins["controls_set"].members():
            for index, shape in enumerate(member.getShapes()):
                shape.rename(f"temp{index}")
            for index, shape in enumerate(member.getShapes()):
                shape.rename(f"{shape.getParent().nodeName()}{index if index else str()}")
                shape.attr("isHistoricallyInteresting").set(0)

    def skinning(self, context):
        pass

    def deformers(self, context):
        pass


class PostScript:

    def __init__(self):
        self.msg = f"Process {self.__module__}.{self.__class__}"
