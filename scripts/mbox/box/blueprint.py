# -*- coding: utf-8 -*-

# built-in
import json
import os
import inspect
from uuid import uuid4

# maya
from pymel import core as pm

# mbox
from mbox import logger
from mbox.core import uuid, vector, transform, icon, attribute, curve
from .build import BuildSystem
from .utils import Selection, Naming, traversal, import_component_module


class Component(dict):

    @property
    def assembly(self):
        component = self
        while component.parent:
            component = component.parent
        return component

    @property
    def is_assembly(self):
        return False

    @property
    def valid(self):
        return self._valid

    @property
    def chain(self):
        # TODO: guide chain
        ui = exec_window()
        if ui:
            axis = ui.dir_axis
            offset = ui.spacing
            number = ui.sections_number
            if axis == 0:  # X
                offVec = pm.datatypes.Vector(offset, 0, 0)
            elif axis == 3:  # -X
                offVec = pm.datatypes.Vector(offset * -1, 0, 0)
            elif axis == 1:  # Y
                offVec = pm.datatypes.Vector(0, offset, 0)
            elif axis == 4:  # -Y
                offVec = pm.datatypes.Vector(0, offset * -1, 0)
            elif axis == 2:  # Z
                offVec = pm.datatypes.Vector(0, 0, offset)
            elif axis == 5:  # -Z
                offVec = pm.datatypes.Vector(0, 0, offset * -1)

            newPosition = pm.datatypes.Vector(0, 0, 0)
            pos_list = [newPosition]
            for i in range(number):
                newPosition = offVec + newPosition
                pos_list.append(newPosition)
            self["guide_transforms"] = [transform.getTransformFromPos(x).tolist() for x in pos_list]
        guide_transforms = list()
        return guide_transforms if guide_transforms else "#"

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
    def naming(self):
        return self.assembly._naming

    @property
    def guides(self):
        return Selection(self.network).guides if self.network else []

    @property
    def ui_host(self):
        return Selection(self.network).ui_host if self.network else []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        if self._parent:
            self._parent["children"].remove(self)
        self._parent = p
        self._parent["children"].append(self)

    def __init__(self, network=None, parent=None, data=None, chain_number=0):
        super(Component, self).__init__()
        self["children"] = list()
        self._parent = parent
        if self._parent:
            self._parent["children"].append(self)
        self.update(data) if data else self.schema()
        self._network = network
        self._valid = True
        if self.is_assembly:
            self._naming = Naming(self)
        else:
            if self["guide_transforms"] == "#":
                # index 0 - root, index 1 ~ ... - loc, + specify loc
                self["guide_transforms"] = [transform.getTransformFromPos(pm.datatypes.Vector(1, 0, 0) * i).tolist()
                                            for i in range(chain_number + 1)] if chain_number else self.chain
                if self["guide_transforms"] == "#":
                    self._valid = False
        if self.network:
            self.pull()

    def update(self, __m, **kwargs):
        for _K, _V in __m.items():
            if _K == "children" or _K == "uuid":
                continue
            self[_K] = _V
        for _K, _V in kwargs.items():
            if _K == "children" or _K == "uuid":
                continue
            self[_K] = _V
        if "children" in __m:
            if __m["children"]:
                for child_data in __m["children"]:
                    mod = import_component_module(child_data["comp_type"], True)
                    comp = mod.Guide(parent=self)
                    comp.update(child_data)

    def schema(self):
        if not self.is_assembly:
            schema_path = os.path.join(os.getenv("MBOX_PYTHON"), "box", "modules", "schema.json")
            with open(schema_path, "r") as f:
                data = json.load(f)
            self.update(data)
        schema_path = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "schema.json")
        with open(schema_path, "r") as f:
            data = json.load(f)
        self.update(data)
        if "uuid" not in self:
            self["uuid"] = str(uuid4())

    def pull(self):
        self["uuid"] = uuid.get_uuid(self.network)
        self["comp_type"] = self.network.attr("comp_type").get()
        self["comp_name"] = self.network.attr("comp_name").get()
        self["comp_side"] = self.network.attr("comp_side").get(asString=True)
        self["comp_index"] = int(self.network.attr("comp_index").get())
        self["ref_parent_index"] = int(self.network.attr("ref_parent_index").get())
        self["jnt_parent_index"] = int(self.network.attr("jnt_parent_index").get())
        self["jnt_names"] = self.network.attr("jnt_names").get()
        self["jnt_rot_off"] = [float(self.network.attr("jnt_rot_offX").get()),
                               float(self.network.attr("jnt_rot_offY").get()),
                               float(self.network.attr("jnt_rot_offZ").get())]
        self["ui_host"] = self.network.attr("ui_host").get()
        self["connector"] = self.network.attr("connector").get()
        self["blend_jnt"] = self.network.attr("blend_jnt").get()
        self["support_jnt"] = self.network.attr("support_jnt").get()
        self["override_color"] = self.network.attr("override_color").get()
        self["color_fk"] = self.network.attr("color_fk").get()
        self["color_ik"] = self.network.attr("color_ik").get()
        self["use_RGB_color"] = self.network.attr("use_RGB_color").get()
        self["RGB_fk"] = self.network.attr("RGB_fk").get()
        self["RGB_ik"] = self.network.attr("RGB_ik").get()
        self["guide_transforms"] = [x.tolist() for x in self.network.attr("guide_transforms").get()]
        if self.guides:
            parent = self.guides[0].getParent()
            plug = parent.attr("worldMatrix")[0].outputs(type="network", plugs=True)
            self["guide_parent_index"] = plug[0].index() if plug else -1

    def push(self):
        uuid.set_uuid(self["uuid"], self.network)
        self.network.attr("comp_type").set(self["comp_type"])
        self.network.attr("comp_name").set(self["comp_name"])
        self.network.attr("comp_side").set(self["comp_side"])
        self.network.attr("comp_index").set(self["comp_index"])
        self.network.attr("ref_parent_index").set(self["ref_parent_index"])
        self.network.attr("jnt_parent_index").set(self["jnt_parent_index"])
        self.network.attr("jnt_names").set(self["jnt_names"])
        self.network.attr("jnt_rot_offX").set(self["jnt_rot_off"][0])
        self.network.attr("jnt_rot_offY").set(self["jnt_rot_off"][1])
        self.network.attr("jnt_rot_offZ").set(self["jnt_rot_off"][2])
        self.network.attr("ui_host").set(self["ui_host"])
        self.network.attr("connector").set(self["connector"])
        self.network.attr("blend_jnt").set(self["blend_jnt"])
        self.network.attr("support_jnt").set(self["support_jnt"])
        self.network.attr("override_color").set(self["override_color"])
        self.network.attr("color_fk").set(self["color_fk"])
        self.network.attr("color_ik").set(self["color_ik"])
        self.network.attr("use_RGB_color").set(self["use_RGB_color"])
        self.network.attr("RGB_fk").set(self["RGB_fk"])
        self.network.attr("RGB_ik").set(self["RGB_ik"])
        [self.network.attr("guide_transforms")[i].set(t)
         if not self.network.attr("guide_transforms")[i].inputs()
         else self.network.attr("guide_transforms")[i].inputs()[0].setMatrix(pm.datatypes.Matrix(t), worldSpace=True)
         for i, t in enumerate(self["guide_transforms"])]
        guides = self.guides
        if guides:
            parent = guides[0].getParent()
            parent_guides = Selection(parent).guides
            if self["guide_parent_index"] < len(parent_guides):
                pm.parent(guides[0], parent_guides[self["guide_parent_index"]])
            else:
                pm.parent(guides[0], parent_guides[-1])
            for guide in guides:
                name = guide.nodeName().split("_")
                name[0] = self["comp_name"]
                name[1] = f"{self['comp_side']}{self['comp_index']}"
                guide.rename("_".join(name))

    def draw_network(self):
        old = uuid.find(self["uuid"])
        if old:
            pm.delete(old)
        n = self._network = pm.createNode("network")
        uuid.set_uuid(self["uuid"], n)
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "comp_type", "string", self["comp_type"])
        attribute.addAttribute(n, "comp_name", "string", self["comp_name"])
        attribute.addEnumAttribute(n, "comp_side", self["comp_side"], ["C", "L", "R"], keyable=False)
        attribute.addAttribute(n, "comp_index", "long", self["comp_index"], keyable=False)
        attribute.addAttribute(n, "ref_parent_index", "long", self["ref_parent_index"], keyable=False)
        attribute.addAttribute(n, "jnt_parent_index", "long", self["jnt_parent_index"], keyable=False)
        attribute.addAttribute(n, "jnt_names", "string", self["jnt_names"])
        attribute.addAttribute(n, "jnt_rot_offX", "doubleAngle", self["jnt_rot_off"][0], minValue=0, maxValue=360,
                               keyable=False)
        attribute.addAttribute(n, "jnt_rot_offY", "doubleAngle", self["jnt_rot_off"][1], minValue=0, maxValue=360,
                               keyable=False)
        attribute.addAttribute(n, "jnt_rot_offZ", "doubleAngle", self["jnt_rot_off"][2], minValue=0, maxValue=360,
                               keyable=False)
        attribute.addAttribute(n, "ui_host", "string", self["ui_host"])
        attribute.addAttribute(n, "blend_jnt", "string", self["blend_jnt"])
        attribute.addAttribute(n, "support_jnt", "string", self["support_jnt"])
        attribute.addAttribute(n, "override_color", "bool", self["override_color"], keyable=False)
        attribute.addAttribute(n, "color_fk", "long", self["color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "color_ik", "long", self["color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "use_RGB_color", "bool", self["use_RGB_color"], keyable=False)
        attribute.addColorAttribute(n, "RGB_fk", self["RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "RGB_ik", self["RGB_ik"], keyable=False)
        pm.addAttr(n, longName="guide_transforms", type="matrix", multi=True)
        pm.addAttr(n, longName="ctls", type="message", multi=True)
        pm.addAttr(n, longName="jnts", type="message", multi=True)
        attribute.addAttribute(n, "connector", "string", self["connector"])

    def draw_guide(self):
        if not self.network:
            self.draw_network()

    def duplicate(self, parent=None, mirror=False):
        dup = self.__class__(None, parent if parent else self.parent, self)
        if mirror:
            dup["comp_side"] = "L" if self["comp_side"] == "R" else "R"
            for index, m in enumerate(dup["guide_transforms"]):
                m = pm.datatypes.Matrix(m)
                dup["guide_transforms"][index] = transform.getSymmetricalTransform(m).tolist()
        for comp in self["children"]:
            comp.duplicate(dup, mirror)
        return dup

    def add_root(self, m=pm.datatypes.Matrix()):
        parent = self.parent.guides[int(self["guide_parent_index"])] \
            if len(self.parent.guides) > int(self["guide_parent_index"]) \
            else self.parent.guides[0]
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_root"
        root = icon.axis(parent, name, 1, m=m)
        for shp in root.listRelatives(shapes=True):
            shp.attr("lineWidth").set(2)
        cube = icon.create(parent, name, icon="cube", w=0.5, h=0.5, d=0.5, color=[1.0, 0.0, 0.0], m=m)
        for shp in cube.listRelatives(shapes=True):
            root.addChild(shp, add=True, shape=True)
        pm.delete(cube)
        attribute.addAttribute(root, "is_guide", "bool", keyable=False)
        attribute.setNotKeyableAttributes(root)
        root.attr("displayHandle").set(1)
        for shp in root.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        index = len(self.network.attr("guide_transforms").inputs(type="transform"))
        pm.connectAttr(root.attr("worldMatrix")[0], self.network.attr("guide_transforms")[index])
        pm.connectAttr(root.attr("message"), self.network.attr("guide"))
        return root

    def add_loc(self, parent, m=pm.datatypes.Matrix()):
        index = len(self.network.attr("guide_transforms").inputs(type="transform"))
        name = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_loc{index}"
        root = icon.null(parent, name, 1, color=[1, 1, 0], m=m)
        sphere = icon.sphere(parent, name, 0.5, color=[1, 1, 0], m=m, degree=3)
        for shp in sphere.listRelatives(shapes=True):
            root.addChild(shp, add=True, shape=True)
        pm.delete(sphere)
        attribute.setNotKeyableAttributes(root)
        root.attr("displayHandle").set(1)
        for shp in root.getShapes():
            shp.attr("isHistoricallyInteresting").set(False)
        index = len(self.network.attr("guide_transforms").inputs(type="transform"))
        pm.connectAttr(root.attr("worldMatrix")[0], self.network.attr("guide_transforms")[index])
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
        centers = [pm.datatypes.Vector() for point in points]
        node = curve.addCurve(parent, name, centers, False, 1)
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
                  lambda x: (
                      [y["uuid"] for y in x["children"]], import_component_module(x["comp_type"], True).Guide(data=x)),
                  lambda x: x["children"],
                  result)
        child_uuid_list, comp_list = zip(*result)
        for index, comp in enumerate(comp_list):
            for child_uuid in child_uuid_list[index]:
                for comp2 in comp_list:
                    if child_uuid == comp2["uuid"]:
                        comp2.parent = comp
        self._blueprint = comp_list[0]

    def find_component(self, uuid):
        if not self.blueprint:
            return
        if not uuid:
            return
        result = list()
        traversal(self.blueprint,
                  lambda x: x if x["uuid"] == uuid else None,
                  lambda x: x["children"],
                  result)
        result = list(filter(lambda x: x, result))
        return result[0] if result else None

    def new_component(self, parent, new_comp_type, draw=False, **kwargs):
        mod = import_component_module(new_comp_type, True)
        if not self.blueprint or not parent:
            assembly_mod = import_component_module("assembly", True)
            self._blueprint = assembly_mod.Guide()
            mod.Guide(parent=self.blueprint)
        else:
            if isinstance(parent, pm.PyNode):
                parent = parent.fullPath()
            parent_uuid = Selection(parent).uuid
            parent_comp = self.find_component(parent_uuid)
            new_comp = mod.Guide(parent=parent_comp, **kwargs)
            self.set_index(new_comp["comp_name"], new_comp["comp_side"], new_comp["comp_index"], new_comp)
            offset_t = pm.PyNode(parent).getTranslation(space="world")
            for index, t in enumerate(new_comp["guide_transforms"]):
                m = pm.datatypes.Matrix(t)
                new_comp["guide_transforms"][index] = transform.setMatrixPosition(m, m.translate + offset_t)
        if draw:
            self.draw_guide()
            if parent:
                if pm.selected()[0].getParent() != parent:
                    pm.parent(pm.selected(), parent)

    def duplicate_component(self, uuid, mirror=False, draw=False):
        comp = self.find_component(uuid)
        if mirror:
            result = list()
            traversal(comp,
                      lambda x: f"{x['comp_name']}_{x['comp_side']}{x['comp_index']}_root" if x[
                                                                                                  "comp_side"] == "C" else None,
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
        lambda_exp = (lambda x:
                      x["comp_index"]
                      if (x["comp_name"] == name) and (x["comp_side"] == side) and (x != target_comp)
                      else None)
        traversal(self.blueprint,
                  lambda_exp,
                  lambda x: x["children"],
                  result)
        result = list(filter(lambda x: x is not None, result))
        while True:
            if index not in result:
                break
            index += 1
        if target_comp:
            target_comp["comp_index"] = index
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

    def draw_network(self):
        with pm.UndoChunk():
            traversal(self.blueprint,
                      lambda x: x.draw_network() and x.push() if not x.network else None,
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
            self.draw_network()
            build_system = BuildSystem(self.blueprint)
            build_system.build()


def import_blueprint(path):
    if not path:
        # TODO: get path
        return
    with open(path, "r") as f:
        data = json.load(f)
    mod = import_component_module("assembly", True)
    blueprint = mod.Guide(data=data)
    return blueprint


def export_blueprint(path, blueprint):
    if not path:
        # TODO: get path
        return
    with open(path, "w") as f:
        json.dump(blueprint, f)


def blueprint_from_guide(node):
    if not node:
        selected = pm.selected(type="transform")
        if selected:
            node = selected[0]
    else:
        node = pm.PyNode(node)
    assembly = Selection(node).assembly_guide
    result = list()
    traversal(assembly,
              lambda x: (
                  [Selection(y).uuid for y in Selection(x).child_guides],
                  import_component_module(Selection(x).comp_type, True).Guide(network=Selection(x).network)),
              lambda x: Selection(x).child_guides,
              result)
    child_uuid_list, comp_list = zip(*result)
    for index, comp in enumerate(comp_list):
        for child_uuid in child_uuid_list[index]:
            for comp2 in comp_list:
                if child_uuid == comp2["uuid"]:
                    comp2.parent = comp
    blueprint = Blueprint(comp_list[0])
    blueprint.pull()
    return blueprint


def blueprint_from_rig(node):
    if not node:
        selected = pm.selected(type="transform")
        if selected:
            node = selected[0]
    else:
        node = pm.PyNode(node)
    network = Selection(node).network
    result = list()
    traversal(network,
              lambda x: (
                  [Selection(y).uuid for y in x.attr("affects")[0].outputs(type="network")],
                  import_component_module(Selection(x).comp_type, True).Guide(network=x)),
              lambda x: x.attr("affects")[0].outputs(type="network"),
              result)
    child_uuid_list, comp_list = zip(*result)
    assembly = comp_list[0]
    for index, comp in enumerate(comp_list):
        for child_uuid in child_uuid_list[index]:
            for comp2 in comp_list:
                if child_uuid == comp2["uuid"]:
                    comp2.parent = comp
    if not assembly.is_assembly:
        mod = import_component_module("assembly", True)
        assembly = mod.Guide(network=Selection(node.getParent(generations=-1)).network)
        comp_list[0].parent = assembly
    blueprint = Blueprint(assembly)
    blueprint.pull()
    return blueprint
