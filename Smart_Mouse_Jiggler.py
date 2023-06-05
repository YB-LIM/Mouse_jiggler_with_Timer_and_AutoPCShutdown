"""
Smart Mouse Jiggler: Mouse jiggler with Timer and Automatic PC shutdown 

AUTHOR: Youngbin LIM
CONTACT: lyb0684@naver.com
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSpinBox, QCheckBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import pyautogui
import os
import random

# Get the directory of the main script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the icon image file
icon_path = os.path.join(script_directory, 'Icon.png')


class TimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Timer Status')  # Set the title for the secondary window
        self.time_label = QLabel(self)
        self.stop_btn = QPushButton('Stop Timer', self)
        self.stop_btn.clicked.connect(self.parent().start_timer)  # Link stop button to start_timer method of parent

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.stop_btn)
        self.setLayout(vbox)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_mouse)

        self.shutdown_timer = QTimer()
        self.shutdown_timer.timeout.connect(self.shutdown)

        self.time_dialog = TimeDialog(self)
        self.time_dialog_timer = QTimer()
        self.time_dialog_timer.timeout.connect(self.update_time_dialog)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Smart Mouse Jiggler')
        self.setWindowIcon(QIcon(icon_path))  # Set the window icon

        self.timer_btn = QPushButton('Start Timer', self)
        self.timer_btn.clicked.connect(self.start_timer)

        self.time_input = QSpinBox(self)
        self.time_input.setRange(1, 999)  # Limit input to a range of 1 to 120 minutes for example
        self.time_input.setValue(1)  # Set a default value

        self.shutdown_check = QCheckBox('Shutdown PC when time is up                       ', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.timer_btn)
        vbox.addWidget(QLabel('Minutes until action:'))
        vbox.addWidget(self.time_input)
        vbox.addWidget(self.shutdown_check)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def start_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.shutdown_timer.stop()
            self.timer_btn.setText('Start Timer')
            self.time_dialog_timer.stop()
            self.time_dialog.stop_btn.setText('Stop Timer')
            self.time_dialog.close()
        else:
            self.timer.start(5000)  # 5000 ms is 5 seconds
            self.shutdown_timer.start(self.time_input.value() * 60000)  # Convert minutes to milliseconds
            self.timer_btn.setText('Stop Timer')
            self.time_dialog.stop_btn.setText('Click to Stop Timer')
            self.time_dialog.show()
            self.time_dialog_timer.start(1000)  # Update every second

    def move_mouse(self):
        x, y = pyautogui.position()
        pyautogui.moveTo(x + random.randint(-1, 1), y + random.randint(-1, 1))

    def shutdown(self):
        if self.shutdown_check.isChecked():
            os.system('shutdown /s /t 1')

    def update_time_dialog(self):
        time_left_sec = self.shutdown_timer.remainingTime() // 1000
        self.time_dialog.time_label.setText(f"Time left: {time_left_sec} seconds...           ")
        if time_left_sec <= 0:
            self.time_dialog_timer.stop()
            self.time_dialog.close()
            self.timer_btn.setText('Start Timer')  # Reset the timer button text

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(icon_path))  # Set the app icon
window = MyApp()
window.show()
sys.exit(app.exec_())
