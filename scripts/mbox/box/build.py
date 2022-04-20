# -*- coding: utf-8 -*-

# build-in
import importlib
import itertools

# maya
from pymel import core as pm

# mbox
from mbox import logger
from .utils import traversal, import_component_module, add_jnt

# mgear
from mgear.core import attribute, transform, icon, primitive, node, applyop


class Context(list):

    @property
    def assembly(self):
        return self._assembly

    @assembly.setter
    def assembly(self, assembly):
        self._assembly = assembly

    def __init__(self):
        super(Context, self).__init__()
        self._assembly = None

    def instance(self, oid):
        instance = list(filter(lambda ins: ins.component["oid"] == oid, self))
        return instance[0] if instance else None


class Instance:

    @property
    def component(self):
        return self._component

    @property
    def context(self):
        return self._context

    @property
    def root(self):
        return self._root

    @property
    def ctls(self):
        return self._ctls

    @property
    def refs(self):
        return self._refs

    @property
    def jnts(self):
        # jnts[0] = [parent, ref, uniform scale,
        return self._jnts

    @property
    def ui_host(self):
        if self.component["ui_host"]:
            _, index, oid = self.component["ui_host"].split(",")
            ui_host = self.context.instance(oid).ctls[int(index)]
        else:
            ui_host = self.context.assembly.ctls[0]
        div_attr_name = f"{self.component['comp_name']}_{self.component['comp_side']}{self.component['comp_index']}"
        if not pm.attributeQuery(div_attr_name, node=ui_host, exists=True):
            attribute.addEnumAttribute(ui_host, div_attr_name, 0, [" "])
            attribute.setNotKeyableAttributes(ui_host, [div_attr_name])
        return ui_host

    @property
    def comp_parent_ref(self):
        parent_component = self.component.parent
        parent_instance = None
        while parent_component:
            parent_instance = self.context.instance(parent_component["oid"])
            if parent_instance.refs:
                break
            parent_component = parent_component.parent
        if parent_instance:
            if self.component["ref_parent_index"] > -1:
                if int(self.component["ref_parent_index"]) < len(parent_instance.refs):
                    return parent_instance.refs[int(self.component["ref_parent_index"])]
            if int(self.component["guide_parent_index"]) < len(parent_instance.comp_ref_parent_dict):
                return parent_instance.comp_ref_parent_dict[int(self.component["guide_parent_index"])]
            return parent_instance.refs[-1]

    @property
    def comp_parent_jnt(self):
        parent_instance = None
        component = self.component
        while component.parent:
            parent_instance = self.context.instance(component.parent["oid"])
            if parent_instance.jnts:
                break
            component = component.parent
        if parent_instance.jnts:
            if self.component["jnt_parent_index"] > -1:
                if int(self.component["jnt_parent_index"]) < len(parent_instance.jnts):
                    return parent_instance.jnts[int(self.component["jnt_parent_index"])]
            if self.component["ref_parent_index"] > -1:
                if int(self.component["ref_parent_index"]) < len(parent_instance.jnts):
                    return parent_instance.jnts[int(self.component["ref_parent_index"])]
            if int(self.component["guide_parent_index"]) < len(parent_instance.comp_jnt_parent_dict):
                return parent_instance.comp_jnt_parent_dict[int(self.component["guide_parent_index"])]
            return parent_instance.jnts[-1][2]
        return None

    def __init__(self, context, component=None):
        self._root = None
        self._ctls = list()
        self._refs = list()
        self._jnts = list()
        self._component = component
        self._context = context
        self._context.append(self)
        if self.component.is_assembly:
            self._context.assembly = self
        self.comp_ref_parent_dict = dict()
        self.comp_jnt_parent_dict = dict()

    def add_root(self, m=pm.datatypes.Matrix()):
        naming = self.component.assembly.naming
        parent = self.comp_parent_ref
        name = naming.name(self.component, False, extension="root") if self.component.parent else self.component["name"]
        root = primitive.addTransform(parent, name, m)
        attribute.addAttribute(root, "is_rig", "bool", keyable=False)
        attribute.setKeyableAttributes(root, [])
        pm.connectAttr(root.attr("message"), self.component.network.attr("rig"), force=True)
        self._root = root
        return root

    def add_loc(self, parent, description, m):
        naming = self.component.assembly.naming
        loc = primitive.addTransform(parent,
                                     naming.name(
                                         self.component,
                                         False,
                                         description=description,
                                         extension="loc"),
                                     m=m)
        attribute.setKeyableAttributes(loc, [])
        return loc

    def add_ctl(self, parent, parent_ctl, color, ctl_attr, npo_attr, description, cns, m, **kwargs):
        naming = self.component.assembly.naming
        ctl_attr = ctl_attr if ctl_attr else ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"]
        npo_attr = npo_attr if npo_attr else ["v"]
        if cns:
            parent = primitive.addTransform(parent,
                                            f"{kwargs['name']}_cns" if "name" in kwargs else naming.name(
                                                self.component,
                                                False,
                                                description=description,
                                                extension="cns"),
                                            m=m)
        npo = primitive.addTransform(parent,
                                     f"{kwargs['name']}_npo" if "name" in kwargs else naming.name(
                                         self.component,
                                         False,
                                         description=description,
                                         extension="npo"),
                                     m=m)
        attribute.setKeyableAttributes(npo, npo_attr)
        ctl = icon.create(npo,
                          f"{kwargs['name']}_{self.component['ctl_name_ext']}" if "name" in kwargs else naming.name(
                              self.component,
                              False,
                              description=description),
                          color=color,
                          icon=kwargs["icon"] if "icon" in kwargs else "cube",
                          w=kwargs["w"],
                          h=kwargs["h"],
                          d=kwargs["d"],
                          m=m)
        attribute.addAttribute(ctl, "is_ctl", "bool", keyable=False)
        attribute.addAttribute(ctl, "ui_host", "message")
        attribute.setKeyableAttributes(ctl, ctl_attr)
        pm.connectAttr(ctl.attr("message"), self.component.network.attr("ctls")[len(self.ctls)], force=True)
        tag = node.add_controller_tag(ctl, parent_ctl)
        tag.attr("visibilityMode").set(1)
        self._ctls.append(ctl)
        return ctl

    def add_ref(self, parent, description, m):
        naming = self.component.assembly.naming
        ref = primitive.addTransform(parent,
                                     naming.name(self.component, False, description=description, extension="ref"),
                                     m)
        self._refs.append(ref)
        return ref

    def add_jnt(self, parent, ref, name, uni_scale):
        parent = parent if parent else self.comp_parent_jnt
        if not parent:
            parent = "deform"
        rot_off = self.component["jnt_rot_off"] if "jnt_rot_off" in self.component else [0, 0, 0]
        self._jnts.append([parent, ref, name, uni_scale, rot_off])
        return name

    def get_ctl_color(self, ik_fk='ik'):
        color = None
        if not self.component.is_assembly:
            if self.component["override_color"]:
                if self.component["use_RGB_color"]:
                    if ik_fk == "ik":
                        color = self.component["RGB_ik"]
                    else:
                        color = self.component["RGB_fk"]
                else:
                    if ik_fk == "ik":
                        color = self.component["color_ik"]
                    else:
                        color = self.component["RGB_fk"]
            else:
                if self.component.assembly["use_RGB_color"]:
                    if self.component["comp_side"] == "L":
                        if ik_fk == "ik":
                            color = self.component.assembly["l_RGB_ik"]
                        else:
                            color = self.component.assembly["l_RGB_fk"]
                    elif self.component["comp_side"] == "R":
                        if ik_fk == "ik":
                            color = self.component.assembly["r_RGB_ik"]
                        else:
                            color = self.component.assembly["r_RGB_fk"]
                    elif self.component["comp_side"] == "C":
                        if ik_fk == "ik":
                            color = self.component.assembly["c_RGB_ik"]
                        else:
                            color = self.component.assembly["c_RGB_fk"]
                else:
                    if self.component["comp_side"] == "L":
                        if ik_fk == "ik":
                            color = self.component.assembly["l_color_ik"]
                        else:
                            color = self.component.assembly["l_color_fk"]
                    elif self.component["comp_side"] == "R":
                        if ik_fk == "ik":
                            color = self.component.assembly["r_color_ik"]
                        else:
                            color = self.component.assembly["r_color_fk"]
                    elif self.component["comp_side"] == "C":
                        if ik_fk == "ik":
                            color = self.component.assembly["c_color_ik"]
                        else:
                            color = self.component.assembly["c_color_fk"]
        else:
            if self.component.assembly["use_RGB_color"]:
                if self.component["comp_side"] == "L":
                    if ik_fk == "ik":
                        color = self.component.assembly["l_RGB_ik"]
                    else:
                        color = self.component.assembly["l_RGB_fk"]
                elif self.component["comp_side"] == "R":
                    if ik_fk == "ik":
                        color = self.component.assembly["r_RGB_ik"]
                    else:
                        color = self.component.assembly["r_RGB_fk"]
                elif self.component["comp_side"] == "C":
                    if ik_fk == "ik":
                        color = self.component.assembly["c_RGB_ik"]
                    else:
                        color = self.component.assembly["c_RGB_fk"]
            else:
                if self.component["comp_side"] == "L":
                    if ik_fk == "ik":
                        color = self.component.assembly["l_color_ik"]
                    else:
                        color = self.component.assembly["l_color_fk"]
                elif self.component["comp_side"] == "R":
                    if ik_fk == "ik":
                        color = self.component.assembly["r_color_ik"]
                    else:
                        color = self.component.assembly["r_color_fk"]
                elif self.component["comp_side"] == "C":
                    if ik_fk == "ik":
                        color = self.component.assembly["c_color_ik"]
                    else:
                        color = self.component.assembly["c_color_fk"]
        return color


