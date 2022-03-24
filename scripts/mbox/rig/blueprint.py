# -*- coding: utf-8 -*-

# built-in
import json
import os
import uuid

# maya
from pymel import core as pm

# mbox
from mbox import logger
from .build import BuildSystem
from .utils import Selection, traversal, import_component_module

# mgear
from mgear.core import vector, transform, icon, attribute, curve


class Component(dict):

    @property
    def is_assembly(self):
        return True if self["comp_type"] == "assembly" else False

    @property
    def valid(self):
        return self._valid

    @property
    def chain(self):
        # TODO: guide chain
        transforms = list()
        return transforms if transforms else "#"

    @property
    def negate(self):
        return True if self["comp_side"] == "R" else False

    @property
    def blade(self):
        b = vector.Blade(pm.datatypes.Matrix(self["blade_matrix"])) if self["blade_matrix"] else None
        return b.z, b.x if b else b

    @property
    def network(self):
        return self._network

    @property
    def guides(self):
        return Selection(self.network).guides

    @property
    def ui_host(self):
        return Selection(self.network).ui_host

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        if self._parent:
            self._parent["children"].remove(self)
        self._parent = p
        self._parent["children"].append(self)

    def __init__(self, network=None, parent=None, data=None):
        super(Component, self).__init__()
        self._parent = parent
        if self._parent:
            self._parent["children"].append(self)
        self.update(data) if data else self.__load()
        self._network = network
        self._valid = True
        if not self.is_assembly:
            if self["transforms"] == "#":
                self["transforms"] = self.chain
                if self["transforms"] == "#":
                    self._valid = False

    def __setitem__(self, key, value):
        # TODO: guide __setitem__
        pass

    def update(self, __m: Mapping[_KT, _VT], **kwargs: _VT) -> None:
        # TODO: guide update
        pass

    def __load(self):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.json")
        with open(schema_path, "r") as f:
            data = json.load(f)
        data["oid"] = str(uuid.uuid4())
        self.update(data)

    def pull(self):
        # TODO: guide pull
        pass

    def push(self):
        # TODO: guide push
        pass

    def duplicate(self, parent=None, mirror=False):
        dup = self.__class__(None, parent if parent else self.parent, self)
        if mirror:
            dup["comp_side"] = "L" if self["comp_side"] == "R" else "R"
            for index, m in enumerate(dup["transforms"]):
                m = pm.datatypes.Matrix(m)
                dup["transforms"][index] = transform.getSymmetricalTransform(m).tolist()
        for comp in self["children"]:
            comp.duplicate(dup, mirror)
        return dup

    def draw_network(self):
        # TODO: guide draw network
        n = pm.createNode("network")
        self._network = n

    def draw_guide(self):
        if not self.network:
            self.draw_network()

    def add_root(self, extension="root", m=pm.datatypes.Matrix()):
        parent = self.parent.guides[int(self["guide_parent_index"])] \
            if len(self.parent.guides) > int(self["guide_parent_index"]) \
            else self.parent.guides[0]
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_{extension}"
        root = icon.axis(parent, name, 1, m=m)
        cube = icon.cube(parent, name, 0.5, 0.5, 0.5, [0, 0, 0], m=m)
        for shp in cube.listRelatives(shapes=True):
            root.addChild(shp, add=True, shape=True)
        pm.delete(cube)
        attribute.addAttribute(root, "is_guide", "bool", keyable=False)
        attribute.setNotKeyableAttributes(root)
        root.attr("displayHandle").set(1)
        for shp in root.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        index = len(self.network.attr("transforms").inputs(type="transform"))
        pm.connectAttr(root.attr("worldMatrix")[0], self.network.attr("transforms")[index])
        return root

    def add_loc(self, parent, extension="", m=pm.datatypes.Matrix()):
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_{extension}"
        root = icon.null(parent, name, 1, [1, 1, 0], m)
        sphere = icon.sphere(parent, name, 0.5, [1, 1, 0], m, degree=3)
        for shp in sphere.listRelatives(shapes=True):
            root.addChild(shp, add=True, shape=True)
        pm.delete(sphere)
        attribute.setNotKeyableAttributes(root)
        root.attr("displayHandle").set(1)
        for shp in root.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        index = len(self.network.attr("transforms").inputs(type="transform"))
        pm.connectAttr(root.attr("worldMatrix")[0], self.network.attr("transforms")[index])
        return root

    def add_blade(self, parent, aim, m=pm.datatypes.Matrix()):
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_blade"
        v0 = pm.datatypes.Vector(0, 0, 0)
        v1 = pm.datatypes.Vector(1 / 2, 0, 0)
        v2 = pm.datatypes.Vector(1, 1 / 4, 0)
        v3 = pm.datatypes.Vector(1 / 2, 1 / 2, 0)
        v4 = pm.datatypes.Vector(0, 1 / 2, 0)
        points = [v0, v1, v2, v3, v4]
        blade = curve.addCurve(parent, name, points, True, 1, m=m)
        icon.setcolor(blade, [1, 0, 0])
        attribute.addAttribute(blade, "blade_offset", "float", 0)
        attribute.addAttribute(blade, "blade_scale", "float", 0)
        attribute.setNotKeyableAttributes(blade, attributes=["blade_offset"])
        aim_cons = pm.aimConstraint(aim,
                                    blade,
                                    offset=(0, 0, 0),
                                    aimVector=(1, 0, 0),
                                    upVector=(0, 1, 0),
                                    worldUpType="objectrotation",
                                    worldUpVector=(0, 1, 0),
                                    worldUpObject=parent)
        pm.connectAttr(blade.attr("blade_offset"), aim_cons.attr("offsetX"))
        pm.connectAttr(blade.attr("blade_scale"), blade.attr("sx"))
        pm.connectAttr(blade.attr("blade_scale"), blade.attr("sy"))
        pm.connectAttr(blade.attr("blade_scale"), blade.attr("sz"))
        attribute.setKeyableAttributes(blade, [])
        for shp in blade.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        aim_cons.attr("isHistoricallyInteresting").set(False)
        pm.connectAttr(blade.attr("worldMatrix")[0], self.network.attr("blade_matrix"))
        pm.connectAttr(blade.attr("blade_offset"), self.network.attr("blade_offset"))
        return blade

    def add_display_curve(self, parent, points):
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_displayCrv"
        points = [pm.datatypes.Vector() for point in points]
        node = curve.addCurve(parent, name, points, False, 1)
        for index, point in enumerate(points):
            mult = pm.createNode("multMatrix")
            decompose = pm.createNode("decomposeMatrix")
            pm.connectAttr(point.attr("worldMatrix")[0], mult.attr("matrixIn")[0])
            pm.connectAttr(node.attr("worldInverseMatrix")[0], mult.attr("matrixIn")[1])
            pm.connectAttr(mult.attr("matrixSum"), decompose.attr("inputMatrix"))
            pm.connectAttr(decompose.attr("outputTranslate"), node.attr("controlPoints")[index])
        node.attr("overrideEnabled").set(1)
        node.attr("overrideDisplayType").set(1)
        attribute.setKeyableAttributes(node, [])
        for shp in node.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        return node


