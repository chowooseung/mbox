# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

#
import logging
import json

# mbox
import mbox.version
from mbox.core.attribute import add_attribute
from mbox.lego import box, utils

# mgear
from mgear.core import primitive, attribute

logger = logging.getLogger(__name__)


def get_component_index(self, name, direction, indexes=None):
    if indexes is None:
        indexes = list()
    for block in self.blocks:
        get_component_index(block, name, direction, indexes)

    if self.component != "mbox":
        if (self.name == name) and (self.direction == direction):
            indexes.append(self.index)
        return

    index = 0
    while True:
        if index in indexes:
            index += 1
        else:
            break
    return index


def get_specify_block(self, name, direction, index):
    if self.component != "mbox":
        if self.name == name and self.direction == direction and self.index == index:
            return self

    for block in self.blocks:
        b = get_specify_block(block, name, direction, index)
        if b:
            return b


def get_component_guide(component):
    if component.hasAttr("is_guide"):
        while True:
            parent = component.getParent() if component.getParent().hasAttr("is_guide_component") else None
            component = parent
            if parent:
                break
    elif component.hasAttr("is_guideRoot"):
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


def connect_network(obj):
    if obj.component == "mbox":
        reset_network_connection(obj)

    for block in obj.blocks:
        pm.connectAttr(obj.NETWORK.affects[0], block.NETWORK.affectedBy[0], force=True)
        connect_network(block)


def reset_network_connection(obj):
    pm.disconnectAttr(obj.NETWORK.affects[0])
    for block in obj.blocks:
        reset_network_connection(block)


