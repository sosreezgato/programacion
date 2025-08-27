import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
    QRadioButton, QButtonGroup, QComboBox, QCheckBox,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 400, 300)

        layout = QGridLayout()
        self.setLayout(layout)

        # -----------------------------------------------------------------------------
        # Ejercicio 1: Título y primer campo
        # -----------------------------------------------------------------------------
        titulo = QLabel("Formulario de Registro")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo, 0, 0, 1, 2)

        lbl_nombre = QLabel("Nombre:")
        self.txt_nombre = QLineEdit()
        layout.addWidget(lbl_nombre, 1, 0)
        layout.addWidget(self.txt_nombre, 1, 1)
###
        # -----------------------------------------------------------------------------
        # Ejercicio 2: Más campos de texto
        #-----------------------------------------------------------------------------
        lbl_email = QLabel("Email:")
        self.txt_email = QLineEdit()
        layout.addWidget(lbl_email, 2, 0)
        layout.addWidget(self.txt_email, 2, 1)

        lbl_pass = QLabel("Contraseña:")
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(lbl_pass, 3, 0)
        layout.addWidget(self.txt_pass, 3, 1)

        # -----------------------------------------------------------------------------
        # Ejercicio 3: Selección de género
        # -----------------------------------------------------------------------------
        lbl_genero = QLabel("Género:")
        layout.addWidget(lbl_genero, 4, 0)

        self.rb_masculino = QRadioButton("Masculino")
        self.rb_femenino = QRadioButton("Femenino")

        grupo_genero = QButtonGroup(self)
        grupo_genero.addButton(self.rb_masculino)
        grupo_genero.addButton(self.rb_femenino)

        layout.addWidget(self.rb_masculino, 4, 1)
        layout.addWidget(self.rb_femenino, 4, 1, Qt.AlignRight)

        # -----------------------------------------------------------------------------
        # Ejercicio 4: Selección de país
        # -----------------------------------------------------------------------------
        lbl_pais = QLabel("País:")
        self.cmb_pais = QComboBox()
        self.cmb_pais.addItems(["Argentina", "Chile", "Uruguay", "Perú", "México"])
        layout.addWidget(lbl_pais, 5, 0)
        layout.addWidget(self.cmb_pais, 5, 1)

        # -----------------------------------------------------------------------------
        # Ejercicio 5: Checkbox de términos
        # -----------------------------------------------------------------------------
        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")
        layout.addWidget(self.chk_terminos, 6, 0, 1, 2)

        # -----------------------------------------------------------------------------
        # Ejercicio 6: Botón de envío y validación
        # -----------------------------------------------------------------------------
        btn_registrar = QPushButton("Registrarse")
        btn_registrar.clicked.connect(self.registrar)
        layout.addWidget(btn_registrar, 7, 0, 1, 2, alignment=Qt.AlignCenter)

        # -----------------------------------------------------------------------------
        # Ejercicio 7: Personalización visual
        # -----------------------------------------------------------------------------
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f7;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    # -----------------------------------------------------------------------------
    # Función de validación (Ejercicio 6)
    # -----------------------------------------------------------------------------
    def registrar(self):
        nombre = self.txt_nombre.text().strip()
        email = self.txt_email.text().strip()
        password = self.txt_pass.text().strip()
        genero = "Masculino" if self.rb_masculino.isChecked() else "Femenino" if self.rb_femenino.isChecked() else ""
        pais = self.cmb_pais.currentText()
        terminos = self.chk_terminos.isChecked()

        if not nombre or not email or not password or not genero or not terminos:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos y acepte los términos.")
        else:
            QMessageBox.information(self, "Éxito", f"Usuario {nombre} registrado con éxito.\nPaís: {pais}, Género: {genero}")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
###