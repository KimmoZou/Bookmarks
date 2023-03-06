from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QTreeWidgetItem, QStyleOption, QStyle




class Item(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)

    def set_value(self, txt1, txt2):
        self.setText(0, txt1)
        self.setText(1, txt2)
