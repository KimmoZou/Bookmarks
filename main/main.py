from PySide6.QtWidgets import QApplication
from model import actions
from controller import handler
from view import window
import ctypes


class Main(object):

    def __init__(self):
        self.__app = QApplication([])
        self.__app.setStyle('fusion')
        self.__window = window.Window()
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        self.__handler = handler.HandlerTask()
        self.__window.OPEN.connect(self.__open_signal)
        self.__window.OUTPUT.connect(self.__output_signal)
        self.__window.INPUT.connect(self.__input_signal)
        self.__window.SAVE.connect(self.__save_signal)

    def __open_signal(self, file):
        self.__window.contents.clear()
        self.__handler.handler_open(file,
                                    [self.__window.contents.init_tree],
                                    [self.__window.contents.update_btn, self.__window.open_file_end]
                                    )

    def __output_signal(self, file):
        action = actions.OutputAction()
        action.set_path(file)
        self.__handler.handler_output(action)

    def __input_signal(self, file):
        self.__window.contents.clear()
        self.__handler.handler_input(actions.InputAction(file),
                                     [self.__window.contents.init_tree],
                                     [self.__window.contents.update_btn, self.__window.input_file_end]
                                     )

    def __save_signal(self, file, shift):
        self.__handler.handler_save(actions.SaveAction(path=file,
                                                       shift=shift,
                                                       treeRoot=self.__window.contents.get_root()),
                                    [],
                                    [self.__window.save_end],
                                    [self.__window.error, self.__window.save_end]
                                    )

    def main(self):
        self.__window.show()
        self.__app.exec()


if __name__ == "__main__":
    Main().main()
