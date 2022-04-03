# -*- coding: utf-8 -*-

# built-in
import importlib
import itertools
import os
import sys

# maya
from pymel import core as pm

# mbox
from mbox import logger

# mgear
from mgear.core import primitive, transform, attribute, applyop


# mbox.__init__.py
MBOX_ROOT = os.getenv("MBOX_ROOT")
MBOX_MODULES = os.getenv("MBOX_MODULES")
MBOX_CUSTOM_MODULES = os.getenv("MBOX_CUSTOM_MODULES")

# sys path append
# load_block_module import component
if MBOX_MODULES not in sys.path:
    sys.path.append(MBOX_MODULES)
for path in MBOX_CUSTOM_MODULES.split(";"):
    if path not in sys.path:
        sys.path.append(path)


def traversal(node, func1, get_child_func, result):
    result.append(func1(node))
    for child_node in get_child_func(node):
        traversal(child_node, func1, get_child_func, result)


def is_guide(node: pm.PyNode):
    return node if node.hasAttr("is_guide") else None


def is_rig(node: pm.PyNode):
    return node if node.hasAttr("is_rig") else None


def is_network(node: pm.PyNode):
    return node if node.hasAttr("comp_type") else None


def is_ctl(node: pm.PyNode):
    return node if node.hasAttr("is_ctl") else None


def is_jnt(node: pm.PyNode):
    return node if node.hasAttr("is_jnt") else None


def get_component_modules():
    result = dict()
    module_dir = [d for d in os.listdir(MBOX_MODULES)
                  if os.path.isdir(os.path.join(MBOX_MODULES, d)) and "__pycache__" not in d]
    clean_module_dir = list(set(module_dir))
    if len(clean_module_dir) != len(module_dir):
        logger.warning("Exists same module in MBOX_MODULES")
    result[MBOX_MODULES] = clean_module_dir
    if os.path.exists(MBOX_CUSTOM_MODULES):
        custom_module_dir = [d for d in os.listdir(MBOX_CUSTOM_MODULES)
                             if os.path.isdir(os.path.join(MBOX_CUSTOM_MODULES, d)) and "__pycache__" not in d]
        clean_custom_module_dir = list(set(custom_module_dir))
        if len(clean_custom_module_dir) != len(custom_module_dir):
            logger.warning("Exists same module in MBOX_CUSTOM_MODULES")
        if len(list(set(clean_custom_module_dir + clean_module_dir))) != len(module_dir + custom_module_dir):
            logger.warning("Exists same module")
        result[MBOX_CUSTOM_MODULES] = clean_custom_module_dir
    return result


def import_component_module(comp_type, guide):
    modules = get_component_modules()
    valid = False
    for modules_list in modules.values():
        if comp_type in modules_list:
            valid = True
    if not valid:
        logger.warning(f"{comp_type} is invalid")
    mod = importlib.import_module(f"{comp_type}.guide" if guide else f"{comp_type}.rig")
    return mod


def add_jnt(parent, ref, name, uni_scale, **kwargs):
    rot_off = kwargs["rot_off"] if "rot_off" in kwargs else [0, 0, 0]
    parents = pm.ls(kwargs["dag_tree"], dagObjects=True, type="transform") if "dag_tree" in kwargs else pm.ls(type="transform")
    p_list = [p for p in parents if parent == p.nodeName()]
    parent = p_list[0] if p_list else None

    if pm.ls(name) and "connect_joints" in kwargs:
        jnt = pm.ls(name)[0]
        keep_off = True
    else:
        if isinstance(ref, pm.datatypes.Matrix):
            t = ref
        else:
            t = transform.getTransform(ref)
        jnt = primitive.addJoint(parent,
                                 name,
                                 t)
        keep_off = False

    # check if already have connections
    # for example Mehahuman twist joint already have connections
    if not jnt.translate.listConnections(d=False):
        # Disconnect inversScale for better preformance
        if isinstance(parent, pm.nodetypes.Joint):
            try:
                pm.disconnectAttr(
                    parent.scale, jnt.inverseScale)

            except RuntimeError:
                # This handle the situation where we have in between
                # joints transformation due a negative scaling
                if not isinstance(jnt, pm.nodetypes.Joint):
                    pm.ungroup(jnt.getParent())

        if keep_off:
            driver = primitive.addTransform(
                ref,
                name=ref.name() + "_offset_t")
            transform.matchWorldTransform(jnt, driver)
            rot_off = [0, 0, 0]

        else:
            if isinstance(ref, pm.datatypes.Matrix):
                driver = None
                jnt.setMatrix(ref, worldSpace=True)

            else:
                driver = ref
                rot_off = rot_off

        if driver:
            cns_m = applyop.gear_matrix_cns(
                driver, jnt, rot_off=rot_off)

            # invert negative scaling in Joints. We only inver Z axis,
            # so is the only axis that we are checking
            if jnt.scaleZ.get() < 0:
                cns_m.scaleMultZ.set(-1.0)
                cns_m.rotationMultX.set(-1.0)
                cns_m.rotationMultY.set(-1.0)

            # if unifor scale is False by default. It can be forced
            # using uniScale arg or set from the ui
            if uni_scale:
                jnt.disconnectAttr("scale")
                pm.connectAttr(cns_m.scaleZ, jnt.sx)
                pm.connectAttr(cns_m.scaleZ, jnt.sy)
                pm.connectAttr(cns_m.scaleZ, jnt.sz)
        else:
            cns_m = None

        # Segment scale compensate Off to avoid issues with the
        # global scale
        jnt.setAttr("segmentScaleCompensate", False)

        if not keep_off:
            # setting the joint orient compensation in order to
            # have clean rotation channels
            jnt.setAttr("jointOrient", 0, 0, 0)
            if cns_m:
                m = cns_m.drivenRestMatrix.get()
            else:
                driven_m = pm.getAttr(jnt + ".parentInverseMatrix[0]")
                m = t * driven_m
                jnt.attr("rotateX").set(0)
                jnt.attr("rotateY").set(0)
                jnt.attr("rotateZ").set(0)
                if jnt.scaleZ.get() < 0:
                    jnt.scaleZ.set(1)
            tm = pm.datatypes.TransformationMatrix(m)
            r = pm.datatypes.degrees(tm.getRotation())
            jnt.attr("jointOrientX").set(r[0])
            jnt.attr("jointOrientY").set(r[1])
            jnt.attr("jointOrientZ").set(r[2])

        # set not keyable
        attribute.setNotKeyableAttributes(jnt)


