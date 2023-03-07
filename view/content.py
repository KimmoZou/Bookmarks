import copy

from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import (
    QWidget, QTreeWidget, QHBoxLayout, QLabel,
    QSpinBox, QVBoxLayout, QSpacerItem, QSizePolicy, QTreeWidgetItem, QPushButton,
    QMessageBox
)

from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from view.widgets import items
from resources import resources_rc


class Contents(QWidget):
    def __init__(self):
        super().__init__()
        self.__catalogs = []
        # 当前选中的值
        self.selected_item = None
        self.selected_row = 0
        self.previous_value = 0
        self.__init_widget()
        self.__init_widgets()
        self.__add_widgets()

    def __init_widget(self):
        pass

    def __init_widgets(self):
        # 数据
        self.__model = QStandardItemModel(self)
        # 布局
        self.__horizon_layout = QHBoxLayout()
        self.__vertical_layout = QVBoxLayout()
        # 目录树
        self.__content_view = QTreeWidget()

        self.__content_view.setStyleSheet(
            "QTreeWidget{"
            "font:15px;"
            "}"
            "QTreeWidget:item:selected{"
            "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);"
            "}"
        )

        # 设置标题
        self.__content_view.setHeaderLabels(["章节名称", "页码"])
        self.__content_view.setColumnWidth(0, 350)
        # 页码偏移
        self.__label1 = QLabel("页偏移量：")
        self.__pages_shift = QSpinBox()
        self.__pages_shift.setMaximumSize(70, 30)
        self.__pages_shift.setSingleStep(1)
        self.__pages_shift.setMinimum(0)
        self.__pages_shift.setMaximum(9999)
        self.__pages_shift.setAlignment(Qt.AlignCenter)

        # 添加，添加子项目，删除 操作
        self.__label2 = QLabel("操作：")
        self.__add_btn = QPushButton(QIcon(r":\icon\icon-add"), "")
        self.__add_btn.setToolTip("在选中的行下插入")
        self.__insert_btn = QPushButton(QIcon(r":\icon\icon-insert"), "")
        self.__insert_btn.setToolTip("添加子目录")
        self.__delete_btn = QPushButton(QIcon(r":\icon\icon-delete"), "")
        self.__delete_btn.setToolTip("删除该目录（包括它的子目录）")
        self.__up_btn = QPushButton(QIcon(r":\icon\icon-up"), "")
        self.__up_btn.setToolTip("上移")
        self.__down_btn = QPushButton(QIcon(r":\icon\icon-down"), "")
        self.__down_btn.setToolTip("下移")
        # 初始无数据，不能使用
        self.__insert_btn.setEnabled(False)
        self.__delete_btn.setEnabled(False)
        self.__up_btn.setEnabled(False)
        self.__down_btn.setEnabled(False)

        # 空白
        self.__space1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # 消息框
        self.__msgbox = QMessageBox(self)
        self.__msgbox.setIconPixmap(QPixmap(r":\icon\icon-warn"))

        # 添加事件
        self.__content_view.itemClicked.connect(self.__item_clicked)
        self.__add_btn.clicked.connect(self.__item_add)
        self.__insert_btn.clicked.connect(self.__item_insert)
        self.__delete_btn.clicked.connect(self.__item_delete)
        self.__up_btn.clicked.connect(self.__item_up)
        self.__down_btn.clicked.connect(self.__item_down)


    def __add_widgets(self):
        self.__vertical_layout.addWidget(self.__content_view)
        self.__horizon_layout.addWidget(self.__label1)
        self.__horizon_layout.addWidget(self.__pages_shift)
        self.__horizon_layout.addWidget(self.__label2)
        self.__horizon_layout.addWidget(self.__add_btn)
        self.__horizon_layout.addWidget(self.__insert_btn)
        self.__horizon_layout.addWidget(self.__delete_btn)
        self.__horizon_layout.addWidget(self.__up_btn)
        self.__horizon_layout.addWidget(self.__down_btn)
        self.__horizon_layout.addItem(self.__space1)
        self.__vertical_layout.addLayout(self.__horizon_layout)
        self.setLayout(self.__vertical_layout)

    @QtCore.Slot()
    def __item_clicked(self, item, column):
        self.selected_item = item
        self.__update_btn()

    # 插入一行数据
    @QtCore.Slot()
    def __item_add(self, e):
        # 插入的节点
        item = None
        if e is False:
            item = items.Item()
            item.setText(0, "新章节")
            item.setText(1, "新页码")
        else:
            item = e

        # 如果没有数据，直接加入
        if self.selected_item is None:
            self.__content_view.addTopLevelItem(item)
            self.selected_item = item
            self.selected_item.setSelected(True)
            self.__update_btn()
            return

        # 获取选中行的父亲
        item_parent = self.selected_item.parent()
        self.__update_selected_row()
        # 顶级节点
        if item_parent is None:
            self.__content_view.insertTopLevelItem(self.selected_row + 1, item)
        else:
            item_parent.insertChild(self.selected_row + 1, item)
        # 更新当前的按钮
        self.selected_item.setSelected(False)
        self.selected_item = item
        self.selected_item.setSelected(True)
        self.__update_btn()

    # 添加一个儿子
    @QtCore.Slot()
    def __item_insert(self):
        # 插入的节点
        item = items.Item()
        item.setText(0, "新章节")
        item.setText(1, "新页码")
        self.selected_item.addChild(item)
        self.__content_view.expandItem(self.selected_item)
        self.selected_item.setSelected(False)
        self.selected_item = item
        self.selected_item.setSelected(True)
        self.__update_btn()

    # 删除一个节点
    @QtCore.Slot()
    def __item_delete(self):
        item_parent = self.selected_item.parent()
        self.__update_selected_row()
        # 顶级节点
        if item_parent is None:
            # 删除
            self.__content_view.takeTopLevelItem(self.selected_row)
            # 设置删除后的节点
            self.selected_item = self.__content_view.topLevelItem(self.selected_row)
            if self.selected_item is None:
                self.selected_item = self.__content_view.topLevelItem(self.selected_row - 1)
        else:
            # 删除儿子
            item_parent.takeChild(self.selected_row)
            self.selected_item = item_parent.child(self.selected_row)
            if self.selected_item is None:
                self.selected_item = item_parent

        self.__update_btn()
        if self.selected_item is not None:
            self.selected_item.setSelected(True)

    # 向上移动
    @QtCore.Slot()
    def __item_up(self):
        # 按钮不能用
        if not self.__up_btn.isEnabled():
            return

        item_parent = self.selected_item.parent()
        self.__update_selected_row()
        # 如果是 顶级标签
        if item_parent is None:
            # 先获得这个 item
            tmp = self.__content_view.topLevelItem(self.selected_row - 1)
            item = items.Item()
            item.set_value(tmp.text(0), tmp.text(1))
            # 删除
            self.__content_view.takeTopLevelItem(self.selected_row - 1)
            self.__content_view.insertTopLevelItem(self.selected_row, item)

        else:
            tmp = item_parent.child(self.selected_row - 1)
            item = items.Item()
            item.set_value(tmp.text(0), tmp.text(1))
            # 删除
            item_parent.takeChild(self.selected_row - 1)
            item_parent.insertChild(self.selected_row, item)

        self.selected_row = self.selected_row - 1
        self.__update_selected_row()
        self.__update_btn()

    # 向下移动
    @QtCore.Slot()
    def __item_down(self):
        # 按钮不能用
        if not self.__down_btn.isEnabled():
            return
        item_parent = self.selected_item.parent()
        self.__update_selected_row()
        # 如果是 顶级标签
        if item_parent is None:
            # 先获得这个 item
            tmp = self.__content_view.topLevelItem(self.selected_row + 1)
            item = items.Item()
            item.set_value(tmp.text(0), tmp.text(1))
            # 删除
            self.__content_view.takeTopLevelItem(self.selected_row + 1)
            self.__content_view.insertTopLevelItem(self.selected_row, item)

        else:
            tmp = item_parent.child(self.selected_row + 1)
            item = items.Item()
            item.set_value(tmp.text(0), tmp.text(1))
            # 删除
            item_parent.takeChild(self.selected_row + 1)
            item_parent.insertChild(self.selected_row, item)

        self.selected_row = self.selected_row + 1
        self.__update_selected_row()
        self.__update_btn()

    # 获得当前所处的行
    def __update_selected_row(self):
        item_parent = self.selected_item.parent()
        if item_parent is None:
            self.selected_row = self.__content_view.indexOfTopLevelItem(
                self.selected_item)
        else:
            self.selected_row = item_parent.indexOfChild(self.selected_item)

    # 更新按钮
    def __update_btn(self):
        if self.selected_item is None:
            # 没有选中
            self.__insert_btn.setEnabled(False)
            self.__delete_btn.setEnabled(False)
            self.__up_btn.setEnabled(False)
            self.__down_btn.setEnabled(False)
            return

        self.__insert_btn.setEnabled(True)
        self.__delete_btn.setEnabled(True)

        # 获取选中行的父亲
        item_parent = self.selected_item.parent()

        self.__update_selected_row()

        # 第一行
        if self.selected_row == 0:
            self.__up_btn.setEnabled(False)
        else:
            self.__up_btn.setEnabled(True)

        # 最后一行 如果是父节点
        if item_parent is None:
            if self.__content_view.topLevelItem(self.selected_row + 1) is None:
                self.__down_btn.setEnabled(False)
            else:
                self.__down_btn.setEnabled(True)
        # 最后一行是 儿子节点
        else:
            if item_parent.child(self.selected_row + 1) is None:
                self.__down_btn.setEnabled(False)
            else:
                self.__down_btn.setEnabled(True)

    def get_catalogs(self):
        return self.__catalogs

    def set_catalogs(self, catalogs):
        self.__catalogs = catalogs


from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('fusion')
    window = Contents()
    window.show()
    app.exec()
