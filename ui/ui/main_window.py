from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from .login_window import LoginWindow
from .register_window import RegisterWindow
from .dashboard_window import DashboardWindow


# Definimos la clase MainWindow que hereda de QMainWindow
class MainWindow(QMainWindow):
    # Constructor de la clase
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank of America - Sistema de Pagos")
        self.setGeometry(500, 200, 800, 600)

        # Inicializar el widget apilado y las ventanas individuales
        self.stacked_widget = QStackedWidget()
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.dashboard_window = None

        # Agregar ventanas de inicio de sesión y registro a la pila
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.register_window)

        # Establecer el widget apilado como el widget central
        self.setCentralWidget(self.stacked_widget)

        # Conectar las señales de las ventanas de inicio de sesión y registro
        self.login_window.login_successful.connect(self.init_dashboard_window)
        self.login_window.open_register_window.connect(self.show_register_window)
        self.register_window.register_completed.connect(self.show_login_window)
        self.register_window.go_to_login.connect(self.show_login_window)

    # Método para inicializar la ventana del tablero
    def init_dashboard_window(self, username):
        # Inicializar la ventana del tablero con el nombre de usuario y añadirla a la pila
        self.dashboard_window = DashboardWindow(username)
        self.stacked_widget.addWidget(self.dashboard_window)
        self.show_dashboard_window()

    # Método para mostrar la ventana de inicio de sesión
    def show_login_window(self):
        self.stacked_widget.setCurrentWidget(self.login_window)

    # Método para mostrar la ventana de registro
    def show_register_window(self):
        self.stacked_widget.setCurrentWidget(self.register_window)

    # Método para mostrar la ventana del tablero
    def show_dashboard_window(self):
        if self.dashboard_window:
            self.stacked_widget.setCurrentWidget(self.dashboard_window)
