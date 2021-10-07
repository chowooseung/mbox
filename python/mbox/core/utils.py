# -*- coding:utf-8 -*-
"""from mgear.core.utils"""

#
import logging
import os
import sys
import timeit
from functools import wraps

# maya
from maya import cmds
import pymel.core as pm
from maya import mel

logger = logging.getLogger(__name__)


def gather_custom_module_directories(envvarkey, defaultModulePath, component=False):
    """returns component directory

    Arguments:
        envvarkey: The environment variable key name, that is searched
        defaultModulePath: The default module path for search in.

    Returns:
        Dict{string: []string}

    """
    results = dict()

    # from default path
    if not isinstance(defaultModulePath, list):
        defaultModulePath = [defaultModulePath]
    for dp in defaultModulePath:
        if not os.path.exists(dp):
            message = "= MBOX RIG SYSTEM ====== notify:"
            message += "\n  default module directory is not " \
                       "found at {}".format(dp)
            message += "\n\n check your mGear installation"
            message += " or call your system administrator."
            message += "\n"
            logger.error(message)
            return dict()

        results[dp] = [x for x in sorted(os.listdir(dp)) if os.path.isdir(os.path.join(dp, x))]

    # from environment variables
    envvarval = os.environ.get(envvarkey, "")
    for path in envvarval.split(os.pathsep):

        if not path or not os.path.exists(path):
            continue
        if component:
            init_py_path = os.path.join(path, "__init__.py")
            if not os.path.exists(init_py_path):
                message = "= MBOX RIG SYSTEM ====== notify:"
                message += "\n  __init__.py for custom component not " \
                           "found {}".format(init_py_path)
                message += "\n\n check your module definition file or " \
                           "environment variable 'MBOX_BLOCKS_PATH'"
                message += " or call your system administrator."
                message += "\n"
                logger.error(message)
                continue

        modules = [x for x in sorted(os.listdir(path)) if os.path.isdir(os.path.join(path, x))]

        results[path] = modules

    return results


def getModuleBasePath(directories, moduleName):
    """search component path"""

    for basepath, modules in directories.iteritems():
        if moduleName in modules:
            # moduleBasePath = os.path.basename(basepath)
            moduleBasePath = basepath
            break
    else:
        moduleBasePath = ""
        message = "= MBOX RIG SYSTEM ======"
        message += "component base directory not found " \
                   " for {}".format(moduleName)
        logger.error(message)

    return moduleBasePath


def import_from_standard_or_custom_directories(directories, defaultFormatter, customFormatter, moduleName):
    """Return imported module

    Arguments:
        directories: the directories for search in. this is got by
            gatherCustomModuleDirectories
        defaultFormatter: this represents module structure for default
            module. for example "mgear.core.shifter.component.{}"
        customFormatter:  this represents module structure for custom
            module. for example "{0}.{1}"

    Returns:
        module: imported module

    """
    # Import module and get class
    try:
        module_name = defaultFormatter.format(moduleName)
        module = __import__(module_name, globals(), locals(), ["*"], -1)

    except ImportError:
        moduleBasePath = getModuleBasePath(directories, moduleName)
        module_name = customFormatter.format(moduleName)
        if pm.dirmap(cd=moduleBasePath) not in sys.path:
            sys.path.append(pm.dirmap(cd=moduleBasePath))
        module = __import__(module_name, globals(), locals(), ["*"], -1)

    return module


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------
def viewport_off(func):
    """Decorator - Turn off Maya display while func is running.

    if func will fail, the error will be raised after.

    type: (function) -> function

    """

    @wraps(func)
    def wrap(*args, **kwargs):
        # type: (*str, **str) -> None

        # Turn $gMainPane Off:
        gMainPane = mel.eval('global string $gMainPane; $temp = $gMainPane;')
        cmds.paneLayout(gMainPane, edit=True, manage=False)

        try:
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            cmds.paneLayout(gMainPane, edit=True, manage=True)

    return wrap


def one_undo(func):
    """Decorator - guarantee close chunk.

    type: (function) -> function

    """

    @wraps(func)
    def wrap(*args, **kwargs):
        # type: (*str, **str) -> None

        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            cmds.undoInfo(closeChunk=True)

    return wrap


def timeFunc(func):
    """Use as a property to time any desired function
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        start = timeit.default_timer()
        try:
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            end = timeit.default_timer()
            timeConsumed = end - start
            print("{} time elapsed running {}".format(timeConsumed, func.func_name))

    return wrap


# -----------------------------------------------------------------------------
# selection Decorators
# -----------------------------------------------------------------------------


def _filter_selection(selection, sel_type="nurbsCurve"):
    filtered_sel = []
    for node in selection:
        if node.getShape().type() == sel_type:
            filtered_sel.append(node)
    return filtered_sel


def filter_nurbs_curve_selection(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        args = list(args)
        args[0] = _filter_selection(args[0])
        return func(*args, **kwargs)

    return wrap
