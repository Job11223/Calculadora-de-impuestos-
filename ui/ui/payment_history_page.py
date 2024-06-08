from PyQt6.QtWidgets import (
        QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
        QPushButton, QFileDialog, QMessageBox
)

from PyQt6.QtGui import QFont
from controllers.user_manager import obtener_historial_pagos
import csv


# Definimos la clase PaymentHistoryPage que hereda de QWidget
class PaymentHistoryPage(QWidget):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Método para inicializar la interfaz de usuario
    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Configuración del título de la página
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)

        title_label = QLabel('Historial de Pagos')
        title_label.setFont(title_font)
        self.layout.addWidget(title_label)

        # Configuración de la tabla para mostrar el historial de pagos
        self.payment_history_table = QTableWidget(0, 4)  # 0 filas inicialmente y 4 columnas
        self.payment_history_table.setHorizontalHeaderLabels(['Fecha de Pago', 'Monto', 'ID Operación', 'Cliente'])
        self.layout.addWidget(self.payment_history_table)

        self.export_button = QPushButton('Exportar a CSV')
        self.export_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_button)

        # Aplicar estilos CSS
        self.apply_styles()

        # Cargar el historial de pagos
        self.load_payment_history()

    # Método para aplicar estilos CSS
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
            }
            QLabel {
                padding-bottom: 5px;
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
            /* Puedes añadir más estilos aquí según sea necesario */
        """)

    # Método para cargar el historial de pagos
    def load_payment_history(self):
        try:
            # Obtener el historial de pagos desde el controlador
            for payment in obtener_historial_pagos():
                row_count = self.payment_history_table.rowCount()
                self.payment_history_table.insertRow(row_count)
                self.payment_history_table.setItem(row_count, 0, QTableWidgetItem(payment['fecha']))
                self.payment_history_table.setItem(row_count, 1, QTableWidgetItem(str(payment['monto'])))
                self.payment_history_table.setItem(row_count, 2, QTableWidgetItem(payment['id_operacion']))
                self.payment_history_table.setItem(row_count, 3, QTableWidgetItem(payment['cliente']))
        except Exception as e:
            print(f"Error al cargar el historial de pagos: {e}")

    # Método para exportar el historial de pagos a un archivo CSV
    def export_to_csv(self):
        try:
            # Abrir cuadro de diálogo para que el usuario elija dónde guardar el archivo CSV
            path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo CSV", "", "CSV Files (*.csv)")
            if path:
                with open(path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    # Escribir el encabezado de la tabla
                    headers = [self.payment_history_table.horizontalHeaderItem(i).text() for i in range(self.payment_history_table.columnCount())]
                    writer.writerow(headers)
                    # Escribir el contenido de la tabla
                    for row in range(self.payment_history_table.rowCount()):
                        row_data = [self.payment_history_table.item(row, col).text() if self.payment_history_table.item(row, col) else '' for col in range(self.payment_history_table.columnCount())]
                        writer.writerow(row_data)
                QMessageBox.information(self, "Exportar a CSV", "El historial de pagos ha sido exportado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error al exportar a CSV: {e}")
    

