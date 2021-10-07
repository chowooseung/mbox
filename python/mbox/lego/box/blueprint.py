# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

#
import logging
import json

# mbox
import mbox.version
from mbox.lego import box
from mbox.core.attribute import add_attribute

# mgear
from mgear.core import primitive, attribute


logger = logging.getLogger(__name__)


class Root:

    def __init__(self):
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
        self.controllerExt = "con"

        # Convention
        self.jointConvention = "{name}_{direction}{index}_{description}_{extension}"
        self.controllerConvention = "{name}_{direction}{index}_{description}_{extension}"

        # default, lower, upper, capitalize
        self.jointDescriptionLetterCase = "default"
        self.controllerDescriptionLetterCase = "default"

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

        # The order of assembly
        self.priority = 0

        # Child blocks
        self.blocks = list()

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def print(self):
        blocks_msg = f""
        for block in self.blocks:
            blocks_msg += block.print()
        msg = (f"\n\nAsset Name : {self.name}\n"
               f"Box Version : {self.version}\n"
               f"Schema : {self.schema}\n"
               f"Process : {self.process}\n"
               f"Step : {self.step}\n"
               f"Direction : {self.direction}\n"
               f"Joint extension : {self.jointExt}\n"
               f"Controller extension : {self.controllerExt}\n"
               f"Joint Convention : {self.jointConvention}\n"
               f"Controller Convention : {self.controllerConvention}\n"
               f"Run ProScripts : {self.runPreScripts}\n"
               f"Run postScripts : {self.runPostScripts}\n"
               f"PreScripts : {self.preScripts}\n"
               f"PostScripts : {self.postScripts}\n"
               f"Blocks : {blocks_msg}\n"
               f"Notes : {self.notes}\n")
        logger.info(msg)

    def save(self, path):
        blueprint = self.__dict__.copy()
        blueprint["blocks"] = list()

        for block in self.__dict__["blocks"]:
            blueprint["blocks"].append(block.save())

        with open(path, "w") as f:
            json.dump(blueprint, f, ensure_ascii=False, sort_keys=False, indent=2)

    def load(self, path):
        """todo"""

    def is_valid_schema(self):
        """todo"""

    def create_guide(self):
        """network node의 affectedBy[0], affects[0]은 blocks의 관계에 사용합니다."""
        guide = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())
        attribute.lockAttribute(guide)
        attribute.setKeyableAttributes(guide, list())
        attribute.addAttribute(guide, "isGuideRoot", "bool", keyable=False)

        network = pm.createNode("network")
        attribute.addAttribute(network, "guide", "message")
        attribute.addAttribute(network, "rig", "message")
        attribute.addAttribute(network, "name", "string", self.name)
        attribute.addAttribute(network, "version", "string", self.version)
        attribute.addAttribute(network, "schema", "string", self.schemaVersion)
        attribute.addAttribute(network, "process", "string", self.process)
        attribute.addAttribute(network, "step", "string", self.step)
        add_attribute(network, "direction", "string", multi=True)
        [network.direction[index].set(direction) for index, direction in enumerate(self.direction)]
        attribute.addAttribute(network, "jointExt", "string", self.jointExt)
        attribute.addAttribute(network, "controllerExt", "string", self.controllerExt)
        attribute.addAttribute(network, "jointConvention", "string", self.jointConvention)
        attribute.addAttribute(network, "controllerConvention", "string", self.controllerConvention)
        attribute.addAttribute(network, "runPreScripts", "bool", self.runPreScripts, keyable=False)
        attribute.addAttribute(network, "runPostScripts", "bool", self.runPostScripts, keyable=False)
        add_attribute(network, "preScripts", "string", multi=True)
        add_attribute(network, "postScripts", "string", multi=True)
        [network.preScripts[index].set(script) for index, script in enumerate(self.preScripts)]
        [network.postScripts[index].set(script) for index, script in enumerate(self.postScripts)]
        attribute.addAttribute(network, "notes", "string", self.notes)

        guide.message >> network.guide
        for block in self.blocks:
            block.create_guide(guide, network)

    def create_rig(self):
        """todo"""
        # objects
        box.objects()
            # blocks objects

        # attributes
        box.attributes()
            # blocks attributes

        # connections
        box.connections()
            # blocks connections


class Blocks:

    def __init__(self):
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

        # primary axis, secondary axis list # ["x", "y"]
        self.jointAxis = ["x", "y"]

        # guide transform matrix list
        self.transforms = list()

        # parent node name
        self.parent = None

        # priority
        self.priority = 1

    def print(self):
        msg = (f"\n   Component : {self.component}\n"
               f"   Component Version : {self.version}\n"
               f"   Name : {self.name}\n"
               f"   Direction : {self.direction}\n"
               f"   Index : {self.index}\n"
               f"   Joint : {self.joint}\n"
               f"   Joint Axis : {self.jointAxis}\n"
               f"   Transforms : {self.transforms}\n"
               f"   Parent : {self.parent}\n"
               f"   Priority : {self.priority}\n")
        return msg

    def save(self):
        blueprint = self.__dict__.copy()
        blueprint["blocks"] = list()

        for block in self.__dict__["blocks"]:
            blueprint["blocks"].append(block.save())
        return blueprint
