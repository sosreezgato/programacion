# -*- coding: utf-8 -*-
"""
Editor de Texto (PyQt5)
-----------------------
- Menús: Archivo, Editar, Ayuda
- Acciones: Nuevo, Abrir, Guardar, Guardar como, Salir
- Edición: Cortar, Copiar, Pegar
- Barra de estado y atajos
- Manejo de archivo actual + detección de cambios
"""
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog,
    QMessageBox, QStatusBar
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class EditorTexto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Texto")
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Escribe aquí tu texto...")
        self.setCentralWidget(self.editor)

        self.ruta_actual = None
        self.editor.textChanged.connect(self._marcar_modificado)

        self.crear_menus()
        self.crear_barra_estado()
        self.statusBar().showMessage("Listo")

    # -------- Menús --------
    def crear_menus(self):
        menubar = self.menuBar()

        # Archivo
        menu_archivo = menubar.addMenu("&Archivo")

        act_nuevo = QAction("&Nuevo", self)
        act_nuevo.setShortcut(QKeySequence.New)
        act_nuevo.triggered.connect(self.nuevo_archivo)

        act_abrir = QAction("&Abrir...", self)
        act_abrir.setShortcut(QKeySequence.Open)
        act_abrir.triggered.connect(self.abrir_archivo)

        act_guardar = QAction("&Guardar", self)
        act_guardar.setShortcut(QKeySequence.Save)
        act_guardar.triggered.connect(self.guardar_archivo)

        act_guardar_como = QAction("Guardar &como...", self)
        act_guardar_como.setShortcut(QKeySequence("Ctrl+Shift+S"))
        act_guardar_como.triggered.connect(self.guardar_como)

        act_salir = QAction("&Salir", self)
        act_salir.setShortcut(QKeySequence.Quit)
        act_salir.triggered.connect(self.salir)

        for a in (act_nuevo, act_abrir, act_guardar, act_guardar_como, act_salir):
            menu_archivo.addAction(a)

        # Editar
        menu_editar = menubar.addMenu("&Editar")

        act_cortar = QAction("Cor&tar", self)
        act_cortar.setShortcut(QKeySequence.Cut)
        act_cortar.triggered.connect(self.editor.cut)

        act_copiar = QAction("&Copiar", self)
        act_copiar.setShortcut(QKeySequence.Copy)
        act_copiar.triggered.connect(self.editor.copy)

        act_pegar = QAction("&Pegar", self)
        act_pegar.setShortcut(QKeySequence.Paste)
        act_pegar.triggered.connect(self.editor.paste)

        for a in (act_cortar, act_copiar, act_pegar):
            menu_editar.addAction(a)

        # Ayuda
        menu_ayuda = menubar.addMenu("&Ayuda")
        act_acerca = QAction("&Acerca de", self)
        act_acerca.triggered.connect(self.acerca_de)
        menu_ayuda.addAction(act_acerca)

    # -------- Barra de estado --------
    def crear_barra_estado(self):
        self.setStatusBar(QStatusBar(self))

    # -------- Lógica archivos --------
    def _marcar_modificado(self):
        self.setWindowModified(True)

    def _puede_descartar_cambios(self):
        if not self.isWindowModified():
            return True
        resp = QMessageBox.question(
            self, "Cambios sin guardar",
            "Hay cambios sin guardar. ¿Desea guardarlos?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if resp == QMessageBox.Cancel:
            return False
        if resp == QMessageBox.Yes:
            return self.guardar_archivo()
        return True

    def nuevo_archivo(self):
        if not self._puede_descartar_cambios():
            return
        self.editor.clear()
        self.ruta_actual = None
        self.setWindowModified(False)
        self._actualizar_titulo()
        self.statusBar().showMessage("Nuevo documento")

    def abrir_archivo(self):
        if not self._puede_descartar_cambios():
            return
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos de texto (*.txt);;Todos (*.*)")
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.ruta_actual = ruta
            self.setWindowModified(False)
            self._actualizar_titulo()
            self.statusBar().showMessage(f"Abierto: {os.path.basename(ruta)}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar_archivo(self):
        if self.ruta_actual is None:
            return self.guardar_como()
        try:
            with open(self.ruta_actual, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.setWindowModified(False)
            self._actualizar_titulo()
            self.statusBar().showMessage(f"Guardado: {os.path.basename(self.ruta_actual)}")
            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el archivo:\n{e}")
            return False

    def guardar_como(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar como", "documento.txt", "Archivos de texto (*.txt)")
        if not ruta:
            return False
        self.ruta_actual = ruta
        return self.guardar_archivo()

    def acerca_de(self):
        QMessageBox.information(
            self, "Acerca de",
            "Editor de Texto v1.0\n\nCreado con PyQt5.\nIdeal para practicar menús, diálogos y archivos."
        )

    def salir(self):
        if not self._puede_descartar_cambios():
            return
        self.close()

    def closeEvent(self, event):
        if self._puede_descartar_cambios():
            event.accept()
        else:
            event.ignore()

    def _actualizar_titulo(self):
        nombre = self.ruta_actual if self.ruta_actual else "Sin título"
        base = os.path.basename(nombre)
        self.setWindowTitle(f"{base} - Editor de Texto")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = EditorTexto()
    editor.show()
    sys.exit(app.exec_())
