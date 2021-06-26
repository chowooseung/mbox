# -*- coding:utf-8 -*-

__version_info__ = (0, 0, 1)
__version__ = "{}.{}.{}".format(*__version_info__)

major, minor, micro = __version_info__

version = __version__
version_info = ("{}(major={}, minor={}, micro={})".format(__package__, major, minor, micro))
