# -*- coding:utf-8 -*-

__mbox = (0, 0, 1)
mbox = "{}.{}.{}".format(*__mbox)

__schema = 1
schema = "blueprint-{}".format(__schema)


def mbox_mmm():
    return __mbox


def schema_n():
    return __schema
