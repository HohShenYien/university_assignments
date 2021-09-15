# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QFile, Qt, QEvent

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QIcon, QPixmap

import utils
import rsc


class mainWindow(QMainWindow):
    """
    # Main window, and some initializations
    """
    def __init__(self):
        super(mainWindow, self).__init__()
        self.load_ui() # loading form.ui file

        # Adjusting the window
        self.setWindowTitle("Nutrient Advisor")
        self.setFixedSize(450, 640)
        self.setWindowIcon(QIcon(":/img/icon.png"))

        # Setting essential starting layouts and widgets etc.
        # Also added self.robot for event filter
        scrollWidget = self.findChild(QWidget, "mainArea")
        layout = self.findChild(QVBoxLayout, "verticalLayout")
        layout.setAlignment(Qt.AlignTop)
        scrollWidget.setLayout(layout)
        self.robot = utils.Chat(self, layout)

        # Adding event filters
        self.chatbox = self.findChild(QPlainTextEdit, "chatbox")
        self.chatbox.installEventFilter(self)

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        uic.loadUi(path, self)
        ui_file.close()

    def eventFilter(self, widget, event):
        """
        # This function is for receiving return/enter key from user and submit the chat
        """
        if (event.type() == QEvent.KeyPress and
            widget is self.chatbox):
            key = event.key()
            if key == Qt.Key_Escape:
                widget.clearFocus()
            else:
                if key == Qt.Key_Return or key == Qt.Key_Enter:
                    self.robot.receiveMessage()
                    return True # Do not add another enter inside

        return QWidget.eventFilter(self, widget, event)


if __name__ == "__main__":
    app = QApplication([])
    widget = mainWindow()
    widget.show()

    app.setApplicationName("Nutrient Advisor")
    sys.exit(app.exec_())