class BuildSystem:

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def context(self):
        return self._context

    @property
    def order(self):
        # TODO: buildsystem custom step
        self._context = Context()
        msgs = list()
        procedure = list()
        # if self.blueprint["precess"] == 2:
        #     return
        objects_msg = list()
        attributes_msg = list()
        operators_msg = list()
        connectors_msg = list()
        objects = list()
        attributes = list()
        operators = list()
        connectors = list()
        result = list()
        traversal(self.blueprint,
                  lambda x: self.__load(x),
                  lambda x: x["children"],
                  result)
        for comp, obj, attr, operator, connector in result:
            objects_msg.append(f"objects {comp['comp_name']} {comp['comp_side']} {comp['comp_index']}")
            attributes_msg.append(f"attributes {comp['comp_name']} {comp['comp_side']} {comp['comp_index']}")
            operators_msg.append(f"operators {comp['comp_name']} {comp['comp_side']} {comp['comp_index']}")
            connectors_msg.append(f"connector {comp['comp_name']} {comp['comp_side']} {comp['comp_index']}")
            objects.append(obj)
            attributes.append(attr)
            operators.append(operator)
            connectors.append(connector)
        msgs += objects_msg
        procedure += objects
        # if self.blueprint["precess"] == 2:
        #     return
        msgs += attributes_msg
        procedure += attributes
        # if self.blueprint["precess"] == 2:
        #     return
        msgs += operators_msg
        procedure += operators
        # if self.blueprint["precess"] == 2:
        #     return
        msgs += connectors_msg
        procedure += connectors
        # if self.blueprint["precess"] == 2:
        #     return

        msgs.append("network tree")
        procedure.append(self.network_tree)
        msgs.append("ctl structure")
        procedure.append(self.ctl_structure)
        msgs.append("jnt structure")
        procedure.append(self.jnt_structure)
        msgs.append("script node")
        procedure.append(self.script_node)
        return list(zip(msgs, procedure))

    def __init__(self, blueprint):
        self._blueprint = blueprint
        self._context = None

    def __load(self, component):
        mod = import_component_module(component["comp_type"], False)
        comp = mod.Rig(self.context, component)
        return component, comp.objects, comp.attributes, comp.operators, comp.connector

    def build(self):
        logger.info("mbox build system")
        order = self.order
        total = len(order)
        count = 0
        logger.info(f"total process... ")
        # logger.info(f"inspect jnt... ")
        # if self.blueprint.naming.inspect_jnt_names():
        #     return
        for msg, process in order:
            logger.info(f"{msg}... [{count} / {total}]")
            process()
            count += 1

        logger.info("build success")

    def network_tree(self):
        traversal(self.blueprint,
                  lambda x: [pm.connectAttr(x.network.attr("affects")[0],
                                            child.network.attr("affectedBy")[0], force=True)
                             for child in x["children"]],
                  lambda x: x["children"],
                  list())

    def ctl_structure(self):
        character_set = self.context.assembly.root.attr("character_sets").inputs()[0]
        ctls_set = [x for x in character_set.members() if "control" in x.name()][0]
        for instance in self.context:
            for ctl in instance.ctls:
                for shp in ctl.getShapes():
                    connect_info = pm.listConnections(shp, connections=True, plugs=True)
                    for source, destination in connect_info:
                        pass
                        # print(source, destination)
                        # pm.connectAttr(destination.replace(shape.name(), new_shape.name()), source)
                    shp.attr("isHistoricallyInteresting").set(0)
            pm.sets(ctls_set, addElement=instance.ctls)

        # add dag pose
        # default T, model, Sim

    def jnt_structure(self):
        connect_jnt = self.blueprint["connect_jnt"]
        root = self.context.assembly.root
        character_set = root.attr("character_sets").inputs()[0]
        jnts_set = [x for x in character_set.members() if "deform" in x.name()][0]
        for instance in self.context:
            comp = instance.component
            for index, jnt in enumerate(instance.jnts):
                parent, ref, name, uni_scale, rot_off = jnt
                j = add_jnt(parent, ref, name, uni_scale, rot_off=rot_off, connect_jnt=connect_jnt, dag_tree=root)
                side = "C" if comp["comp_side"] == "C" else "S"
                label = f"{comp['comp_name']}_{side}{comp['comp_index']}_{index}"
                side_set = ["C", "L", "R"]
                j.attr("side").set(side_set.index(comp["comp_side"]))
                j.attr("type").set("Other")
                j.attr("otherType").set(label)
                j.attr("radius").set(0.5)
                pm.connectAttr(j.attr("message"), comp.network.attr("jnts")[index], force=True)
                pm.sets(jnts_set, addElement=j)

    def script_node(self):
        # TODO: buildsystem script node
        trash_node = list()
        self.blueprint.network.attr("script_node").outputs()
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