class Root:

    def __init__(self, guide=None, network=None, rig=None):
        self.GUIDE = guide
        self.NETWORK = network
        self.RIG = rig

        # component
        self.component = "mbox"

        # version
        self.version = mbox.version.mbox

        # WIP or PUB
        self.process = "WIP"

        # all, prepare, objects, attributes, operate
        self.step = "all"

        # Asset name
        self.name = "rig"

        # Direction string
        self.joint_direction = ["C", "L", "R"]
        self.controls_direction = ["C", "L", "R"]

        # Extension
        self.joint_ext = "jnt"
        self.controls_ext = "con"

        # Convention
        self.joint_convention = "{name}_{direction}{index}_{description}_{extension}"
        self.controls_convention = "{name}_{direction}{index}_{description}_{extension}"

        # default, lower, upper, capitalize
        self.joint_description_letter_case = "default"
        self.controls_description_letter_case = "default"

        # padding
        self.joint_padding = 0
        self.controls_padding = 0

        # bool
        self.run_pre_scripts = False
        self.run_post_scripts = False

        # Scripts path
        self.pre_scripts = list()
        self.post_scripts = list()

        # Schema version
        self.schema = mbox.version.schema

        # controls index color
        self.l_color_fk = 6
        self.l_color_ik = 18
        self.r_color_fk = 23
        self.r_color_ik = 14
        self.c_color_fk = 13
        self.c_color_ik = 17

        # use RGB color
        self.use_RGB_color = False

        # controls RGB color
        self.l_RGB_fk = [0, 0, 1]
        self.l_RGB_ik = [0, 0.25, 1]
        self.r_RGB_fk = [1, 0, 0]
        self.r_RGB_ik = [1, 0.1, 0.25]
        self.c_RGB_fk = [1, 1, 0]
        self.c_RGB_ik = [0, 0.6, 0]

        # notes
        self.notes = None

        # Child blocks
        self.blocks = list()

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def print(self):
        blocks_msg = f""
        for block in self.blocks:
            blocks_msg += block.print(1)

        msg = f"\n\n"
        for key, value in self.__dict__.items():
            if key == "blocks":
                msg += f"{key} : \n{blocks_msg}\n"
            else:
                msg += f"{key} : {value}\n"

        logger.info(msg)

    def draw_guide(self):
        """network node의 affectedBy[0], affects[0]은 blocks의 관계에 사용합니다."""
        if not self.NETWORK:
            self.draw_network()
        # create root, root network
        self.GUIDE = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())

        # attribute
        attribute.lockAttribute(self.GUIDE)
        attribute.setKeyableAttributes(self.GUIDE, list())
        attribute.addAttribute(self.GUIDE, "is_guide_root", "bool", keyable=False)

        # connection
        pm.connectAttr(self.GUIDE.message, self.NETWORK.guide, force=True)

        selection = None
        for block in self.blocks:
            selection = block.draw_guide(parent=self.GUIDE)

        connect_network(self)
        return selection

    def draw_network(self):
        self.NETWORK = pm.createNode("network")

        attribute.addAttribute(self.NETWORK, "guide", "message")
        attribute.addAttribute(self.NETWORK, "rig", "message")
        attribute.addAttribute(self.NETWORK, "component", "string", self.component)
        attribute.addAttribute(self.NETWORK, "name", "string", self.name)
        attribute.addAttribute(self.NETWORK, "version", "string", self.version)
        attribute.addAttribute(self.NETWORK, "schema", "string", self.schema)
        attribute.addAttribute(self.NETWORK, "process", "string", self.process)
        attribute.addEnumAttribute(self.NETWORK, "step", self.step,
                                   ["all", "prepare", "objects", "attributes", "operate"], keyable=False)
        add_attribute(self.NETWORK, "joint_direction", "string", multi=True)
        add_attribute(self.NETWORK, "controls_direction", "string", multi=True)
        [self.NETWORK.joint_direction[i].set(direction) for i, direction in enumerate(self.joint_direction)]
        [self.NETWORK.controls_direction[i].set(direction) for i, direction in enumerate(self.controls_direction)]
        attribute.addAttribute(self.NETWORK, "joint_ext", "string", self.joint_ext)
        attribute.addAttribute(self.NETWORK, "controls_ext", "string", self.controls_ext)
        attribute.addAttribute(self.NETWORK, "joint_convention", "string", self.joint_convention)
        attribute.addAttribute(self.NETWORK, "controls_convention", "string", self.controls_convention)
        attribute.addEnumAttribute(self.NETWORK, "joint_description_letter_case", self.joint_description_letter_case,
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addEnumAttribute(self.NETWORK, "controls_description_letter_case",
                                   self.controls_description_letter_case,
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addAttribute(self.NETWORK, "joint_padding", "long", self.joint_padding, keyable=False)
        attribute.addAttribute(self.NETWORK, "controls_padding", "long", self.controls_padding, keyable=False)
        attribute.addAttribute(self.NETWORK, "run_pre_scripts", "bool", self.run_pre_scripts, keyable=False)
        attribute.addAttribute(self.NETWORK, "run_post_scripts", "bool", self.run_post_scripts, keyable=False)
        add_attribute(self.NETWORK, "pre_scripts", "string", multi=True)
        add_attribute(self.NETWORK, "post_scripts", "string", multi=True)
        [self.NETWORK.pre_scripts[index].set(script) for index, script in enumerate(self.pre_scripts)]
        [self.NETWORK.post_scripts[index].set(script) for index, script in enumerate(self.post_scripts)]
        attribute.addAttribute(self.NETWORK, "l_color_fk", "long", self.l_color_fk, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "l_color_ik", "long", self.l_color_ik, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "r_color_fk", "long", self.r_color_fk, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "r_color_ik", "long", self.r_color_ik, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "c_color_fk", "long", self.c_color_fk, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "c_color_ik", "long", self.c_color_ik, minValue=0, maxValue=31)
        attribute.addAttribute(self.NETWORK, "use_RGB_Color", "bool", self.use_RGB_color, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "l_RGB_fk", self.l_RGB_fk, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "l_RGB_ik", self.l_RGB_ik, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "r_RGB_fk", self.r_RGB_fk, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "r_RGB_ik", self.r_RGB_ik, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "c_RGB_fk", self.c_RGB_fk, keyable=False)
        attribute.addColorAttribute(self.NETWORK, "c_RGB_ik", self.c_RGB_ik, keyable=False)
        attribute.addAttribute(self.NETWORK, "notes", "string", self.notes)

        for block in self.blocks:
            block.draw_network()

    def draw_rig(self, context, step):
        if not self.NETWORK:
            self.draw_network()

        # step objects
        if step == "objects":
            logger.info("----- step object -----")
            box.objects(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

        # step attributes
        if step == "attributes":
            logger.info("----- step attributes -----")
            box.attributes(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

        # step connections
        if step == "connections":
            logger.info("----- step connections -----")
            box.connections(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

        # return context for post scripts
        return context

    def update_blueprint_to_network(self):
        self.NETWORK.attr("name").set(self.name)
        self.NETWORK.attr("version").set(self.version)
        self.NETWORK.attr("schema").set(self.schema)
        self.NETWORK.attr("process").set(self.process)
        self.NETWORK.attr("step").set(self.step)
        [self.NETWORK.joint_direction[i].set(direction) for i, direction in enumerate(self.joint_direction)]
        [self.NETWORK.controls_direction[i].set(direction) for i, direction in enumerate(self.controls_direction)]
        self.NETWORK.attr("joint_ext").set(self.joint_ext)
        self.NETWORK.attr("controls_ext").set(self.controls_ext)
        self.NETWORK.attr("joint_convention").set(self.joint_convention)
        self.NETWORK.attr("controls_convention").set(self.controls_convention)
        self.NETWORK.attr("joint_description_letter_case").set(self.joint_description_letter_case)
        self.NETWORK.attr("controls_description_letter_case").set(self.controls_description_letter_case)
        self.NETWORK.attr("joint_padding").set(self.joint_padding)
        self.NETWORK.attr("controls_padding").set(self.controls_padding)
        self.NETWORK.attr("run_pre_scripts").set(self.run_pre_scripts)
        self.NETWORK.attr("run_post_scripts").set(self.run_post_scripts)
        [self.NETWORK.pre_scripts[index].set(script) for index, script in enumerate(self.pre_scripts)]
        [self.NETWORK.post_scripts[index].set(script) for index, script in enumerate(self.post_scripts)]
        self.NETWORK.attr("notes").set(str(self.notes))

        for block in self.blocks:
            block.update_blueprint_to_network()

    def update_network_to_blueprint(self):
        self.name = self.NETWORK.attr("name").get()
        self.version = self.NETWORK.attr("version").get()
        self.schema = self.NETWORK.attr("schema").get()
        self.process = self.NETWORK.attr("process").get()
        self.step = self.NETWORK.attr("step").get(asString=True)
        self.joint_direction = self.NETWORK.attr("joint_direction").get()
        self.controls_direction = self.NETWORK.attr("controls_direction").get()
        self.joint_ext = self.NETWORK.attr("joint_ext").get()
        self.controls_ext = self.NETWORK.attr("controls_ext").get()
        self.joint_convention = self.NETWORK.attr("joint_convention").get()
        self.controls_convention = self.NETWORK.attr("controls_convention").get()
        self.joint_description_letter_case = self.NETWORK.attr("joint_description_letter_case").get(asString=True)
        self.controls_description_letter_case = self.NETWORK.attr("controls_description_letter_case").get(asString=True)
        self.joint_padding = self.NETWORK.attr("joint_padding").get()
        self.controls_padding = self.NETWORK.attr("controls_padding").get()
        self.run_pre_scripts = self.NETWORK.attr("run_pre_scripts").get()
        self.run_post_scripts = self.NETWORK.attr("run_post_scripts").get()
        self.pre_scripts = self.NETWORK.attr("pre_scripts").get()
        self.post_scripts = self.NETWORK.attr("post_scripts").get()
        self.notes = self.NETWORK.attr("notes").get()

        for block in self.blocks:
            block.update_network_to_blueprint()

    @staticmethod
    def save(obj, path=None):
        blueprint = obj.__dict__.copy()
        blueprint["blocks"] = list()

        for block in obj.__dict__["blocks"]:
            blueprint["blocks"].append(Root.save(block))

        if obj.component == "mbox":
            with open(path, "w") as f:
                json.dump(blueprint, f, ensure_ascii=False, sort_keys=False, indent=2)
        else:
            return blueprint

    @staticmethod
    def load(obj, data):

        obj.set(**data)

        for index, b_data in enumerate(obj.blocks):
            mod = utils.load_block_blueprint(b_data["component"])
            block = mod.Block()
            Root.load(block, b_data)
            obj.blocks[index] = block

        if obj.component == "mbox":
            return obj


class Blocks:

    def __init__(self, guide=None, network=None, rig=None):
        self.GUIDE = guide
        self.NETWORK = network
        self.RIG = rig

        # what kind of box
        self.component = None

        # block version
        self.version = None

        # module name # arm... leg... spine...
        self.name = None

        # "center", "left", "right"
        self.direction = "center"

        # index
        self.index = 0

        # True - create joint / False
        self.joint_rig = True

        # primary axis, secondary axis
        self.primary_axis = "x"
        self.secondary_axis = "y"

        # guide transform matrix list
        self.transforms = list()

        # parent node name
        self.root_ref_index = -1
        self.joint_ref_index = -1

        # blocks
        self.blocks = list()

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def print(self, recurNum):
        tab = "    " * recurNum
        msg = f"\n"
        for key, value in self.__dict__.items():
            msg += f"{tab}{key} : {value}\n"

        recurNum += 1
        child_msg = f""
        for block in self.blocks:
            child_msg += block.print(recurNum)
        return msg + child_msg

    def draw_guide(self, parent):
        """"""
        pm.connectAttr(self.GUIDE.message, self.NETWORK.guide, force=True)
        for block in self.blocks:
            block.draw_guide(parent)

    def draw_network(self):
        self.NETWORK = pm.createNode("network")
        attribute.addAttribute(self.NETWORK, "guide", "message")
        attribute.addAttribute(self.NETWORK, "rig", "message")
        attribute.addAttribute(self.NETWORK, "component", "string", self.component)
        attribute.addAttribute(self.NETWORK, "version", "string", self.version)
        attribute.addAttribute(self.NETWORK, "name", "string", self.name)
        attribute.addEnumAttribute(self.NETWORK, "direction", self.direction,
                                   ["center", "right", "left"], keyable=False)
        attribute.addAttribute(self.NETWORK, "index", "long", self.index, keyable=False)
        attribute.addAttribute(self.NETWORK, "joint_rig", "bool", self.joint_rig, keyable=False)
        attribute.addEnumAttribute(self.NETWORK, "primary_axis", self.primary_axis,
                                   ["x", "y", "z", "-x", "-y", "-z"], keyable=False)
        attribute.addEnumAttribute(self.NETWORK, "secondary_axis", self.secondary_axis,
                                   ["x", "y", "z", "-x", "-y", "-z"], keyable=False)
        add_attribute(self.NETWORK, "transforms", "matrix", multi=True)
        attribute.addAttribute(self.NETWORK, "root_ref_index", "long", self.root_ref_index)
        attribute.addAttribute(self.NETWORK, "joint_ref_index", "long", self.joint_ref_index)

        for block in self.blocks:
            block.draw_network()

    def draw_rig(self, context, step, rig):
        # step objects
        if step == "objects":
            logger.info("----- step object -----")
            rig.objects(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

        # step attributes
        if step == "attributes":
            logger.info("----- step attributes -----")
            rig.attributes(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

        # step connections
        if step == "connections":
            logger.info("----- step connections -----")
            rig.connections(self, context)
            for block in self.blocks:
                block.draw_rig(block, context, step)

    def update_blueprint_to_network(self):
        print("update bp to net")
        if self.GUIDE:
            print("has guide")
            # get component guide node
            repeated = [self.GUIDE]
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

            # rename guide node
            for guide in guides:
                n = guide.split("_")
                n[0] = f"{self.name}"
                n[1] = f"{self.direction}{self.index}"
                guide.rename("_".join(n))

        self.NETWORK.attr("component").set(self.component)
        self.NETWORK.attr("version").set(self.version)
        self.NETWORK.attr("name").set(self.name)
        self.NETWORK.attr("direction").set(self.direction)
        self.NETWORK.attr("index").set(self.index)
        self.NETWORK.attr("joint_rig").set(self.joint_rig)
        self.NETWORK.attr("primary_axis").set(self.primary_axis)
        self.NETWORK.attr("secondary_axis").set(self.secondary_axis)
        if self.GUIDE:
            for index, attr in enumerate(self.NETWORK.transforms):
                attr.inputs(type="transform")[0].setMatrix(pm.datatypes.Matrix(self.transforms[index]), worldSpace=True)
        else:
            [self.NETWORK.attr("transforms")[i].set(pm.datatypes.Matrix(m)) for i, m in enumerate(self.transforms)]
        self.NETWORK.attr("root_ref_index").set(self.root_ref_index)
        self.NETWORK.attr("joint_ref_index").set(self.joint_ref_index)

        for block in self.blocks:
            block.update_blueprint_to_network()

    def update_network_to_blueprint(self):
        """get common block info"""
        self.component = self.NETWORK.attr("component").get()
        self.version = self.NETWORK.attr("version").get()
        self.name = self.NETWORK.attr("name").get()
        self.direction = self.NETWORK.attr("direction").get(asString=True)
        self.index = self.NETWORK.attr("index").get()
        self.joint_rig = self.NETWORK.attr("joint_rig").get()
        self.primary_axis = self.NETWORK.attr("primary_axis").get(asString=True)
        self.secondary_axis = self.NETWORK.attr("secondary_axis").get(asString=True)
        self.transforms = [x.tolist() for x in self.NETWORK.attr("transforms").get()]
        self.root_ref_index = self.NETWORK.attr("root_ref_index").get()
        self.joint_ref_index = self.NETWORK.attr("joint_ref_index").get()

        for block in self.blocks:
            block.update_network_to_blueprint()
