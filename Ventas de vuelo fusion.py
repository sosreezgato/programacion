
import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
    QRadioButton, QButtonGroup, QComboBox, QCheckBox,
    QSpinBox, QDateEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Unificado de Registro y Compra")
        self.setGeometry(100, 100, 600, 600)

        layout = QGridLayout()
        self.setLayout(layout)

        # ---------------- TÍTULO ----------------
        titulo = QLabel("Formulario de Registro y Compra")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo, 0, 0, 1, 2)

        # ---------------- DATOS PERSONALES ----------------
        layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.nombre = QLineEdit()
        layout.addWidget(self.nombre, 1, 1)

        layout.addWidget(QLabel("Apellido:"), 2, 0)
        self.apellido = QLineEdit()
        layout.addWidget(self.apellido, 2, 1)

        layout.addWidget(QLabel("Email:"), 3, 0)
        self.email = QLineEdit()
        layout.addWidget(self.email, 3, 1)

        layout.addWidget(QLabel("Contraseña:"), 4, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password, 4, 1)

        layout.addWidget(QLabel("DNI:"), 5, 0)
        self.dni = QLineEdit()
        layout.addWidget(self.dni, 5, 1)

        layout.addWidget(QLabel("Fecha de nacimiento:"), 6, 0)
        self.fecha_nac = QDateEdit()
        self.fecha_nac.setCalendarPopup(True)
        self.fecha_nac.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_nac, 6, 1)

        # Género
        layout.addWidget(QLabel("Género:"), 7, 0)
        self.rb_masculino = QRadioButton("Masculino")
        self.rb_femenino = QRadioButton("Femenino")
        grupo_genero = QButtonGroup(self)
        grupo_genero.addButton(self.rb_masculino)
        grupo_genero.addButton(self.rb_femenino)
        layout.addWidget(self.rb_masculino, 7, 1)
        layout.addWidget(self.rb_femenino, 7, 1, Qt.AlignRight)

        # País
        layout.addWidget(QLabel("País:"), 8, 0)
        self.cmb_pais = QComboBox()
        self.cmb_pais.addItems(["", "Argentina", "Chile", "Uruguay", "Perú", "México"])
        layout.addWidget(self.cmb_pais, 8, 1)

        # Aceptar términos
        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")
        layout.addWidget(self.chk_terminos, 9, 0, 1, 2)

        # ---------------- DATOS DE VUELO ----------------
        subtitulo = QLabel("Datos del Vuelo")
        subtitulo.setFont(QFont("Arial", 14, QFont.Bold))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo, 10, 0, 1, 2)

        layout.addWidget(QLabel("Origen:"), 11, 0)
        self.origen = QComboBox()
        self.origen.addItems(["", "Santa Fe", "Córdoba", "Buenos Aires"])
        layout.addWidget(self.origen, 11, 1)

        layout.addWidget(QLabel("Destino:"), 12, 0)
        self.destino = QComboBox()
        self.destino.addItems([
            "Seleccione un destino", "Japon", "Alemania", "Peru0",
            "Sudafrica", "Africa", "Rusia", "Ucrania"
        ])
        layout.addWidget(self.destino, 12, 1)

        layout.addWidget(QLabel("Fecha de vuelo:"), 13, 0)
        self.fecha_vuelo = QDateEdit()
        self.fecha_vuelo.setCalendarPopup(True)
        self.fecha_vuelo.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_vuelo, 13, 1)

        self.rb_turista = QRadioButton("Turista")
        self.rb_ejecutiva = QRadioButton("Ejecutiva")
        self.rb_turista.setChecked(True)
        layout.addWidget(self.rb_turista, 14, 0)
        layout.addWidget(self.rb_ejecutiva, 14, 1)

        layout.addWidget(QLabel("Cantidad de pasajeros:"), 15, 0)
        self.cant_pasajeros = QSpinBox()
        self.cant_pasajeros.setRange(1, 10)
        layout.addWidget(self.cant_pasajeros, 15, 1)

        # ---------------- BOTÓN ----------------
        btn_finalizar = QPushButton("Finalizar Registro y Compra")
        btn_finalizar.clicked.connect(self.validar_datos)
        layout.addWidget(btn_finalizar, 16, 0, 1, 2, alignment=Qt.AlignCenter)

        # ---------------- ESTILOS DARK ----------------
        self.setStyleSheet("""
            QWidget { 
                font-family: Arial; 
                font-size: 12pt; 
                background-color: #121212; 
                color: #E0E0E0;
            }
            QLabel {
                font-weight: bold;
                color: #E0E0E0;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 4px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #0078D7;
                background-color: #2A2A2A;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 6px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QRadioButton, QCheckBox {
                color: #E0E0E0;
            }
        """)

    def validar_datos(self):
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        dni = self.dni.text().strip()
        fecha_nac = self.fecha_nac.date()
        hoy = QDate.currentDate()

        genero = "Masculino" if self.rb_masculino.isChecked() else "Femenino" if self.rb_femenino.isChecked() else ""
        pais = self.cmb_pais.currentText()
        terminos = self.chk_terminos.isChecked()

        origen = self.origen.currentText()
        destino = self.destino.currentText()
        fecha_vuelo = self.fecha_vuelo.date()
        clase = "Turista" if self.rb_turista.isChecked() else "Ejecutiva"
        cantidad = self.cant_pasajeros.value()

        # -------- VALIDACIONES --------
        if not (nombre and apellido and email and password and dni and genero and pais):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Email
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            QMessageBox.warning(self, "Error", "Por favor ingresa un email válido.")
            return

        # DNI
        if not dni.isdigit() or len(dni) < 7:
            QMessageBox.warning(self, "Error", "El DNI debe ser numérico y tener al menos 7 dígitos.")
            return

        # Fecha de nacimiento
        if fecha_nac > hoy:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no puede ser futura.")
            return
        if fecha_nac.addYears(13) > hoy:
            QMessageBox.warning(self, "Error", "Debes tener al menos 13 años.")
            return

        if not terminos:
            QMessageBox.warning(self, "Error", "Debes aceptar los términos y condiciones.")
            return

        # Vuelo
        if origen == "" or destino == "Seleccione un destino":
            QMessageBox.warning(self, "Error", "Debe seleccionar origen y destino.")
            return
        if origen == destino:
            QMessageBox.warning(self, "Error", "El origen y destino no pueden ser iguales.")
            return

        # ⚡ NUEVA VALIDACIÓN: Fecha de vuelo no puede ser pasada
        if fecha_vuelo < hoy:
            QMessageBox.warning(self, "Error", "La fecha de vuelo no puede ser anterior al día de hoy.")
            return

        # -------- RESUMEN --------
        resumen = (f"Registro exitoso:\n"
                   f"Nombre: {nombre} {apellido}\n"
                   f"Email: {email}\n"
                   f"DNI: {dni}\n"
                   f"Género: {genero}\n"
                   f"País: {pais}\n"
                   f"Fecha de Nac.: {fecha_nac.toString('dd/MM/yyyy')}\n\n"
                   f"Compra de pasaje:\n"
                   f"Origen: {origen}\n"
                   f"Destino: {destino}\n"
                   f"Fecha de vuelo: {fecha_vuelo.toString('dd/MM/yyyy')}\n"
                   f"Clase: {clase}\n"
                   f"Cantidad de pasajeros: {cantidad}")

        QMessageBox.information(self, "Éxito", resumen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