def destroy_cb(*args): # all callback clear
    global mbox_destroy_new_id
    global mbox_destroy_open_id
    global mbox_destroy_remove_ref_id
    global mbox_destroy_unload_ref_id
    global mbox_character_cb_registry
    global mbox_character_namespace_registry
    logger.info("destroy_cb")

    try:
        for array in mbox_character_cb_registry:
            om2.MNodeMessage.removeCallback(array[1])
        om2.MSceneMessage.removeCallback(mbox_destroy_new_id)
        om2.MSceneMessage.removeCallback(mbox_destroy_open_id)
        om2.MSceneMessage.removeCallback(mbox_destroy_remove_ref_id)
        om2.MSceneMessage.removeCallback(mbox_destroy_unload_ref_id)
        del mbox_character_cb_registry
        del mbox_character_namespace_registry
        del mbox_destroy_new_id
        del mbox_destroy_open_id
        del mbox_destroy_remove_ref_id
        del mbox_destroy_unload_ref_id
    except:
        logger.error("destroy_cb")
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
    global mbox_destroy_id
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
    om2.MSceneMessage.removeCallback(mbox_destroy_new_id)
except:
    pass
finally:
    mbox_destroy_new_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterNew, destroy_cb)
try:
    om2.MSceneMessage.removeCallback(mbox_destroy_open_id)
except:
    pass
finally:
    mbox_destroy_open_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterOpen, destroy_cb)
try:
    om2.MSceneMessage.removeCallback(mbox_destroy_remove_ref_id)
except:
    pass
finally:
    mbox_destroy_remove_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterRemoveReference, refresh_registry)
try:
    om2.MSceneMessage.removeCallback(mbox_destroy_unload_ref_id)
except:
    pass
finally:
    mbox_destroy_unload_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterUnloadReference, refresh_registry)"""
        pm.scriptNode(root_script_node, edit=True, beforeScript=before_script_code)
        pm.scriptNode(root_script_node, executeBefore=True)
