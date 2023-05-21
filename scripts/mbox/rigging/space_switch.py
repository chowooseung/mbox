# -*- coding: utf-8 -*-

# maya
import pymel.core as pm
import maya.api.OpenMaya as om2

# built-in
import traceback
import logging

logger = logging.getLogger()


def destroy_cb(*args):  # all callback clear
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


def refresh_registry(*argc):  # refresh registry at reference unload, remove
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
    mbox_destroy_remove_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterRemoveReference,
                                                               refresh_registry)
try:
    om2.MSceneMessage.removeCallback(mbox_destroy_unload_ref_id)
except:
    pass
finally:
    mbox_destroy_unload_ref_id = om2.MSceneMessage.addCallback(om2.MSceneMessage.kAfterUnloadReference,
                                                               refresh_registry)
