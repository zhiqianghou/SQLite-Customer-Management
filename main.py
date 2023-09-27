from PyQt6.QtCore import Qt
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
		edit_menu_item = self.menuBar().addMenu("&Edit")

		add_customer_action = QAction("Add Customer", self)
		add_customer_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_customer_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		search_action = QAction("Search", self)
		edit_menu_item.addAction(search_action)
		search_action.triggered.connect(self.search)

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

	def search(self):
		dialog = SearchDialog()
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
		self.customer_name = QLineEdit()
		self.customer_name.setPlaceholderText("Name:")

		layout.addWidget(label1,0,0)
		layout.addWidget(self.customer_name,0,1)

		# Add combox of customer country
		label2 = QLabel("Customer Country:")
		self.country_name = QComboBox()
		countries = ["USA", "Canada", "Mexico", "Europe", "Asia", "Others"]
		self.country_name.addItems(countries)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(self.country_name, 1, 1)

		# Add mobile widget
		label3 = QLabel("Mobile Number:")
		self.mobile = QLineEdit()
		self.mobile.setPlaceholderText("Mobile Number:")
		layout.addWidget(label3, 2, 0)
		layout.addWidget(self.mobile,2,1)

		# Add a submit button
		button = QPushButton("Submit")
		button.clicked.connect(self.add_customer)
		layout.addWidget(button,3,0,1,2)


		self.setLayout(layout)

	def add_customer(self):
		name = self.customer_name.text()
		country = self.country_name.itemText(self.country_name.currentIndex())
		mobile = self.mobile.text()

		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("INSERT INTO patients (name, course, mobile) VALUES (?,?,?)",
					   (name, country, mobile))
		connection.commit()
		cursor.close()
		connection.close()
		main_window.load_data()


class SearchDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Search Patient")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		# Create layout and input widget
		layout = QVBoxLayout()
		self.patient_name = QLineEdit()
		self.patient_name.setPlaceholderText("Name:")
		layout.addWidget(self.patient_name)

		# Creat Button
		button = QPushButton("Search")
		button.clicked.connect(self.search)
		layout.addWidget(button)

		self.setLayout(layout)


	def search(self):
		name = self.patient_name.text()
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		result = cursor.execute("SELECT * FROM patients WHERE name=?",
								(name,))
		rows = list(result)
		print(rows)
		items = main_window.table.findItems(name, Qt.MatchFlag.MatchContains)
		for item in items:
			main_window.table.item(item.row(), 1).setSelected(True)

		cursor.close()
		connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

