from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, pyqtSignal

# Importamos la función para registrar usuarios desde el controlador
from controllers.user_manager import registrar_usuario

# Definimos la clase RegisterWindow que hereda de QWidget
class RegisterWindow(QWidget):
    # Definimos señales personalizadas para comunicarse con otros componentes
    register_completed = pyqtSignal()
    go_to_login = pyqtSignal()

    # Constructor de la clase
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    # Método para inicializar la interfaz de usuario
    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle("Acceso a Bank of America")
        self.setWindowIcon(QIcon('path/to/bank_icon.png'))
        self.setGeometry(500, 200, 700, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
            QLabel, QLineEdit {
                font-size: 16px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                margin-top: 15px;
                background-color: #0052cc;
                color: white;
                border-radius: 5px;
            }
        """)

        # Configuración del diseño de la ventana
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Registro de Usuario")
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Campos de entrada para nombre de usuario, correo electrónico y contraseña
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario a Registrar")
        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Gmail")
        layout.addWidget(self.email_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar Contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón para registrar un nuevo usuario
        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón para ir a la pantalla de inicio de sesión
        self.go_to_login_button = QPushButton('Volver al inicio', self)
        self.go_to_login_button.clicked.connect(self.on_go_to_login_clicked)
        layout.addWidget(self.go_to_login_button, alignment=Qt.AlignmentFlag.AlignCenter)

    # Método para registrar un nuevo usuario
    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validación de campos obligatorios
        if not all([username, email, password, confirm_password]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Validación de coincidencia de contraseñas
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas es incorrecta.")
            return

        try:
            # Llamamos al controlador para registrar al usuario
            registrar_usuario(username, password, email)
            QMessageBox.information(self, "Registro Exitoso", "Puedes Ingresar secion.")
            # Emitimos la señal de registro completado
            self.register_completed.emit()
        except Exception as e:
            QMessageBox.warning(self, "Registro Fallido", str(e))

    # Método para ir a la pantalla de inicio de sesión
    def on_go_to_login_clicked(self):
        self.go_to_login.emit()
