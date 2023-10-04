from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
	 QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, \
	 QToolBar, QStatusBar, QMessageBox
import sys
from datetime import datetime
from PyQt6.QtGui import QAction, QIcon
import sqlite3



class MainWindow(QMainWindow): # QMainWindow class allow more operation like toolbar, status bar et al.
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Patients Management System")
		self.setMinimumSize(800,600)

		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")
		edit_menu_item = self.menuBar().addMenu("&Edit")

		add_customer_action = QAction(QIcon("icons/add.png"), "Add Customer", self)
		add_customer_action.triggered.connect(self.insert)
		file_menu_item.addAction(add_customer_action)

		about_action = QAction("About", self)
		help_menu_item.addAction(about_action)
		about_action.setMenuRole(QAction.MenuRole.NoRole)

		search_action = QAction(QIcon("icons/search.png"),"Search", self)
		edit_menu_item.addAction(search_action)
		search_action.triggered.connect(self.search)

		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("ID","Name","Country","Mobile"))
		self.table.verticalHeader().setVisible(False)
		self.setCentralWidget(self.table)

		# Create toolbar and add elements
		toolbar = QToolBar()

		toolbar.setMovable(True)
		self.addToolBar(toolbar)
		toolbar.addAction(add_customer_action)
		toolbar.addAction(search_action)

		# Create status bar and add status bar elements
		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)

		# Detect a cell click
		self.table.clicked.connect(self.cell_clicked)


	def cell_clicked(self):
		edit_button = QPushButton("Edit Record")
		edit_button.clicked.connect(self.edit)

		delete_button = QPushButton("Delete Record")
		delete_button.clicked.connect(self.delete)

		children = self.findChildren(QPushButton)
		if children:
			for child in children:
				self.statusbar.removeWidget(child)


		self.statusbar.addWidget(edit_button)
		self.statusbar.addWidget(delete_button)

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

	def edit(self):
		dialog = EditDialog()
		dialog.exec()

	def delete(self):
		dialog = DeleteDialog()
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


class EditDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Update Customer Information")
		self.setFixedWidth(300)
		self.setFixedHeight(300)

		layout = QGridLayout()

		# Get customer name form the selected row.
		index = main_window.table.currentRow()
		customer_name = main_window.table.item(index, 1).text()

		# Get id from the selected row:
		self.customer_id = main_window.table.item(index, 0).text()

		# update customer name widget
		label1 = QLabel("Customer Name:")
		self.customer_name = QLineEdit(customer_name)
		self.customer_name.setPlaceholderText("Name:")

		layout.addWidget(label1,0,0)
		layout.addWidget(self.customer_name,0,1)

		# update combox of customer country
		country_name = main_window.table.item(index, 2).text()
		label2 = QLabel("Customer Country:")
		self.country_name = QComboBox()
		countries = ["USA", "Canada", "Mexico", "Europe", "Asia", "Others"]
		self.country_name.addItems(countries)
		self.country_name.setCurrentText(country_name)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(self.country_name, 1, 1)

		# update mobile widget
		mobile = main_window.table.item(index,3).text()
		label3 = QLabel("Mobile Number:")
		self.mobile = QLineEdit(mobile)
		self.mobile.setPlaceholderText("Mobile Number:")
		layout.addWidget(label3, 2, 0)
		layout.addWidget(self.mobile,2,1)

		# Add a submit button
		button = QPushButton("Update")
		button.clicked.connect(self.update_customer)
		layout.addWidget(button,3,0,1,2)

		self.setLayout(layout)

	def update_customer(self):
		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("UPDATE patients SET name = ?, course = ?, mobile = ? WHERE id =?",
					   (self.customer_name.text(),
						self.country_name.itemText(self.country_name.currentIndex()),
						self.mobile.text(),
						self.customer_id ))
		connection.commit()
		cursor.close()
		connection.close()

		# Refresh the table
		main_window.load_data()


class DeleteDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Delete Customer Information")

		layout = QGridLayout()
		confirmation = QLabel("Are you sure you want to delete?")
		yes = QPushButton("Yes")
		no = QPushButton("No")

		layout.addWidget(confirmation, 0, 0, 1, 2)
		layout.addWidget(yes, 1, 0, 1, 1)
		layout.addWidget(no, 1, 1, 1, 1)
		self.setLayout(layout)

		yes.clicked.connect(self.delete_customer)


	def delete_customer(self):
		# Get index and customer_id
		index = main_window.table.currentRow()
		customer_id = main_window.table.item(index, 0).text()

		connection = sqlite3.connect("database.db")
		cursor = connection.cursor()
		cursor.execute("DELETE from patients WHERE id = ?",
					   (customer_id,))
		connection.commit()
		cursor.close()
		connection.close()
		main_window.load_data()

		self.close()

		confirmation_widget = QMessageBox()
		confirmation_widget.setWindowTitle("Success")
		confirmation_widget.setText("The record has been deleted successfully!")
		confirmation_widget.exec()



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

