# -*- coding: utf-8 -*-


def naming(convention, padding=1, name="", direction="", index="", description="", extension=""):

    index = str(index).zfill(padding)
    n = convention.format(name=name, direction=direction, index=index, description=description, extension=extension)
    result = "_".join([x for x in n.split("_") if x])
    return result
