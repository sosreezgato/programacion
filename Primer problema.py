import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
    QComboBox, QDateEdit, QRadioButton, QSpinBox,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compra de Pasaje Aéreo")
        self.setGeometry(100, 100, 500, 350)
        layout = QGridLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel("Formulario de Compra")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo, 0, 0, 1, 2)

        # Datos del pasajero
        layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.nombre = QLineEdit()
        layout.addWidget(self.nombre, 1, 1)

        layout.addWidget(QLabel("Apellido:"), 2, 0)
        self.apellido = QLineEdit()
        layout.addWidget(self.apellido, 2, 1)

        layout.addWidget(QLabel("DNI:"), 3, 0)
        self.dni = QLineEdit()
        layout.addWidget(self.dni, 3, 1)

        # Vuelo
        layout.addWidget(QLabel("Origen:"), 4, 0)
        self.origen = QComboBox()
        self.origen.addItems(["", "Buenos Aires", "Córdoba", "Mendoza"])
        layout.addWidget(self.origen, 4, 1)

        layout.addWidget(QLabel("Destino:"), 5, 0)
        self.destino = QComboBox()
        self.destino.addItems(["", "Madrid", "Miami", "Santiago de Chile"])
        layout.addWidget(self.destino, 5, 1)

        layout.addWidget(QLabel("Fecha de vuelo:"), 6, 0)
        self.fecha = QDateEdit()
        self.fecha.setDate(QDate.currentDate())
        self.fecha.setCalendarPopup(True)
        layout.addWidget(self.fecha, 6, 1)

        # Clase y pasajeros
        self.rb_turista = QRadioButton("Turista")
        self.rb_ejecutiva = QRadioButton("Ejecutiva")
        self.rb_turista.setChecked(True)
        layout.addWidget(self.rb_turista, 7, 0)
        layout.addWidget(self.rb_ejecutiva, 7, 1)

        layout.addWidget(QLabel("Cantidad de pasajeros:"), 8, 0)
        self.cant_pasajeros = QSpinBox()
        self.cant_pasajeros.setRange(1, 10)
        layout.addWidget(self.cant_pasajeros, 8, 1)

        # Botón
        self.btn_comprar = QPushButton("Comprar")
        self.btn_comprar.clicked.connect(self.validar_datos)
        layout.addWidget(self.btn_comprar, 9, 0, 1, 2)

        # Estilos
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 12pt;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox {
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 4px;
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
        """)

    def validar_datos(self):
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        dni = self.dni.text().strip()
        origen = self.origen.currentText()
        destino = self.destino.currentText()

        # Validaciones básicas
        if not nombre or not apellido or not dni:
            QMessageBox.warning(self, "Error", "Todos los campos personales son obligatorios.")
            return

        if not dni.isdigit() or len(dni) < 7:
            QMessageBox.warning(self, "Error", "El DNI debe ser numérico y tener al menos 7 dígitos.")
            return

        if origen == "" or destino == "":
            QMessageBox.warning(self, "Error", "Debe seleccionar origen y destino.")
            return

        if origen == destino:
            QMessageBox.warning(self, "Error", "El origen y destino no pueden ser iguales.")
            return

        # Si pasa las validaciones → mostrar resumen
        self.mostrar_resumen()

    def mostrar_resumen(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        dni = self.dni.text()
        origen = self.origen.currentText()
        destino = self.destino.currentText()
        fecha = self.fecha.date().toString("dd/MM/yyyy")
        clase = "Turista" if self.rb_turista.isChecked() else "Ejecutiva"
        cantidad = self.cant_pasajeros.value()

        resumen = (f"Nombre: {nombre} {apellido}\n"
                   f"DNI: {dni}\n"
                   f"Origen: {origen}\n"
                   f"Destino: {destino}\n"
                   f"Fecha: {fecha}\n"
                   f"Clase: {clase}\n"
                   f"Cantidad de pasajeros: {cantidad}")

        QMessageBox.information(self, "Resumen de Compra", resumen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
