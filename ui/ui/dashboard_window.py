# Importamos los módulos y clases necesarios de PyQt6
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QHBoxLayout, QStackedWidget, QPushButton
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt

# Importamos las clases de las páginas de la aplicación
from .credit_operation_page import CreditOperationPage
from .payment_management_page import PaymentManagementPage
from .payment_history_page import PaymentHistoryPage


# Definimos la clase DashboardWindow que hereda de QMainWindow
class DashboardWindow(QMainWindow):
    # Constructor de la clase que recibe el nombre de usuario como parámetro
    def __init__(self, username=None):
        super().__init__()
        # Guardar el nombre de usuario como atributo de la clase
        self.username = username  
        self.setWindowTitle('Bank of America - Sistema de Pagos')
        self.setGeometry(700, 200, 724, 568)
        self.init_ui()

    # Método para inicializar la interfaz de usuario
    def init_ui(self):
        # Crear la barra lateral para la navegación
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(200)
        self.sidebar.addItem('Registro de Operación de Crédito')
        self.sidebar.addItem('Generación Tabla de Pagos')
        self.sidebar.addItem('Gestión de Pagos')
        self.sidebar.addItem('Traslado Histórico de Pagos')

        # Crear el widget de pila para el contenido principal
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_credit_operation_page())  # Registro de operación de crédito
        self.stacked_widget.addWidget(self.create_payment_table_page())     # Generación de tabla de pagos
        self.stacked_widget.addWidget(self.create_payment_management_page())# Gestión de pagos
        self.stacked_widget.addWidget(self.create_payment_history_page())   # Traslado histórico de pagos

        # Conectar la barra lateral con el cambio de página en el contenido principal
        self.sidebar.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        # Crear un widget central y establecer el layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Aplicar estilos CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5; /* Color de fondo claro */
            }
            QListWidget {
                background-color: #ffffff; /* Fondo blanco para la barra lateral */
                border: none;
                border-right: 1px solid #e1e4e8; /* Divisor sutil */
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #e7e7e7; /* Efecto hover suave */
            }
            QListWidget::item:selected {
                background-color: #d1d8e0; /* Selección con color más pronunciado */
                color: #333333;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333; /* Texto oscuro para contraste */
                padding: 5px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #0052cc;
                color: white;
                border-radius: 5px;
                padding: 12px 24px;
                margin: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #003f8c;
                transition: background-color 0.3s;
            }
            /* Aquí puedes añadir más estilos para otros widgets */
        """)

    # Método para crear la página de registro de operación de crédito
    def create_credit_operation_page(self):
        # Página para registro de operación de crédito
        page = CreditOperationPage()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel('Registro de Operación de Crédito'))
        # Aquí agregarías más controles para esta página
        return page

    # Método para crear la página de generación de la tabla de pagos
    def create_payment_table_page(self):
        # Página para generación de la tabla de pagos
        page = PaymentManagementPage()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel('Generación Tabla de Pagos'))
        # Aquí agregarías más controles para esta página
        return page

    # Método para crear la página de gestión de pagos
    def create_payment_management_page(self):
        # Página para gestión de pagos
        page = PaymentManagementPage()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel('Gestión de Pagos'))
        # Aquí agregarías más controles para esta página
        return page

    # Método para crear la página de traslado histórico de pagos
    def create_payment_history_page(self):
        # Página para traslado histórico de pagos
        page = PaymentHistoryPage()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel('Traslado Histórico de Pagos'))
        # Aquí agregarías más controles para esta página
        return page
