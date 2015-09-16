# -*- coding: utf-8 -*-
import ctypes
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from win32api import GetEnvironmentVariable, SetEnvironmentVariable
from _winreg import *
import subprocess
import time
import res

APP_ID = 'devart.imagecompressor.py-pyqt4.v2.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.action_combo = QComboBox()
        self.browser = QTextBrowser()
        self.accept_btn = QPushButton('Aceptar')
        self.value_var_edit = QLineEdit()
        self.env_var_see_edit = QLineEdit()
        self.select_dir_btn = QPushButton('...')
        self.name_var_edit = QLineEdit()

        self.connect(self.action_combo, SIGNAL('currentIndexChanged(int)'), self.update_ui)
        self.connect(self.action_combo, SIGNAL('currentIndexChanged(int)'), self.get_env_var_values)
        # self.connect(self.path_edit, SIGNAL('clicked()'), self.selectAll)
        self.connect(self.select_dir_btn, SIGNAL('clicked()'), self.selectDir)
        self.accept_btn.clicked.connect(self.change_env_var)
        # self.connect(self.accept_btn, SIGNAL('clicked()'), self.changeEnvVar)
        self.set_ui()

    def set_ui(self):
        self.setWindowIcon(QIcon(':/icon'))
        self.setWindowTitle('Variables de entorno.')
        self.browser.setWindowIcon(QIcon(':/icon'))
        self.resize(400, 600)
        # self.browser.setVisible(False)

        self.setStyleSheet(self.qss())
        self.browser.setStyleSheet("border:0; font:12px; color: darkslategrey;")

        self.accept_btn.setObjectName("accept_btn")
        self.select_dir_btn.setObjectName("select_dir_btn")
        self.browser.setObjectName("browser")

        self.action_combo.addItems([u"Añadir al path", u"Añadir variable de entorno"])
        self.name_var_edit.setPlaceholderText('Nombre de la variable.')
        # self.path_edit.setPlaceholderText('Escriba el path a adicionar...')
        self.name_var_edit.setVisible(False)

        self.action_combo.setMinimumWidth(400)
        self.select_dir_btn.setMaximumWidth(20)
        self.select_dir_btn.setMaximumHeight(20)
        # self.browser.resize(400, 600)

        grid = QGridLayout()
        grid.addWidget(self.action_combo, 0, 0, 1, 2)
        grid.addWidget(self.name_var_edit, 1, 0)
        grid.addWidget(self.value_var_edit, 2, 0)
        grid.addWidget(self.select_dir_btn, 2, 1)
        grid.addWidget(self.browser, 3, 0)
        grid.addWidget(self.accept_btn, 4, 0)
        self.setLayout(grid)

    def get_env_var_values(self):
        self.browser.clear()
        if self.action_combo.currentIndex() == 0:
            title = "Path de windows"
            values = GetEnvironmentVariable("path").replace(";", "\n")
        else:
            title = "Variables de Entorno establecidas"
            values = "".join(os.popen("set").readlines())
        self.browser.append("<h2 style='color: grey'>%s</h2>" % title)
        self.browser.append(values)
        self.browser.show()

    @staticmethod
    def qss():
        return """
            QLineEdit, QPushButton, QComboBox{
                padding: 3px;
                font: 14px;
                height: 40px;
                color: darkslategrey;
            }
            QComboBox, QLineEdit{
                border: 1px solid silver;
                padding-left: 10px;
            }
            QComboBox:hover, QLineEdit:hover{
                border: 1px solid grey;
            }
            QComboBox::drop-down {
                border: 0;
                width: 25px;
            }
            QComboBox::down-arrow {
                border: 0;
                color: grey;
                background-color: grey;
                border-radius: 6px;
            }
            QComboBox::down-arrow:hover{
                background-color: cornflowerblue;
            }
            QComboBox QAbstractItemView {
                border: 1px solid grey;
                selection-background-color: cornflowerblue;
                selection-color: white;
                color: darkslategrey;
                background-color: white;
                border-top: 5px;
                padding: 5px;
                font-size: 14px;
            }
            #select_dir_btn{
                border: 0;
                color: darkslategrey;
                font: 17px;
            }
            #select_dir_btn:hover{
                color: cornflowerblue;
            }
            #accept_btn{
                border: 0;
                border-radius: 4px;
                background-color: grey;
                color: white;
            }
            #accept_btn:hover{
                background-color: cornflowerblue;
            }
            #see_btn:hover{
                color: cornflowerblue;
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel{
                color: darkslategrey;
                font: 14px;
            }
            QMessageBox QPushButton{
                border: 0;
                font: 16px;
            }
            QMessageBox QPushButton:hover{
                color: cornflowerblue;
            }
            QScrollBar {
                border: 0px solid grey;
                width: 7px;
            }
            QScrollBar::handle {
                background: gainsboro;
                border-radius: 3px;
            }
            QScrollBar::handle:hover{
                background: cornflowerblue;
            }
        """

    def update_ui(self):
        visible = False if self.action_combo.currentIndex() == 0 else True
        self.name_var_edit.setVisible(visible)
        placeholder = "Escriba el path a adicionar..." if not visible else "Escriba el valor de la variable..."
        self.value_var_edit.setPlaceholderText(placeholder)

    def selectDir(self):
        directory = unicode(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print 'd', directory
        directory = directory.replace('/', '\\')
        print directory
        if directory is not None:
            self.value_var_edit.setText(directory)

    def validate(self):
        is_empty = False
        if self.action_combo.currentIndex() == 0:
            if unicode(self.value_var_edit.text()).strip() == "":
                is_empty = True
        else:
            if unicode(self.name_var_edit.text()).strip() == "" or unicode(self.value_var_edit.text()).strip() == "":
                is_empty = True
        if is_empty:
            QMessageBox.warning(self, u'Atención', 'Llene los datos, por favor.')
        return not is_empty

    def change_env_var(self):
        if not self.validate(): return
        if self.action_combo.currentIndex() == 0:  # cambiar el path
            value = "Path"
            data = GetEnvironmentVariable(value)
            semi_colon = True if data[-1] == ';' else False
            if semi_colon:
                data += '%s;' % unicode(self.value_var_edit.text())
            else:
                data += ';%s;' % unicode(self.value_var_edit.text())
        else:
            value = unicode(self.name_var_edit.text())
            data = unicode(self.value_var_edit.text())
        self.regedit(value, data)

    def regedit(self, value, data):
        sub_key = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
        hklm = HKEY_LOCAL_MACHINE
        try:
            key = OpenKey(hklm, sub_key, 0, KEY_ALL_ACCESS)
            SetValueEx(key, value, 0, REG_EXPAND_SZ, data)
            if self.warning_message():
                os.system('shutdown /l')
        except WindowsError:
            QMessageBox.critical(self, 'Error', 'Acceso denegado. Eleve sus permisos.')
        finally:
            sys.exit()

    def warning_message(self):
        msgBox = QMessageBox(QMessageBox.Information,
                             u'Éxito',
                             u"Se ha establecido correctamente el valor de la variable.\nDebe cerrar la sesión para que los cambios surtan efecto.",
                             QMessageBox.NoButton, self)
        msgBox.addButton(u"Cerrar sesión ahora", QMessageBox.AcceptRole)
        msgBox.addButton(u"Salir sin cerrar sesión", QMessageBox.RejectRole)
        return True if msgBox.exec_() == QMessageBox.AcceptRole else False


app = QApplication(sys.argv)
form = Main()
form.show()
app.exec_()
