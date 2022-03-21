# -*- coding: utf-8 -*-

# built-in
import uuid

# maya
from pymel import core as pm

# mbox
from .build import BuildSystem


class Component(dict):

    def __init__(self):
        super(Component, self).__init__()

    def __load(self):
        self["oid"] = str(uuid.uuid4())
        return False

    def __setitem__(self, key, value):
        pass

    def update(self, __m: Mapping[_KT, _VT], **kwargs: _VT) -> None:
        pass


class Guide(Component):

    @property
    def negate(self):
        return -1

    def pull(self):
        pass

    def push(self):
        pass

    def draw(self):
        pass

    def duplicate(self):
        pass

    def get_jnt_structure(self):
        pass

    def blade(self):
        pass


class Blueprint:

    @property
    def blueprint(self):
        return self

    def import_blueprint(self):
        pass

    def export_blueprint(self):
        pass

    def blueprint_from_guide(self):
        pass

    def blueprint_from_rig(self):
        pass

    def find_component(self):
        pass

    def duplicate_component(self):
        pass

    def mirror_component(self):
        pass

    def set_index(self):
        pass

    def combine_blueprint(self):
        pass

    def draw_guide(self):
        pass

    def draw_rig(self):
        build_system = BuildSystem(self.blueprint)
        build_system.build()
