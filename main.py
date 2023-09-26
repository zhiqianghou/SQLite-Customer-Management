from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
	 QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox
import sys
from datetime import datetime
from PyQt6.QtGui import QAction
import sqlite3



class MainWindow(QMainWindow): # QMainWindow class allow more operation like toolbar, status bar et al.
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Patients Management System")

		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		add_customer_action = QAction("Add Customer", self)
		add_customer_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_customer_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("ID","Name","Country","Mobile"))
		self.table.verticalHeader().setVisible(False)
		self.setCentralWidget(self.table)

	def load_data(self):
		connection = sqlite3.connect("database.db")
		result = connection.execute("select * from patients")
		self.table.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.table.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
		connection.close()

	def insert(self):
		dialog = InsertDialog()
		dialog.exec()


class InsertDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Add Customer Information")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		layout = QGridLayout()

		# Add customer name widget
		label1 = QLabel("Customer Name:")
		customer_name = QLineEdit()
		customer_name.setPlaceholderText("Name:")

		layout.addWidget(label1,0,0)
		layout.addWidget(customer_name,0,1)

		# Add customer country widget
		label2 = QLabel("Customer Country:")
		country_name = QComboBox()
		countries = ["USA", "Canada", "Mexico", "Europe", "Asia", "Others"]
		country_name.addItems(countries)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(country_name, 1, 1)





		self.setLayout(layout)







app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

