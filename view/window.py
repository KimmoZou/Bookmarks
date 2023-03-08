import os

from PySide6.QtCore import Qt, QSize, Signal
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QStatusBar, QFileDialog, QMessageBox
)

from resources import resources_rc
from view import content
from view import helps


class Window(QMainWindow):
    OPEN = Signal(str)
    OUTPUT = Signal(str)
    INPUT = Signal(str)
    SAVE = Signal(str, int)

    def __init__(self):
        self.filePath = ''
        super().__init__()
        self.__init_window()
        self.__init_widgets()
        self.__add_widgets()

    def __init_window(self):
        self.setWindowTitle("Bookmarks")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(r":\icon\icon-app"))
        # 设置工具栏不可以取消
        self.setContextMenuPolicy(Qt.NoContextMenu)

    def __init_widgets(self):
        # 菜单
        self.__toolBar = QToolBar()
        self.__toolBar.setMovable(False)
        self.__toolBar.setIconSize(QSize(50, 50))
        self.__toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.__toolBar.setStyleSheet(
            "QToolButton {"
            "margin:2px 10px;"
            "}"
            "QToolBar{"
            "border-bottom:1px solid black"
            "}"
        )
        # 菜单项
        self.__toolBar_file = QAction(QIcon(r":\icon\icon-file"), "选择文件", self)
        self.__toolBar_output = QAction(QIcon(r":\icon\icon-output"), "导出文件目录", self)
        self.__toolBar_input = QAction(QIcon(r":\icon\icon-input"), "导入目录", self)
        self.__toolBar_save = QAction(QIcon(r":\icon\icon-save"), "保存文件", self)
        self.__toolBar_help = QAction(QIcon(r":\icon\icon-help"), "使用帮助", self)
        # 状态栏
        self.__statusBar = QStatusBar(self)
        # 内容
        self.contents = content.Contents()

        # 消息框
        self.__msgbox = QMessageBox(self)
        self.__msgbox.setIconPixmap(QPixmap(r":\icon\icon-warn"))

        self.helps = None

        # 绑定事件
        self.__toolBar_file.triggered.connect(self.__open_file)
        self.__toolBar_output.triggered.connect(self.__output_file)
        self.__toolBar_input.triggered.connect(self.__input_file)
        self.__toolBar_save.triggered.connect(self.__save_file)
        self.__toolBar_help.triggered.connect(self.__help)

    def __add_widgets(self):
        # 添加菜单项
        self.__toolBar.addAction(self.__toolBar_file)
        self.__toolBar.addAction(self.__toolBar_output)
        self.__toolBar.addAction(self.__toolBar_input)
        self.__toolBar.addAction(self.__toolBar_save)
        self.__toolBar.addAction(self.__toolBar_help)

        # 添加菜单
        self.addToolBar(self.__toolBar)
        self.setStatusBar(self.__statusBar)
        self.setCentralWidget(self.contents)

    @QtCore.Slot()
    def __open_file(self):
        fileName, filter = QFileDialog.getOpenFileName(self,
                                                       "打开文件",
                                                       "/",
                                                       " files (*.pdf)")
        if fileName != '':
            self.filePath = fileName
            self.__toolBar_output.setDisabled(True)
            self.__toolBar_input.setDisabled(True)
            self.__toolBar_save.setDisabled(True)
            self.OPEN.emit(self.filePath)

    def open_file_end(self):
        self.__toolBar_output.setEnabled(True)
        self.__toolBar_input.setEnabled(True)
        self.__toolBar_save.setEnabled(True)

    def __output_file(self):
        if self.filePath == '':
            self.__msgbox.setText("请先选择文件")
            self.__msgbox.setStandardButtons(
                 QMessageBox.Ok)
            self.__msgbox.show()
            return

        fileName, filter = QFileDialog.getSaveFileName(self,
                                                       "保存文件",
                                                       "/",
                                                       " files (*.txt)")
        if fileName != '':
            self.OUTPUT.emit(fileName)

    def __input_file(self):
        flag = QMessageBox.Ok
        if not self.window().contents.isEmpty():
            self.__msgbox.setText("导入的目录将覆盖下方的目录树")
            self.__msgbox.setStandardButtons(
                QMessageBox.Ok|QMessageBox.Cancel)
            flag = self.__msgbox.exec()

        if flag == QMessageBox.Cancel:
            return

        fileName, filter = QFileDialog.getOpenFileName(self,
                                                       "打开文件",
                                                       "/",
                                                       " files (*.txt)")
        if fileName != '':
            self.__toolBar_file.setDisabled(True)
            self.__toolBar_output.setDisabled(True)
            self.__toolBar_save.setDisabled(True)
            self.INPUT.emit(fileName)

    def input_file_end(self):
        self.__toolBar_output.setEnabled(True)
        self.__toolBar_file.setEnabled(True)
        self.__toolBar_save.setEnabled(True)

    def __save_file(self):

        if self.filePath == '':
            self.__msgbox.setText("请先选择文件")
            self.__msgbox.setStandardButtons(
                 QMessageBox.Ok)
            self.__msgbox.show()
            return

        fileName= QFileDialog.getExistingDirectory(self,
                                                       "保存路径",
                                                       "/")
        if fileName != '':
            self.contents.dis_btn()
            self.contents.dis_content()
            self.__toolBar_file.setDisabled(True)
            self.__toolBar_input.setDisabled(True)
            self.__toolBar_output.setDisabled(True)
            dir, file = os.path.split(self.filePath)
            self.SAVE.emit(os.path.join(fileName, f"加目录-{file}"), self.contents.get_shift())


    def save_end(self):
        self.contents.saved()
        self.__toolBar_file.setEnabled(True)
        self.__toolBar_input.setEnabled(True)
        self.__toolBar_output.setEnabled(True)

    def __help(self):
        if self.helps is None:
            self.helps = helps.Help()

        self.helps.show()

    def error(self, error):
        self.__msgbox.setText(f"{error}")
        self.__msgbox.setStandardButtons(
            QMessageBox.Ok)
        self.__msgbox.show()


from PySide6.QtWidgets import QApplication
import ctypes

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication([])
    app.setStyle('fusion')
    window = Window()
    window.show()
    app.exec()
