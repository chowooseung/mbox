# -*- coding: utf-8 -*-

# build-in
import importlib

# maya
from pymel import core as pm

# mbox
from mbox import logger
from .utils import traversal, import_component_module

# mgear
from mgear.core import attribute, transform


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
        instance = list(filter(lambda ins: ins.oid == oid, self))
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
        return self._jnts

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

    def add_root(self):
        # TODO: instance add root
        pass

    def add_loc(self):
        # TODO: instance add loc
        pass

    def add_ctl(self):
        # TODO: instance add ctl
        pass

    def add_ref(self):
        # TODO: instance add ref
        pass

    def add_jnt(self):
        # TODO: instance add jnt
        pass

    def get_ctl_color(self, ikfk='ik'):
        # TODO: instance get ctl color
        pass

    def get_name(self, description="", extension=""):
        # TODO: instance get name
        pass


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
        result = list()
        traversal(self.blueprint,
                  lambda x: self.__load(x),
                  lambda x: x["children"],
                  result)
        objects_msg = list()
        features_msg = list()
        connectors_msg = list()
        objects = list()
        features = list()
        connectors = list()
        for comp, obj, feature, connector in result:
            objects_msg.append(f"{comp['comp_name']} {comp['comp_side']} {comp['comp_index']} objects")
            features_msg.append(f"{comp['comp_name']} {comp['comp_side']} {comp['comp_index']} feature")
            connectors_msg.append(f"{comp['comp_name']} {comp['comp_side']} {comp['comp_index']} connector")
            objects.append(obj)
            features.append(feature)
            connectors.append(connector)
        msgs += objects_msg
        msgs += features_msg
        msgs += connectors_msg
        procedure += objects
        procedure += features
        procedure += connectors

        msgs.append("network tree")
        procedure.append(self.network_tree)
        msgs.append("ctl tree")
        procedure.append(self.ctl_tree)
        msgs.append("ctl shapes")
        procedure.append(self.ctl_shapes)
        msgs.append("clean jnt")
        procedure.append(self.clean_jnt)
        msgs.append("sets")
        procedure.append(self.sets)
        msgs.append("script node")
        procedure.append(self.script_node)
        return list(zip(msgs, procedure))

    def __init__(self, blueprint):
        self._blueprint = blueprint
        self._context = None

    def __load(self, component):
        mod = import_component_module(component["comp_type"], False)
        comp = mod.Instance(self.context, component)
        return component, comp.objects, comp.features, comp.connector

    def build(self):
        logger.info("mbox build system")
        order = self.order
        total = len(order)
        count = 0
        logger.info(f"total process... [{count} / {total}]")

        for msg, process in order:
            logger.info(f"{msg}... [{count} / {total}]")
            process()
            count += 1

        logger.info("build success")

    def network_tree(self):
        # TODO: buildsystem network tree connect
        pass

    def ctl_tree(self):
        # TODO: buildsystem connect ctl tree and connect ui host
        pass

    def ctl_shapes(self):
        # TODO: buildsystem ctl replace and reconnection and configure
        connect_info = pm.listConnections(shape, connections=True, plugs=True)
        for source, destination in connect_info:
            pm.connectAttr(source, destination.replace(shape.name(), new_shape.name()))

    def clean_jnt(self):
        for instance in self.context:
            comp = instance.component
            for index, jnt in enumerate(instance.jnts):
                side = "C" if comp["comp_side"] == "C" else "S"
                label = f"{comp['comp_name']}_{side}{comp['comp_index']}_{index}"
                side_set = ["C", "L", "R"]
                jnt.attr("side").set(side_set.index(comp["comp_side"]))
                jnt.attr("type").set("Other")
                jnt.attr("otherType").set(label)
                jnt.attr("radius").set(0.5)
                jnt.attr("segmentScaleCompensate").set(False)
                pm.connectAttr(self.context.assembly.root.attr("joints_label_vis"), jnt.attr("drawLabel"))

    def sets(self):
        # TODO: buildsystem create maya sets
        pass

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