class Naming:

    def __init__(self, component=None):
        self.component = component

    def name(self, comp, ctl=True, description="", extension=""):
        if not ctl:
            rule = self.component["jnt_name_rule"]
            padding = self.component["jnt_index_padding"]
            description_letter_case = self.component["jnt_description_letter_case"]
            side_set = [self.component["jnt_L_name"], self.component["jnt_R_name"], self.component["jnt_C_name"]]
            if not extension:
                extension = self.component["jnt_name_ext"]
        else:
            rule = self.component["ctl_name_rule"]
            padding = self.component["ctl_index_padding"]
            description_letter_case = self.component["ctl_description_letter_case"]
            side_set = [self.component["ctl_L_name"], self.component["ctl_R_name"], self.component["ctl_C_name"]]
            if not extension:
                extension = self.component["ctl_name_ext"]

        if description_letter_case == "lower":
            description = description.lower()
        elif description_letter_case == "upper":
            description = description.upper()
        elif description_letter_case == "capitalize":
            description = description.capitalize()
        index_filter = ["L", "R", "C"]
        side = side_set[index_filter.index(comp["comp_side"])]
        name = rule.format(comp_name=comp["comp_name"],
                           comp_side=side,
                           comp_index=str(comp["comp_index"]).zfill(padding),
                           description=description,
                           extension=extension)
        name = "_".join([x for x in name.split("_") if x])
        return name

    def inspect_jnt_names(self):
        result = list()
        traversal(self.component,
                  lambda x: x.jnt_names,
                  lambda x: x["children"],
                  result)
        valid = True
        invalid_msg = str()
        jnt_names = itertools.chain(*result)
        for name in jnt_names:
            if pm.objExists(name):
                if self.component["connect_jnts"]:
                    logger.info(f"already exists : {name}")
                valid = False
                jnt = pm.PyNode(name)
                if jnt.attr("r").get() != (0, 0, 0):
                    invalid_msg += f"{jnt} rotate : {jnt.attr('r').get()}\n"
        return True if self.component["connect_jnts"] and not invalid_msg else valid


class Selection:

    @property
    def is_guide(self):
        return True if is_guide(self.node) else False

    @property
    def is_rig(self):
        return True if is_rig(self.node) else False

    @property
    def network(self):
        node = self.valid(self.node)
        if node:
            if is_network(node):
                return node
            network = node.attr("message").outputs(type="network")
            if network:
                return network[0]

    @property
    def comp_type(self):
        return self.network.attr("comp_type").get() if self.network else None

    @property
    def oid(self):
        return self.network.attr("oid").get() if self.network else None

    @property
    def guides(self):
        guides = list()
        if self.network:
            guides = self.network.attr("guide_transforms").inputs(type="transform")
            if self.network.attr("comp_type").get() == "assembly":
                guides = self.network.attr("guide").inputs(type="transform")
        return guides

    @property
    def child_guides(self):
        child_guides = list()
        guides = self.guides
        for guide in guides:
            child = guide.getChildren(type="transform")
            for c in child:
                if is_guide(c):
                    child_guides.append(c)
        return child_guides

    @property
    def ui_host(self):
        node = None
        if is_network(self.node):
            node = self.node.attr("ctls").inputs(type="transform")
            if node:
                node = node[0]
        elif is_ctl(self.node):
            node = self.node
        if node:
            ui_host = node.attr("ui_host").inputs(type="transform")
            if ui_host:
                return ui_host[0]

    @property
    def assembly_guide(self):
        if isinstance(self.node, pm.nodetypes.Transform):
            assembly = self.node.getParent(generations=-1)
            if is_guide(assembly):
                return assembly

    @property
    def assembly_rig(self):
        if isinstance(self.node, pm.nodetypes.Transform):
            assembly = self.node.getParent(generations=-1)
            if is_rig(assembly):
                return assembly

    @property
    def ctl_hierarchy(self):
        result = list()
        if is_ctl(self.node):
            traversal(self.node,
                      lambda x: x,
                      lambda x: pm.controller(x, query=True, children=True) if pm.controller(x, query=True, children=True) else [],
                      result)
        return list(result)

    @property
    def jnt_hierarchy(self):
        result = list()
        if is_jnt(self.node):
            traversal(self.node,
                      lambda x: x,
                      lambda x: x.getChildren(type="joint"),
                      result)
        return list(result)

    def __init__(self, node):
        """self.node is guide or rig or network"""
        self.node = None
        if node:
            self.node = node if isinstance(node, pm.PyNode) else pm.PyNode(node)

    @staticmethod
    def valid(node):
        while node:
            if is_guide(node) or is_rig(node) or is_network(node):
                break
            node = node.getParent()
        return node
