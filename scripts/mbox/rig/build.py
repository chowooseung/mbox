# -*- coding: utf-8 -*-

# build-in
import logging

# maya
from pymel import core as pm


class Context(list):

    def instance(self, oid):
        instance = list(filter(lambda ins: ins.oid == oid, self))
        return instance[0] if instance else None


class Instance:

    @property
    def component(self):
        return self._component

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

    def __init__(self, component):
        self._root = None
        self._ctls = list()
        self._refs = list()
        self._jnts = list()
        self._component = component

    def add_root(self):
        pass

    def add_ctl(self):
        pass

    def add_ref(self):
        pass

    def add_jnt(self):
        pass

    def add_attribute(self):
        pass

    def get_ctl_color(self):
        pass

    def get_name(self):
        pass


class BuildSystem:

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def context(self):
        return self._context

    @property
    def pre_custom_step(self):
        return self._pre_custom_step

    @property
    def objects(self):
        return self._objects

    @property
    def features(self):
        return self._features

    @property
    def connector(self):
        return self._connector

    @property
    def post_custom_step(self):
        return self._post_custom_step

    @property
    def order(self):
        # pre custom step
        # objects
        # features
        # connector
        # ctl_structure
        # ctl_shapes
        # jnt_structure
        # sets
        # post custom step
        return []

    def __init__(self, blueprint):
        self._blueprint = blueprint
        self._context = Context()
        self._pre_custom_step = list()
        self._objects = list()
        self._features = list()
        self._connector = list()
        self._post_custom_step = list()

    def __load(self):
        pass

    def build(self):
        pass

    def ctl_structure(self):
        pass

    def ctl_shapes(self):
        pass

    def jnt_structure(self):
        pass

    def sets(self):
        pass
