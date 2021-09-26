# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

#
import logging

logger = logging.getLogger(__name__)


class Root:

    def __init__(self):
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
        self.schemaVersion = "blueprint-1"

        # notes
        self.notes = None

        # The order of assembly
        self.priority = 0

        # Child blocks
        self.blocks = list()

    def set(self, **kwargs):
        self.process = kwargs["process"]
        self.step = kwargs["step"]
        self.name = kwargs["name"]
        self.direction = kwargs["direction"]
        self.jointExt = kwargs["jointExt"]
        self.controllerExt = kwargs["controllerExt"]
        self.jointConvention = kwargs["jointConvention"]
        self.controllerConvention = kwargs["controllerConvention"]
        self.jointDescriptionLetterCase = kwargs["jointDescriptionLetterCase"]
        self.controllerDescriptionLetterCase = kwargs["controllerDescriptionLetterCase"]
        self.runPreScripts = kwargs["runPreScripts"]
        self.runPostScripts = kwargs["runPostScripts"]
        self.preScripts = kwargs["preScripts"]
        self.postScripts = kwargs["postScripts"]
        self.schemaVersion = kwargs["schemaVersion"]
        self.notes = kwargs["notes"]
        self.blocks = kwargs["blocks"]

    def print(self):
        msg = f"""Asset Name : {self.name}
        Box Version : {self.version}
        Schema Version : {self.schemaVersion}
        Process : {self.process}
        Step : {self.step}
        Direction : {self.direction}
        Joint extension : {self.jointExt}
        Controller extension : {self.controllerExt}
        Joint Convention : {self.jointConvention}
        Controller Convention : {self.controllerConvention}
        Run ProScripts : {self.runPreScripts}
        Run postScripts : {self.runpostScripts}
        PreScripts : {self.preScripts}
        PostScripts : {self.postScripts}
        Blocks : {self.blocks}
        Notes : {self.notes}
        """
        logger.info(msg)

    def save_json(self, path):
        """TODO"""


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
        self.priority = 0

        self.msg = None

    def set(self, **kwargs):
        self.component = kwargs["component"]
        self.version = kwargs["version"]
        self.name = kwargs["name"]
        self.direction = kwargs["direction"]
        self.index = kwargs["index"]
        self.joint = kwargs["joint"]
        self.jointAxis = kwargs["jointAxis"]
        self.transforms = kwargs["transforms"]
        self.parent = kwargs["parent"]
        self.priority = kwargs["priority"]

    def print(self):
        self.msg = f"""Component : {self.component}
        Component Version : {self.version}
        Name : {self.name}
        Direction : {self.direction}
        Index : {self.index}
        Joint : {self.joint}
        Joint Axis : {self.jointAxis}
        Transforms : {self.transforms}
        Parent : {self.parent}
        Priority : {self.priority}
        
        """

    def save_json(self):
        """TODO"""
