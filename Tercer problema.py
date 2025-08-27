import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGridLayout, QDateEdit
)
from PyQt5.QtCore import QDate

class RegistroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Formulario de Registro")

        layout = QGridLayout()

        # Nombre
        layout.addWidget(QLabel("Nombre:"), 0, 0)
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input, 0, 1)

        # Email
        layout.addWidget(QLabel("Email:"), 1, 0)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input, 1, 1)

        # Fecha de nacimiento
        layout.addWidget(QLabel("Fecha de nacimiento:"), 2, 0)
        self.fecha_nac_input = QDateEdit()
        self.fecha_nac_input.setCalendarPopup(True)
        self.fecha_nac_input.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_nac_input, 2, 1)

        # Botón de registro
        self.registrar_btn = QPushButton("Registrarse")
        self.registrar_btn.clicked.connect(self.registrar)
        layout.addWidget(self.registrar_btn, 3, 0, 1, 2)

        self.setLayout(layout)

    def registrar(self):
        nombre = self.nombre_input.text().strip()
        email = self.email_input.text().strip()
        fecha_nac = self.fecha_nac_input.date()
        hoy = QDate.currentDate()

        # Validaciones
        if not nombre or not email:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Validación de email (regex simple)
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            QMessageBox.warning(self, "Error", "Por favor ingresa un email válido.")
            return

        if fecha_nac > hoy:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no puede ser posterior a hoy.")
            return

        if fecha_nac.addYears(13) > hoy:
            QMessageBox.warning(self, "Error", "Debes tener al menos 13 años para registrarte.")
            return

        QMessageBox.information(self, "Éxito", f"Registro completado.\n¡Bienvenido/a {nombre}!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RegistroApp()
    ventana.show()
    sys.exit(app.exec_())
