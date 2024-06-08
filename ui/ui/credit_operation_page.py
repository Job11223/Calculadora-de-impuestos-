from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox,  # type: ignore
    QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt # type: ignore
from PyQt6.QtGui import QFont # type: ignore

# Definimos la clase CreditOperationPage que hereda de QWidget
class CreditOperationPage(QWidget):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    # Método para configurar la interfaz de usuario
    def setup_ui(self):
        # Aplicar el estilo CSS
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
            }
            QLabel {
                padding-bottom: 5px;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox {
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

        # Configuración de la fuente para el título
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)

        # Creación del título de la página
        title_label = QLabel('Registro de Operación de Crédito')
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # Campo de entrada para el monto del crédito
        self.layout.addWidget(QLabel('Monto del Crédito:'))
        self.amount_input = QLineEdit(self)
        self.layout.addWidget(self.amount_input)

        # Campo de entrada para la tasa de interés anual
        self.layout.addWidget(QLabel('Tasa de Interés (% anual):'))
        self.interest_rate_input = QDoubleSpinBox(self)
        self.interest_rate_input.setRange(0, 100)
        self.layout.addWidget(self.interest_rate_input)

        # Campo de entrada para el plazo en meses
        self.layout.addWidget(QLabel('Plazo (meses):'))
        self.term_input = QSpinBox(self)
        self.term_input.setRange(1, 360)
        self.layout.addWidget(self.term_input)

        # Botón para calcular la tabla de pagos
        self.calculate_button = QPushButton('Calcular Tabla de Pagos', self)
        self.calculate_button.clicked.connect(self.calculate_payment_table)
        self.layout.addWidget(self.calculate_button)

        # Tabla para mostrar la tabla de pagos
        self.payment_table = QTableWidget(self)
        self.payment_table.setColumnCount(3)
        self.payment_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.payment_table.setHorizontalHeaderLabels(['Fecha', 'Cuota', 'Saldo Pendiente'])
        self.layout.addWidget(self.payment_table)
        
        

    # Método para calcular y mostrar la tabla de pagos
    def calculate_payment_table(self):
        try:
            # Validar y convertir la entrada del usuario
            principal_text = self.amount_input.text().strip()
            interest_rate_text = self.interest_rate_input.text().strip()
            term_text = self.term_input.text().strip()

            if not principal_text or not interest_rate_text or not term_text:
                raise ValueError("Todos los campos son obligatorios.")

            principal = float(principal_text)
            # Convertir a decimal
            annual_interest_rate = self.interest_rate_input.value() / 100  
            term_months = int(term_text)

            if principal <= 0 or annual_interest_rate <= 0 or term_months <= 0:
                raise ValueError("Los valores deben ser mayores que cero.")
            

            # Calcular la tasa de interés mensual
            monthly_interest_rate = annual_interest_rate / 12

            # Calcular el pago mensual
            monthly_payment = principal * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_months))

            # Inicializar el saldo pendiente
            outstanding_balance = principal

            # Limpiar la tabla actual
            self.payment_table.setRowCount(0)

            # Llenar la tabla de pagos
            for month in range(1, term_months + 1):
                # Calcular el interés del período
                interest_payment = outstanding_balance * monthly_interest_rate
                # Calcular el capital pagado
                principal_payment = monthly_payment - interest_payment
                # Actualizar el saldo pendiente
                outstanding_balance -= principal_payment
                    
                # Añadir la fila a la tabla
                self.payment_table.insertRow(self.payment_table.rowCount())
                self.payment_table.setItem(self.payment_table.rowCount() - 1, 0, QTableWidgetItem(str(month)))
                self.payment_table.setItem(self.payment_table.rowCount() - 1, 1, QTableWidgetItem(f'{monthly_payment:.2f}'))
                self.payment_table.setItem(self.payment_table.rowCount() - 1, 2, QTableWidgetItem(f'{outstanding_balance:.2f}'))

        except ValueError as e:
            QMessageBox.warning(self, 'Entrada inválida', str(e))



