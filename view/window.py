from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QStatusBar
)

from resources import resources_rc
from view import content


class Window(QMainWindow):
    def __init__(self):
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
        self.__toolBar_output = QAction(QIcon(r":\icon\icon-output"), "导出目录", self)
        self.__toolBar_input = QAction(QIcon(r":\icon\icon-input"), "导入目录", self)
        self.__toolBar_save = QAction(QIcon(r":\icon\icon-save"), "保存文件", self)
        self.__toolBar_help = QAction(QIcon(r":\icon\icon-help"), "使用帮助", self)
        # 状态栏
        self.__statusBar = QStatusBar(self)
        # 内容
        self.__contents = content.Contents()


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
        self.setCentralWidget(self.__contents)


from PySide6.QtWidgets import QApplication
import ctypes

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication([])
    app.setStyle('fusion')
    window = Window()
    window.show()
    app.exec()
