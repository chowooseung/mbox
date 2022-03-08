# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.lego.lib import (
    AbstractObjects,
    AbstractAttributes,
    AbstractOperators,
    AbstractConnection
)

# mgear
from mgear.core import (
    attribute,
    transform,
    vector
)


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        # matrix
        if self.block["neutral_rotation"]:
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.block["transforms"][1]).translate)
        else:
            if self.block["mirror_behaviour"] and self.block.negate:
                scl = [1, 1, -1]
            else:
                scl = [1, 1, 1]
            m = transform.setMatrixScale(pm.datatypes.Matrix(self.block["transforms"][1]), scl)

        # get ctl color
        ik_color = self.get_ctl_color("ik")

        # create
        if not self.block["leaf_joint"]:
            root = self.create_root(context=context, m=m)
            distance = vector.getDistance(pm.datatypes.Matrix(self.block["transforms"][0]).translate,
                                          pm.datatypes.Matrix(self.block["transforms"][1]).translate)
            ctl = self.create_ctl(context=context,
                                  parent=root,
                                  m=m,
                                  parent_ctl=None,
                                  color=ik_color,
                                  ctl_attr=self.block["key_able_attrs"],
                                  shape=self.block["icon"],
                                  size=self.block["ctl_size"] * distance,
                                  cns=True if self.block["ik_ref_array"] else False)
            ref = self.create_ref(context=context,
                                  parent=ctl,
                                  description="",
                                  m=m)
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.create_jnt(context=context,
                                      parent=None,
                                      description="",
                                      ref=ref)
            if self.block["ik_ref_array"]:
                self.ins["script_node"] = pm.createNode("script", name="block_sc")
        else:
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.create_jnt(context=context,
                                      parent=None,
                                      description="",
                                      ref=m)


class Attributes(AbstractAttributes):

    def __init__(self, block):
        super(Attributes, self).__init__(block=block)

    def process(self, context):
        super(Attributes, self).process(context=context)

        if self.block["leaf_joint"]:
            return
        if not self.block["ik_ref_array"]:
            return
        array = [x for x in self.block["ik_ref_array"].split(",")]
        ik_ref_ctls = list()
        for ctl_index, oid in [x.split(" | ") for x in array]:
            block = self.block.top.find_block_with_oid(oid)
            target_instance = context.instance(block.ins_name)
            ik_ref_ctls.append(target_instance["ctls"][int(ctl_index)])
        enum = [x.nodeName() for x in ik_ref_ctls]
        ik_ref_attr = self.create_enum_attr(context, "ik_ref", value="self", enum=["self"]+enum)
        ik_ref_match_attr = self.create_enum_attr(context, "ik_ref_match", value="self", enum=["self"]+enum, storable=False)
        ik_ref_match_attr.set(keyable=True, lock=False, channelBox=True)
        attribute.addAttribute(self.ins["script_node"], "script_node", "message")
        self.ins["script_node"].attr("sourceType").set(1)
        self.ins["script_node"].attr("scriptType").set(0)
        oid = self.block["oid"]
        script_code = f"""import pymel.core as pm
import maya.api.OpenMaya as om2
import uuid

global mbox_character_cb_registry

oid = '{oid}'

class SpaceSwitch:

    def __init__(self, node):
        self.node = pm.PyNode(node)
        namespace = self.node.namespace()
        split_name = [x for x in '{self.ins["ctls"][0].fullPath()}'.split("|") if x]
        self.ctl = "|".join([namespace + x for x in split_name if x])

    def switch(self):
        destination_value = self.node.attr('ik_ref_match').get()
        temp_obj = pm.group(name=str(uuid.uuid4()), empty=True)
        pm.matchTransform(temp_obj, self.ctl, position=True, rotation=True)
        self.node.attr('ik_ref').set(destination_value)
        pm.matchTransform(self.ctl, temp_obj, position=True, rotation=True)
        pm.delete(temp_obj)

    def space_switch(self):
        with pm.UndoChunk():
            selected = pm.selected()
            value = self.node.attr('ik_ref_match').get()
            if value not in {range(len(enum) + 1)}:
                return
            switch_value = self.node.attr('ik_ref').get()
            if value != switch_value:
                self.switch()
            pm.select(selected)

def cb_run(msg, plug1, plug2, client_data):
    if msg != 2056:
        return
    if plug1.partialName(includeNodeName=False) != 'ik_ref_match':
        return
    client_data.space_switch()

def register_cb(node):
    sel_list = om2.MGlobal.getSelectionListByName(node)
    node_dag = sel_list.getDagPath(0)
    node_obj = sel_list.getDependNode(0)
    node_full_name = node_dag.fullPathName()
    cb_id = om2.MNodeMessage.addAttributeChangedCallback(node_obj, cb_run, clientData=SpaceSwitch(node))
    return (node_dag, cb_id)

all_network = [x for x in pm.ls(type='network') if x.hasAttr('oid')]
networks = [x for x in all_network if x.attr('oid').get() == oid]
for network in networks:
    if network.namespace():
        namespace = network.namespace()[:-1]
    else:
        namespace = network.namespace()
    if namespace not in mbox_character_namespace_registry:
        break

target = network.attr('script_node').inputs(type='transform')
if target:
    target = target[0]
    try:
        mbox_character_cb_registry.append(register_cb(target.fullPath()))
    except:
        mbox_character_cb_registry = list()
        mbox_character_cb_registry.append(register_cb(target.fullPath()))"""
        pm.scriptNode(self.ins["script_node"], edit=True, beforeScript=script_code)


class Operators(AbstractOperators):

    def __init__(self, block):
        super(Operators, self).__init__(block=block)

    def process(self, context):
        super(Operators, self).process(context=context)


class Connection(AbstractConnection):

    def __init__(self, block):
        super(Connection, self).__init__(block=block)

    def process(self, context):
        super(Connection, self).process(context=context)

        if self.ins["script_node"]:
            pm.connectAttr(self.ins["ui_host"].attr("message"), self.block.network.attr("script_node"), force=True)
