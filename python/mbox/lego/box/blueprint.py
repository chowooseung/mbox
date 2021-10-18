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


def get_component_index(self, name, direction, indexes):
    for block in self.blocks:
        get_component_index(block, name, direction, indexes)

    if hasattr(self, "component"):
        if (self.naming == name) and (self.direction == direction):
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
    for block in self.blocks:
        b = get_specify_block(block, name, direction, index)
        if b:
            return

    if hasattr(self, "component"):
        if self.naming == name and self.direction == direction and self.index == index:
            return self


class Root:

    GUIDE = None
    NETWORK = None
    RIG = None

    def __init__(self):
        Root.GUIDE = None
        Root.NETWORK = None
        Root.RIG = None

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
        self.direction = ["C", "L", "R"]

        # Extension
        self.jointExt = "jnt"
        self.controlExt = "con"

        # Convention
        self.jointConvention = "{name}_{direction}{index}_{description}_{extension}"
        self.controlConvention = "{name}_{direction}{index}_{description}_{extension}"

        # default, lower, upper, capitalize
        self.jointDescriptionLetterCase = "default"
        self.controlDescriptionLetterCase = "default"

        # padding
        self.jointPadding = 0
        self.controlPadding = 0

        # bool
        self.runPreScripts = False
        self.runPostScripts = False

        # Scripts path
        self.preScripts = list()
        self.postScripts = list()

        # Schema version
        self.schema = mbox.version.schema

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
            msg += f"{key} : {value}\n"

        logger.info(msg)

    def draw_guide(self):
        """network node의 affectedBy[0], affects[0]은 blocks의 관계에 사용합니다."""
        if not Root.NETWORK:
            self.draw_network()
        # create root, root network
        Root.GUIDE = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())

        # attribute
        attribute.lockAttribute(Root.GUIDE)
        attribute.setKeyableAttributes(Root.GUIDE, list())
        attribute.addAttribute(Root.GUIDE, "isGuideRoot", "bool", keyable=False)

        # connection
        pm.connectAttr(Root.GUIDE.message, Root.NETWORK.guide, force=True)

        selection = None
        for block in self.blocks:
            selection = block.draw_guide(parent=Root.GUIDE)

        return selection

    def draw_network(self):
        Root.NETWORK = pm.createNode("network")

        attribute.addAttribute(Root.NETWORK, "guide", "message")
        attribute.addAttribute(Root.NETWORK, "rig", "message")
        attribute.addAttribute(Root.NETWORK, "component", "string", self.component)
        attribute.addAttribute(Root.NETWORK, "name", "string", self.name)
        attribute.addAttribute(Root.NETWORK, "version", "string", self.version)
        attribute.addAttribute(Root.NETWORK, "schema", "string", self.schema)
        attribute.addAttribute(Root.NETWORK, "process", "string", self.process)
        attribute.addEnumAttribute(Root.NETWORK, "step", self.step,
                                   ["all", "prepare", "objects", "attributes", "operate"], keyable=False)
        add_attribute(Root.NETWORK, "direction", "string", multi=True)
        [Root.NETWORK.direction[index].set(direction) for index, direction in enumerate(self.direction)]
        attribute.addAttribute(Root.NETWORK, "jointExt", "string", self.jointExt)
        attribute.addAttribute(Root.NETWORK, "controlExt", "string", self.controlExt)
        attribute.addAttribute(Root.NETWORK, "jointConvention", "string", self.jointConvention)
        attribute.addAttribute(Root.NETWORK, "controlConvention", "string", self.controlConvention)
        attribute.addEnumAttribute(Root.NETWORK, "jointDescriptionLetterCase", self.jointDescriptionLetterCase,
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addEnumAttribute(Root.NETWORK, "controlDescriptionLetterCase", self.controlDescriptionLetterCase,
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addAttribute(Root.NETWORK, "runPreScripts", "bool", self.runPreScripts, keyable=False)
        attribute.addAttribute(Root.NETWORK, "runPostScripts", "bool", self.runPostScripts, keyable=False)
        add_attribute(Root.NETWORK, "preScripts", "string", multi=True)
        add_attribute(Root.NETWORK, "postScripts", "string", multi=True)
        [Root.NETWORK.preScripts[index].set(script) for index, script in enumerate(self.preScripts)]
        [Root.NETWORK.postScripts[index].set(script) for index, script in enumerate(self.postScripts)]
        attribute.addAttribute(Root.NETWORK, "notes", "string", self.notes)

        for block in self.blocks:
            block.draw_network()

    def draw_rig(self, context, step):
        if not Root.NETWORK:
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
        Root.NETWORK.attr("name").set(self.name)
        Root.NETWORK.attr("version").set(self.version)
        Root.NETWORK.attr("schema").set(self.schema)
        Root.NETWORK.attr("process").set(self.process)
        Root.NETWORK.attr("step").set(self.step)
        Root.NETWORK.attr("direction").set(self.direction)
        Root.NETWORK.attr("jointExt").set(self.jointExt)
        Root.NETWORK.attr("controlExt").set(self.controlExt)
        Root.NETWORK.attr("jointConvention").set(self.jointConvention)
        Root.NETWORK.attr("controlConvention").set(self.controlConvention)
        Root.NETWORK.attr("jointDescriptionLetterCase").set(self.jointDescriptionLetterCase)
        Root.NETWORK.attr("controlDescriptionLetterCase").set(self.controlDescriptionLetterCase)
        Root.NETWORK.attr("jointPadding").set(self.jointPadding)
        Root.NETWORK.attr("controlPadding").set(self.controlPadding)
        Root.NETWORK.attr("runPreScripts").set(self.runPreScripts)
        Root.NETWORK.attr("runPostScripts").set(self.runPostScripts)
        [Root.NETWORK.preScripts[index].set(script) for index, script in enumerate(self.preScripts)]
        [Root.NETWORK.postScripts[index].set(script) for index, script in enumerate(self.postScripts)]
        Root.NETWORK.attr("notes").set(self.notes)

        for block in self.blocks:
            block.update_blueprint_to_network()

    def update_network_to_blueprint(self):
        self.name = Root.NETWORK.attr("name").get()
        self.version = Root.NETWORK.attr("version").get()
        self.schema = Root.NETWORK.attr("schema").get()
        self.process = Root.NETWORK.attr("process").get()
        self.step = Root.NETWORK.attr("step").get(asString=True)
        self.direction = Root.NETWORK.attr("direction").get()
        self.jointExt = Root.NETWORK.attr("jointExt").get()
        self.controlExt = Root.NETWORK.attr("controlExt").get()
        self.jointConvention = Root.NETWORK.attr("jointConvention").get()
        self.controlConvention = Root.NETWORK.attr("controlConvention").get()
        self.jointDescriptionLetterCase = Root.NETWORK.attr("jointDescriptionLetterCase").get(asString=True)
        self.controlDescriptionLetterCase = Root.NETWORK.attr("controlDescriptionLetterCase").get(asString=True)
        self.jointPadding = Root.NETWORK.attr("jointPadding").get()
        self.controlPadding = Root.NETWORK.attr("controlPadding").get()
        self.runPreScripts = Root.NETWORK.attr("runPreScripts").get()
        self.runPostScripts = Root.NETWORK.attr("runPostScripts").get()
        self.preScripts = Root.NETWORK.attr("preScripts").get()
        self.postScripts = Root.NETWORK.attr("postScripts").get()
        self.notes = Root.NETWORK.attr("notes").get()

    @staticmethod
    def connect_network(obj):
        if obj.component == "mbox":
            Root.reset_network_connection(obj)

        for block in obj.blocks:
            pm.connectAttr(obj.__class__.NETWORK.affects[0], block.__class__.NETWORK.affedtedBy[0], force=True)
            Root.connect_network(block)

    @staticmethod
    def reset_network_connection(obj):
        pm.disconnectAttr(obj.__class__.NETWORK.affects[0])
        for block in obj.blocks:
            Root.reset_network_connection(block)

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

    def __init__(self):
        self.__class__.GUIDE = None
        self.__class__.NETWORK = None
        self.__class__.RIG = None

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
        self.joint = True

        # primary axis, secondary axis
        self.primaryAxis = "x"
        self.secondaryAxis = "y"

        # guide transform matrix list
        self.transforms = list()

        # parent node name
        self.rootRefIndex = -1

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
        for block in self.blocks:
            block.draw_guide(parent)

    def draw_network(self):
        self.__class__.NETWORK = pm.createNode("network")
        attribute.addAttribute(self.__class__.NETWORK, "guide", "message")
        attribute.addAttribute(self.__class__.NETWORK, "rig", "message")
        attribute.addAttribute(self.__class__.NETWORK, "component", "string", self.component)
        attribute.addAttribute(self.__class__.NETWORK, "version", "string", self.version)
        attribute.addAttribute(self.__class__.NETWORK, "name", "string", self.name)
        attribute.addEnumAttribute(self.__class__.NETWORK, "direction", self.direction,
                                   ["center", "right", "left"], keyable=False)
        attribute.addAttribute(self.__class__.NETWORK, "index", "long", self.index, keyable=False)
        attribute.addAttribute(self.__class__.NETWORK, "joint", "bool", self.joint, keyable=False)
        attribute.addEnumAttribute(self.__class__.NETWORK, "primaryAxis", self.primaryAxis,
                                   ["x", "y", "z", "-x", "-y", "-z"], keyable=False)
        attribute.addEnumAttribute(self.__class__.NETWORK, "secondaryAxis", self.secondaryAxis,
                                   ["x", "y", "z", "-x", "-y", "-z"], keyable=False)
        add_attribute(self.__class__.NETWORK, "transforms", "matrix", multi=True)
        attribute.addAttribute(self.__class__.NETWORK, "rootRefIndex", "long", self.rootRefIndex)

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
        if self.__class__.GUIDE:
            # get component guide node
            repeated = [self.__class__.GUIDE]
            guides = list()
            guides += repeated
            while True:
                children = list()
                for r in repeated:
                    children += [x for x in r.getChildren(type="transform") if x.hasAttr("isGuide")]
                guides += children
                if not children:
                    break
                repeated = guides

            # rename guide node
            for guide in guides:
                n = guide.split("_")
                n[0] = f"{self.name}"
                n[1] = f"{self.direction}{self.index}"
                guide.rename("_".join(n))

        Root.NETWORK.attr("component").set(self.component)
        Root.NETWORK.attr("version").set(self.version)
        Root.NETWORK.attr("name").set(self.name)
        Root.NETWORK.attr("direction").set(self.direction)
        Root.NETWORK.attr("index").set(self.index)
        Root.NETWORK.attr("joint").set(self.joint)
        Root.NETWORK.attr("primaryAxis").set(self.primaryAxis)
        Root.NETWORK.attr("secondaryAxis").set(self.secondaryAxis)
        if self.__class__.GUIDE:
            for index, attr in enumerate(Root.NETWORK.transforms):
                attr.inputs(type="transform")[0].setMatrix(pm.datatypes.Matrix(self.transforms[index]), worldSpace=True)
        else:
            [Root.NETWORK.attr("transforms")[i].set(pm.datatypes.Matrix(m)) for i, m in enumerate(self.transforms)]
        Root.NETWORK.attr("rootRefIndex").set(self.rootRefIndex)

        for block in self.blocks:
            block.update_blueprint_to_network()

    def update_network_to_blueprint(self):
        """get common block info"""
        self.component = Root.NETWORK.attr("component").get()
        self.version = Root.NETWORK.attr("version").get()
        self.name = Root.NETWORK.attr("name").get()
        self.direction = Root.NETWORK.attr("direction").get(asString=True)
        self.index = Root.NETWORK.attr("index").get()
        self.joint = Root.NETWORK.attr("joint").get()
        self.primaryAxis = Root.NETWORK.attr("primaryAxis").get(asString=True)
        self.secondaryAxis = Root.NETWORK.attr("secondaryAxis").get(asString=True)
        self.transforms = [x.tolist() for x in Root.NETWORK.attr("transforms").get()]
        self.rootRefIndex = Root.NETWORK.attr("rootRefIndex").get()

        for block in self.blocks:
            block.update_network_to_blueprint()
