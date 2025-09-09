# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Docentes (PyQt5)
-------------------------------------
- Alta, búsqueda, modificación, eliminación
- Persistencia en archivo de texto: docentes.txt
- Exportación a CSV
"""
import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QMessageBox,
    QFileDialog, QGroupBox, QListWidget, QListWidgetItem, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

SEPARADOR = "|"
ARCHIVO_DATOS = "docentes.txt"

def validar_email(email: str) -> bool:
    # Regex simple pero razonable
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patron, email) is not None

def normalizar_telefono(t: str) -> str:
    # Deja dígitos y + - espacios
    return re.sub(r"[^\d+\-\s]", "", t).strip()

class SistemaDocentes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Docentes")
        self.setGeometry(100, 100, 1000, 700)

        self.archivo_datos = ARCHIVO_DATOS

        self.configurar_interfaz()
        self.aplicar_estilos()
        self.cargar_datos()

    # ----------- UI -----------
    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #495057;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:pressed { background-color: #004085; }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus { border-color: #007bff; }
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
            }
        """)

    def configurar_interfaz(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        splitter.addWidget(self.crear_panel_formulario())
        splitter.addWidget(self.crear_panel_lista())
        splitter.setSizes([420, 580])

    def crear_panel_formulario(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        grupo_form = QGroupBox("Datos del Docente")
        form_layout = QGridLayout()

        # Campos
        self.legajo_edit = QLineEdit(); self.legajo_edit.setPlaceholderText("Ej: DOC001")
        self.nombre_edit = QLineEdit(); self.nombre_edit.setPlaceholderText("Nombre")
        self.apellido_edit = QLineEdit(); self.apellido_edit.setPlaceholderText("Apellido")
        self.dni_edit = QLineEdit(); self.dni_edit.setPlaceholderText("DNI")
        self.email_edit = QLineEdit(); self.email_edit.setPlaceholderText("correo@ejemplo.com")
        self.telefono_edit = QLineEdit(); self.telefono_edit.setPlaceholderText("+54 9 11 1234-5678")
        self.materia_edit = QLineEdit(); self.materia_edit.setPlaceholderText("Materia")
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Titular", "Asociado", "Adjunto", "Auxiliar", "Interino"])

        etiquetas = ["Legajo:", "Nombre:", "Apellido:", "DNI:", "Email:", "Teléfono:", "Materia:", "Categoría:"]
        widgets = [self.legajo_edit, self.nombre_edit, self.apellido_edit, self.dni_edit,
                   self.email_edit, self.telefono_edit, self.materia_edit, self.categoria_combo]

        for i, (et, w) in enumerate(zip(etiquetas, widgets)):
            form_layout.addWidget(QLabel(et), i, 0)
            form_layout.addWidget(w, i, 1)

        grupo_form.setLayout(form_layout)
        layout.addWidget(grupo_form)

        grupo_botones = QGroupBox("Acciones")
        bl = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_modificar = QPushButton("Modificar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_exportar = QPushButton("Exportar CSV")

        for b in [self.btn_agregar, self.btn_buscar, self.btn_modificar, self.btn_eliminar, self.btn_limpiar, self.btn_exportar]:
            bl.addWidget(b)

        grupo_botones.setLayout(bl)
        layout.addWidget(grupo_botones)

        # Conexiones
        self.btn_agregar.clicked.connect(self.agregar_docente)
        self.btn_buscar.clicked.connect(self.buscar_docente)
        self.btn_modificar.clicked.connect(self.modificar_docente)
        self.btn_eliminar.clicked.connect(self.eliminar_docente)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        self.btn_exportar.clicked.connect(self.exportar_datos)

        layout.addStretch(1)
        return widget

    def crear_panel_lista(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Búsqueda
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(QLabel("Buscar:"))
        self.busqueda_edit = QLineEdit()
        self.busqueda_edit.setPlaceholderText("Apellido, nombre o legajo...")
        self.busqueda_edit.textChanged.connect(self.filtrar_lista)
        busqueda_layout.addWidget(self.busqueda_edit)
        layout.addLayout(busqueda_layout)

        # Lista
        self.lista_docentes = QListWidget()
        self.lista_docentes.itemClicked.connect(self.mostrar_detalles)
        layout.addWidget(self.lista_docentes)

        # Detalles
        grupo_detalles = QGroupBox("Detalles del Docente Seleccionado")
        self.detalles_text = QTextEdit()
        self.detalles_text.setReadOnly(True)
        self.detalles_text.setMaximumHeight(220)
        dl = QVBoxLayout()
        dl.addWidget(self.detalles_text)
        grupo_detalles.setLayout(dl)
        layout.addWidget(grupo_detalles)

        return widget

    # ----------- Persistencia -----------
    def cargar_datos(self):
        self.lista_docentes.clear()
        if not os.path.exists(self.archivo_datos):
            return
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    datos = linea.split(SEPARADOR)
                    if len(datos) == 8:
                        self.agregar_a_lista(datos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos:\n{e}")

    def guardar_datos(self):
        try:
            with open(self.archivo_datos, "w", encoding="utf-8") as f:
                for i in range(self.lista_docentes.count()):
                    item = self.lista_docentes.item(i)
                    datos = item.data(Qt.UserRole)
                    f.write(SEPARADOR.join(datos) + "\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar datos:\n{e}")

    # ----------- Operaciones -----------
    def agregar_a_lista(self, datos):
        texto = f"{datos[2]}, {datos[1]} ({datos[0]})"
        item = QListWidgetItem(texto)
        item.setData(Qt.UserRole, datos)
        self.lista_docentes.addItem(item)

    def campos_a_datos(self):
        return [
            self.legajo_edit.text().strip(),
            self.nombre_edit.text().strip(),
            self.apellido_edit.text().strip(),
            self.dni_edit.text().strip(),
            self.email_edit.text().strip(),
            normalizar_telefono(self.telefono_edit.text()),
            self.materia_edit.text().strip(),
            self.categoria_combo.currentText()
        ]

    def validar_formulario(self) -> bool:
        legajo, nombre, apellido, dni, email, telefono, materia, categoria = self.campos_a_datos()
        obligatorios = {
            "Legajo": legajo,
            "Nombre": nombre,
            "Apellido": apellido,
            "DNI": dni,
            "Email": email,
            "Materia": materia,
        }
        faltantes = [k for k, v in obligatorios.items() if not v]
        if faltantes:
            QMessageBox.warning(self, "Campos obligatorios", f"Complete: {', '.join(faltantes)}")
            return False
        if not validar_email(email):
            QMessageBox.warning(self, "Email inválido", "Ingrese un email válido.")
            return False
        return True

    def buscar_item_por_legajo(self, legajo: str):
        legajo = legajo.strip().lower()
        for i in range(self.lista_docentes.count()):
            it = self.lista_docentes.item(i)
            datos = it.data(Qt.UserRole)
            if datos[0].strip().lower() == legajo:
                return it
        return None

    def agregar_docente(self):
        if not self.validar_formulario():
            return
        legajo = self.legajo_edit.text().strip()
        if self.buscar_item_por_legajo(legajo) is not None:
            QMessageBox.warning(self, "Duplicado", "Ya existe un docente con ese legajo.")
            return
        datos = self.campos_a_datos()
        self.agregar_a_lista(datos)
        self.guardar_datos()
        self.limpiar_formulario()
        QMessageBox.information(self, "Éxito", "Docente agregado correctamente.")

    def buscar_docente(self):
        legajo = self.legajo_edit.text().strip()
        if not legajo:
            QMessageBox.warning(self, "Buscar", "Ingrese un legajo en el campo Legajo.")
            return
        it = self.buscar_item_por_legajo(legajo)
        if it:
            self.lista_docentes.setCurrentItem(it)
            self.mostrar_detalles(it)
        else:
            QMessageBox.information(self, "No encontrado", f"No se encontró docente con legajo: {legajo}")

    def modificar_docente(self):
        item = self.lista_docentes.currentItem()
        if not item:
            QMessageBox.warning(self, "Modificar", "Seleccione un docente de la lista.")
            return
        # Carga en el formulario para editar
        datos = item.data(Qt.UserRole)
        self.legajo_edit.setText(datos[0])
        self.nombre_edit.setText(datos[1])
        self.apellido_edit.setText(datos[2])
        self.dni_edit.setText(datos[3])
        self.email_edit.setText(datos[4])
        self.telefono_edit.setText(datos[5])
        self.materia_edit.setText(datos[6])
        idx = self.categoria_combo.findText(datos[7])
        self.categoria_combo.setCurrentIndex(max(0, idx))

        # Cambia botón Agregar por Actualizar
        self.btn_agregar.setText("Actualizar")
        try:
            self.btn_agregar.clicked.disconnect()
        except Exception:
            pass
        self.btn_agregar.clicked.connect(lambda: self.actualizar_docente(item))

    def actualizar_docente(self, item):
        if not self.validar_formulario():
            return
        datos_nuevos = self.campos_a_datos()

        # Si cambió el legajo, verificar duplicado
        legajo_nuevo = datos_nuevos[0].strip().lower()
        for i in range(self.lista_docentes.count()):
            it = self.lista_docentes.item(i)
            if it is item:
                continue
            legajo_it = it.data(Qt.UserRole)[0].strip().lower()
            if legajo_it == legajo_nuevo:
                QMessageBox.warning(self, "Duplicado", "Otro docente ya usa ese legajo.")
                return

        item.setData(Qt.UserRole, datos_nuevos)
        item.setText(f"{datos_nuevos[2]}, {datos_nuevos[1]} ({datos_nuevos[0]})")
        self.guardar_datos()
        self.limpiar_formulario()
        QMessageBox.information(self, "Actualizado", "Docente actualizado correctamente.")
        # Restaurar botón
        try:
            self.btn_agregar.clicked.disconnect()
        except Exception:
            pass
        self.btn_agregar.setText("Agregar")
        self.btn_agregar.clicked.connect(self.agregar_docente)

    def eliminar_docente(self):
        item = self.lista_docentes.currentItem()
        if not item:
            QMessageBox.warning(self, "Eliminar", "Seleccione un docente de la lista.")
            return
        datos = item.data(Qt.UserRole)
        resp = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Eliminar a {datos[1]} {datos[2]} (Legajo {datos[0]})?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            row = self.lista_docentes.row(item)
            self.lista_docentes.takeItem(row)
            self.guardar_datos()
            self.detalles_text.clear()
            QMessageBox.information(self, "Eliminado", "Docente eliminado.")

    def limpiar_formulario(self):
        self.legajo_edit.clear()
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.dni_edit.clear()
        self.email_edit.clear()
        self.telefono_edit.clear()
        self.materia_edit.clear()
        self.categoria_combo.setCurrentIndex(0)

    # ----------- Lista/Detalles -----------
    def filtrar_lista(self):
        q = self.busqueda_edit.text().lower().strip()
        for i in range(self.lista_docentes.count()):
            item = self.lista_docentes.item(i)
            datos = item.data(Qt.UserRole)
            coincide = (
                q in datos[0].lower() or
                q in datos[1].lower() or
                q in datos[2].lower()
            )
            item.setHidden(not coincide)

    def mostrar_detalles(self, item):
        datos = item.data(Qt.UserRole)
        detalles = (
            "INFORMACIÓN DEL DOCENTE\n"
            "========================\n"
            f"Legajo: {datos[0]}\n"
            f"Nombre: {datos[1]}\n"
            f"Apellido: {datos[2]}\n"
            f"DNI: {datos[3]}\n"
            f"Email: {datos[4]}\n"
            f"Teléfono: {datos[5]}\n"
            f"Materia: {datos[6]}\n"
            f"Categoría: {datos[7]}\n"
        )
        self.detalles_text.setPlainText(detalles)

    # ----------- Extra -----------
    def exportar_datos(self):
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Exportar datos", "docentes_export.csv", "Archivos CSV (*.csv)"
        )
        if not archivo:
            return
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write("legajo,nombre,apellido,dni,email,telefono,materia,categoria\n")
                for i in range(self.lista_docentes.count()):
                    datos = self.lista_docentes.item(i).data(Qt.UserRole)
                    # Escapar comas con comillas
                    fila = ",".join([f'"{c}"' for c in datos])
                    f.write(fila + "\n")
            QMessageBox.information(self, "Exportado", "Datos exportados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SistemaDocentes()
    w.show()
    sys.exit(app.exec_())