class Blueprint:

    @property
    def blueprint(self):
        return self._blueprint

    @blueprint.setter
    def blueprint(self, bp):
        self._blueprint = bp

    def __init__(self, blueprint=None):
        self._blueprint = blueprint

    def __load(self, data):
        result = list()
        traversal(data,
                  lambda x: ([y["oid"] for y in x["children"]], import_component_module(x["comp_type"], True).Guide()),
                  lambda x: x["children"],
                  result)
        child_oid_list, comp_list = [x for x in result]

    def find_component(self, oid):
        if not self.blueprint:
            return None
        result = list()
        traversal(self.blueprint,
                  lambda x: x if x["oid"] == oid else None,
                  lambda x: x["children"],
                  result)
        result = list(filter(lambda x: x, result))
        return result[0] if result else None

    def new_component(self, parent, parent_comp_oid, new_comp_type, draw=False):
        mod = import_component_module(new_comp_type, True)
        parent_comp = self.find_component(parent_comp_oid)
        if not parent_comp:
            assembly_mod = import_component_module("assembly", True)
            parent_comp = assembly_mod()
        new_comp = mod.Guide(parent_comp)
        if not new_comp.valid:
            return
        self._blueprint = parent_comp
        self.set_index(new_comp["comp_name"], new_comp["comp_side"], new_comp["index"], new_comp)
        if draw:
            self.draw_guide()
            if parent:
                pm.parent(pm.selected(), parent)

    def duplicate_component(self, oid, mirror=False, draw=False):
        comp = self.find_component(oid)
        if mirror:
            result = list()
            traversal(comp,
                      lambda x: f"{x['comp_name']}_{x['comp_side']}{x['comp_index']}_root" if x["comp_side"] == "C" else None,
                      lambda x: x["children"],
                      result)
            center_components = list(filter(lambda x: x, result))
            if center_components:
                logger.warning("selected component tree have side 'C'")
                [logger.warning(x) for x in center_components]
                return
        dup_comp = comp.duplicate(mirror=mirror)
        traversal(dup_comp,
                  lambda x: self.set_index(x["comp_name"], x["comp_side"], x["comp_index"], x),
                  lambda x: x["children"],
                  [])
        if draw:
            self.draw_guide()

    def combine_component(self, parent_comp, child_comp):
        if child_comp.is_assembly:
            # TODO: combine assembly info
            pass

        child_comp = child_comp["children"] if child_comp.is_assembly else [child_comp]
        for child in child_comp:
            child.parent = parent_comp
            result = list()
            traversal(child,
                      lambda x: x,
                      lambda x: x["children"],
                      result)
            for comp in list(filter(lambda x: x, result)):
                self.set_index(comp["comp_name"], comp["comp_side"], comp["comp_index"], comp)

    def set_index(self, name, side, index, target_comp):
        result = list()
        lambda_exp = (lambda x: x["comp_index"] if (x["comp_name"] == name) and (x["comp_side"] == side) and (
                x is not target_comp) else None)
        traversal(self.blueprint,
                  lambda_exp,
                  lambda x: x["children"],
                  result)
        result = list(filter(lambda x: x, result))
        while True:
            if index not in result:
                break
            index += 1

        return index

    def pull(self):
        traversal(self.blueprint,
                  lambda x: x.pull() if x.guides else None,
                  lambda x: x["children"],
                  [])

    def push(self):
        with pm.UndoChunk():
            traversal(self.blueprint,
                      lambda x: x.push() if x.guides else None,
                      lambda x: x["children"],
                      [])

    def draw_guide(self):
        with pm.UndoChunk():
            result = list()
            traversal(self.blueprint,
                      lambda x: x.draw_guide() if not x.guides else None,
                      lambda x: x["children"],
                      result)
            result = list(filter(lambda x: x, result))
            pm.select(result[-1]) if result else None

    def draw_rig(self):
        with pm.UndoChunk():
            build_system = BuildSystem(self.blueprint)
            build_system.build()


def import_blueprint():
    # TODO: import blueprint
    pass


def export_blueprint():
    # TODO: export blueprint
    pass


def blueprint_from_guide():
    # TODO: blueprint from guide
    pass


def blueprint_from_rig():
    # TODO: blueprint from rig
    pass
