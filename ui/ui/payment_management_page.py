from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QFormLayout, QLineEdit, QDateEdit, QSizePolicy, QHeaderView

)
from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt

# Definimos la clase PaymentManagementPage que hereda de QWidget
class PaymentManagementPage(QWidget):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.payments = []

        # Crear la tabla de operaciones de crédito
        self.credit_operations_table = QTableWidget(0, 4)  # 0 filas inicialmente y 4 columnas
        self.credit_operations_table.setHorizontalHeaderLabels(['ID Operación', 'Cliente', 'Monto Total', 'Saldo Pendiente'])
        self.credit_operations_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.credit_operations_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.credit_operations_table)
       
        # Crear los campos de entrada para registrar un nuevo pago
        self.form_layout = QFormLayout()
        self.payment_date_input = QDateEdit()
        self.payment_date_input.setDate(QDate.currentDate())
        self.payment_amount_input = QLineEdit()

        self.form_layout.addRow('Fecha de Pago:', self.payment_date_input)
        self.form_layout.addRow('Monto del Pago:', self.payment_amount_input)

        # Botones para acciones
        self.add_payment_button = QPushButton('Añadir Pago')
        self.update_payment_button = QPushButton('Actualizar Pago')
        self.delete_payment_button = QPushButton('Eliminar Pago')

        # Conectar botones con métodos
        self.add_payment_button.clicked.connect(self.add_payment)
        self.update_payment_button.clicked.connect(self.update_payment)
        self.delete_payment_button.clicked.connect(self.delete_payment)

        # Layout para botones
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_payment_button)
        self.buttons_layout.addWidget(self.update_payment_button)
        self.buttons_layout.addWidget(self.delete_payment_button)

        # Añadir form y botones al layout principal
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)

        # Aplicar el estilo CSS
        self.apply_styles()

    # Método para aplicar estilos CSS
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
            }
            QLabel {
                padding-bottom: 5px;
            }
            QLineEdit, QDateEdit {
                padding: 5px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px 15px;
                border-radius: 5px;
                background-color: #0052cc;
                color: white;
            }
            QPushButton:hover {
                background-color: #003f8c;
            }
            QTableWidget {
                border: none;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 5px;
                border: 1px solid #e0e0e0;
                font-size: 14px;
            }
        """)

    # Método para agregar un nuevo pago
    def add_payment(self):
        if self.validate_payment_input():
            new_payment = {
                'date': self.payment_date_input.date().toString(Qt.DateFormat.ISODate),
                'amount': float(self.payment_amount_input.text())
            }
            self.payments.append(new_payment)
            self.update_payments_table()

    # Método para actualizar un pago existente
    def update_payment(self):
        selected_payment = self.get_selected_payment()
        if selected_payment and self.validate_payment_input():
            selected_payment['date'] = self.payment_date_input.date().toString(Qt.DateFormat.ISODate)
            selected_payment['amount'] = float(self.payment_amount_input.text())
            self.update_payments_table()

    # Método para eliminar un pago
    def delete_payment(self):
        selected_payment = self.get_selected_payment()
        if selected_payment:
            self.payments.remove(selected_payment)
            self.update_payments_table()

    # Método para validar la entrada del pago
    def validate_payment_input(self):
        try:
            amount = float(self.payment_amount_input.text())
            if amount <= 0:
                raise ValueError("El monto del pago debe ser positivo.")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")  # Reemplaza esto con una alerta de usuario adecuada
            return False

    # Método para obtener el pago seleccionado en la tabla
    def get_selected_payment(self):
        selected_indices = self.credit_operations_table.selectedIndexes()

        if selected_indices:
            selected_row = selected_indices[0].row()
            return self.payments[selected_row]
        return None

    # Método para actualizar la tabla de pagos
    def update_payments_table(self):
        self.credit_operations_table.clearContents()
        self.credit_operations_table.setRowCount(len(self.payments))
        for row, payment in enumerate(self.payments):
            self.credit_operations_table.setItem(row, 0, QTableWidgetItem(payment['date']))
            self.credit_operations_table.setItem(row, 1, QTableWidgetItem(str(payment['amount'])))
