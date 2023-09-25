from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
	 QLineEdit, QPushButton, QMainWindow, QTableWidget
import sys
from datetime import datetime
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow): # QMainWindow class allow more operation like toolbar, status bar et al.
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Patients Management System")

		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		add_student_action = QAction("Add Student", self)
		file_menu_item.addAction(add_student_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("ID","Name","Country","Mobile"))
		self.setCentralWidget(self.table)





app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
sys.exit(app.exec())

