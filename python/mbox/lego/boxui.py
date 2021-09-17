# -*- coding:utf-8 -*-

#
import os
import sys
import traceback
from functools import partial
import importlib

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# mbox
from mbox.core import pyqt
from mbox.vendor.Qt import QtCore, QtWidgets, QtGui
from mbox.lego import boxdesign, lib

PY2 = sys.version_info[0] == 2


class BoxDesignUI(QtWidgets.QDialog, boxdesign.Ui_Form):

    def __init__(self, parent=None):

        super(BoxDesignUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.component_listView.setAcceptDrops(False)
        self.component_listView.setDragEnabled(True)
        self.component_listView.setDropIndicatorShown(False)
        self.installEventFilter(self)

    def keyPressEvent(self, event):

        if not event.key() == QtCore.Qt.Key_Escape:
            super(BoxDesignUI, self).keyPressEvent(event)


class BoxUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):

        self.toolName = "legoBlockComponentManager"
        super(BoxUI, self).__init__(parent=parent)

        self.box_ui = BoxDesignUI()
        self.box_ui.component_listView.setAction(self.drag_draw_component)
        self.box_ui.component_listView.installEventFilter(self)

        self.start_dir = pm.workspace(query=True, rootDirectory=True)

        self.__proxyModel = QtCore.QSortFilterProxyModel(self)
        self.box_ui.component_listView.setModel(self.__proxyModel)

        self.create_window()
        self.create_layout()
        self.create_connections()
        self._refreshList()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def eventFilter(self, watched, event):

        if (event.type() == QtCore.QEvent.KeyPress
                and event.matches(
                    QtGui.QKeySequence.InsertParagraphSeparator)):
            self.draw_component()

        return False

    def create_window(self):

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Lego Block Component Manager")
        self.resize(280, 600)

    def create_layout(self):

        self.gmc_layout = QtWidgets.QVBoxLayout()
        self.gmc_layout.addWidget(self.box_ui)
        self.gmc_layout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.gmc_layout)

    def get_component_list(self):

        comp_list = list()
        compDir = lib.get_blocks_directory()
        trackLoadComponent = list()
        for path, comps in compDir.items():
            pm.progressWindow(title='Loading Components',
                              progress=0,
                              max=len(comps))
            for comp_name in comps:
                pm.progressWindow(edit=True,
                                  step=1,
                                  status='\nLoading: %s' % comp_name)
                if comp_name in trackLoadComponent:
                    pm.displayWarning(
                        "Custom component name: %s, already in default "
                        "components. Names should be unique. This component is"
                        " not loaded" % comp_name)
                    continue
                else:
                    trackLoadComponent.append(comp_name)

                if not os.path.exists(os.path.join(path,
                                                   comp_name, "__init__.py")):
                    continue
                try:
                    module = lib.load_blocks_blueprint(comp_name)
                    if PY2:
                        reload(module)
                    else:
                        importlib.reload(module)
                    comp_list.append(module.TYPE)
                except Exception as e:
                    pm.displayWarning(
                        "{} can't be load. Error at import".format(comp_name))
                    pm.displayError(e)
                    pm.displayError(traceback.format_exc())

        pm.progressWindow(edit=True, endProgress=True)
        return comp_list

    def setSourceModel(self, model):
        """Set the source model for the listview

        Args:
            model (Qt model): QtCore.QSortFilterProxyModel
        """

        self.__proxyModel.setSourceModel(model)

    def _refreshList(self):
        """Refresh listview content
        """

        model = QtGui.QStandardItemModel(self)
        for c_node in self.get_component_list():
            model.appendRow(QtGui.QStandardItem(c_node))
        self.setSourceModel(model)

    ###########################
    # "right click context menu"
    ###########################

    def _component_menu(self, QPos):
        """Create the component list rightclick menu

        Args:
            QPos (QPos): Position

        Returns:
            None: None
        """
        comp_widget = self.box_ui.component_listView
        currentSelection = comp_widget.selectedIndexes()
        if currentSelection is None:
            return
        self.comp_menu = QtWidgets.QMenu()
        parentPosition = comp_widget.mapToGlobal(QtCore.QPoint(0, 0))
        menu_item_01 = self.comp_menu.addAction("Draw Component")
        self.comp_menu.addSeparator()
        menu_item_02 = self.comp_menu.addAction("Refresh List")

        menu_item_01.triggered.connect(self.draw_component)
        menu_item_02.triggered.connect(self._refreshList)

        self.comp_menu.move(parentPosition + QPos)
        self.comp_menu.show()

    def _search_menu(self, QPos):
        search_widget = self.box_ui.search_lineEdit

        self.search_menu = QtWidgets.QMenu()
        parentPosition = search_widget.mapToGlobal(QtCore.QPoint(0, 0))
        menu_item_01 = self.search_menu.addAction("Clear")
        menu_item_01.triggered.connect(search_widget.clear)
        self.search_menu.move(parentPosition + QPos)
        self.search_menu.show()

    ###########################
    # create connections SIGNALS
    ###########################
    def create_connections(self):

        # buttons
        self.box_ui.settings_pushButton.clicked.connect(lib.inspect_settings)
        # self.box_ui.build_pushButton.clicked.connect(lib.build, None, )
        self.box_ui.duplicate_pushButton.clicked.connect(partial(lib.duplicate_blueprint_component, False, True))
        self.box_ui.dupSym_pushButton.clicked.connect(partial(lib.duplicate_blueprint_component, True, True))
        # self.box_ui.extrCtl_pushButton.clicked.connect(guide_manager.extract_controls)
        self.box_ui.draw_pushButton.clicked.connect(self.draw_comp_doubleClick)

        # list view
        self.box_ui.search_lineEdit.textChanged.connect(
            self.filter_changed)

        self.box_ui.component_listView.clicked.connect(self.update_info)
        self.selModel = self.box_ui.component_listView.selectionModel()
        self.selModel.selectionChanged.connect(self.update_info)
        self.box_ui.component_listView.doubleClicked.connect(
            self.draw_comp_doubleClick)

        # connect menu
        self.box_ui.component_listView.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.box_ui.component_listView.customContextMenuRequested.connect(
            self._component_menu)

        self.box_ui.search_lineEdit.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.box_ui.search_lineEdit.customContextMenuRequested.connect(
            self._search_menu)

    #############
    # SLOTS
    #############

    def update_info(self):
        try:
            item = self.box_ui.component_listView.selectedIndexes()[0]
            comp_name = item.data()
            module = lib.load_blocks_blueprint(comp_name)
            if PY2:
                reload(module)
            else:
                importlib.reload(module)
            info_text = (
                "{}\n".format(module.DESCRIPTION)
                + "\n-------------------------------\n\n"
                + "Author: {}\n".format(module.AUTHOR)
                + "Url: {}\n".format(module.URL)
                + "Version: {}\n".format(str(module.VERSION))
                + "Type: {}\n".format(module.TYPE)
                + "Name: {}\n".format(module.NAME)
            )
        except IndexError:
            info_text = ""

        self.box_ui.info_plainTextEdit.setPlainText(info_text)

    def draw_comp_doubleClick(self, *args):
        self.draw_component()

    def drag_draw_component(self, pGuide):
        if pGuide:
            if pGuide and isinstance(pGuide, list):
                pGuide = pGuide[0]
            parent = pm.PyNode(pGuide)
            self.draw_component(parent)
        else:
            pm.displayWarning("Nothing catch under cursor. Not Component Draw")

    def draw_component(self, parent=None):
        showUI = self.box_ui.showUI_checkBox.checkState()
        for x in self.box_ui.component_listView.selectedIndexes():
            lib.draw_blueprint(None, x.data(), parent, showUI)

    def filter_changed(self, ft):
        """Filter out the elements in the list view

        """
        regExp = QtCore.QRegExp(ft,
                                QtCore.Qt.CaseSensitive,
                                QtCore.QRegExp.Wildcard
                                )
        self.__proxyModel.setFilterRegExp(regExp)
        self.box_ui.info_plainTextEdit.setPlainText("")


def show_box_ui(*args):
    pyqt.show_dialog(BoxUI, dockable=True)


if __name__ == "__main__":
    show_box_ui()
