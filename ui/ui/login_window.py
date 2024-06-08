
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from controllers.user_manager import validar_usuario, registrar_usuario

# Definimos la clase LoginWindow que hereda de QWidget
class LoginWindow(QWidget):
    # Definimos señales personalizadas para comunicación entre ventanas
    login_successful = pyqtSignal(str)  # Señal emitida cuando el inicio de sesión es exitoso
    open_register_window = pyqtSignal()  # Señal emitida para abrir la ventana de registro

    # Constructor de la clase
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    # Método para inicializar la interfaz de usuario
    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle("Acceso a Bank of America")
        self.setWindowIcon(QIcon('path/to/bank_icon.png'))
        self.setGeometry(500, 200, 500, 500)

        # Aplicar estilos CSS
        self.setStyleSheet("""
            QMainWindow {
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

        # Creación del layout principal y configuración de widgets
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon('path/to/bank_icon.png').pixmap(100, 100))
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Acceso a Bank of America")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Campos de entrada para nombre de usuario y contraseña
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de Usuario")
        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón de inicio de sesión
        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.on_login_clicked)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Etiqueta para restablecer contraseña
        forgot_password_label = QLabel("<a href='#' style='color: #0052cc;'>Olvidé mi contraseña</a>")
        forgot_password_label.linkActivated.connect(self.forgot_password)
        layout.addWidget(forgot_password_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Etiqueta para registro de usuario
        sign_up_label = QLabel("¿No tienes una cuenta? <a href='#' style='color: #0052cc;'>Regístrate aquí</a>")
        sign_up_label.linkActivated.connect(self.emit_open_register_window)
        layout.addWidget(sign_up_label, alignment=Qt.AlignmentFlag.AlignCenter)

    # Método llamado cuando se hace clic en el botón de inicio de sesión
    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Validar el usuario y contraseña
        if validar_usuario(username, password):
            self.login_successful.emit(username)  # Emitir señal de inicio de sesión exitoso
        else:
            QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")

    # Método para solicitar el restablecimiento de contraseña
    def forgot_password(self):
        username = self.username_input.text()
        if username:
            print(f"Se solicita restablecimiento de contraseña para: {username}")
            # Puedes agregar aquí más lógica para manejar el restablecimiento de contraseña
            QMessageBox.information(self, "Recuperar Contraseña", "Instrucciones enviadas al correo asociado.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingresa tu nombre de usuario.")

    # Método para emitir la señal de abrir la ventana de registro
    def emit_open_register_window(self):
        self.open_register_window.emit()
