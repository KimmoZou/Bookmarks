from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QDialogButtonBox
from resources import resources_rc

class Help(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setStyleSheet(
            "QTextEdit{"
            "border:none;"
            "background:rgb(240, 240, 240)"
            "}"
        )
        self.ok = QDialogButtonBox(QDialogButtonBox.Ok)
        self.text.setReadOnly(True)
        self.setMinimumSize(400, 500)
        self.setWindowTitle("bookmarks")
        self.setWindowIcon(QIcon(r":\icon\icon-app"))
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.ok)
        self.setLayout(self.layout)
        self.__set_text()

        # 事件
        self.ok.clicked.connect(self.close)

    def __set_text(self):
        self.text.setText("<h1>Bookmarks</h1>pdf 目录添加工具")



from PySide6.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication([])
    app.setStyle('fusion')
    window = Help()
    window.show()
    app.exec()
