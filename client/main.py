from gui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QTableWidgetItem, QAbstractItemView, QDialog
from WaitingSpinner import QtWaitingSpinner
from database import get_orders, DatabaseThread
from database import get_articoli
from PyQt5.QtCore import pyqtSlot
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import Qt
from scanner import ScannerThread, ConnectionThread
from qt_material import apply_stylesheet


app = QApplication([''])


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.list_ordini.itemSelectionChanged.connect(
            self.on_list_ordini_selectionChange)

        self.ui.start_scarico_btn.clicked.connect(self.start_scarico)
        self.ui.annulla_scarico_btn.clicked.connect(self.annulla_scarico)
        self.on_start_routine()

    def on_start_routine(self):
        self.start_reset_ordini_thread()
        self.start_connection_thread()

    @pyqtSlot()
    def ui_done(self):
        print("Done")

    @pyqtSlot()
    def on_list_ordini_selectionChange(self):
        # self.ui.list_articoli.clear()
        # self.ui.list_n.clear()
        ordine = self.ui.list_ordini.currentItem().data(QtCore.Qt.UserRole)
        articoli = get_articoli(ordine.id)
        self.ui.articoli_table.setRowCount(len(articoli))

        for y, i in enumerate(articoli):
            row = [i.codice_ean, i.descrizione, i.n]
            for x, data in enumerate(row):
                self.ui.articoli_table.setItem(
                    y, x, QTableWidgetItem(str(data)))
        self.ui.articoli_table.sortItems(0, QtCore.Qt.AscendingOrder)

    @pyqtSlot()
    def start_scarico(self):
        print(self.connection_thread.get_connections())
        if not self.connection_thread.get_connections():
            self.ui.makeErrorDialog(
                title="Errore", text="Collegare uno scanner per iniziare lo scarico")
            return
        if not self.ui.list_ordini.currentItem():
            self.ui.makeErrorDialog(
                title="Errore", text="Selezionare un ordine per iniziare lo scarico")
            return
        print("Scarico iniziato")
        self.connection_thread.progressChanged.connect(self.scanner_dispatch)
        self.ui.list_ordini.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.annulla_scarico_btn.setEnabled(True)
        self.ui.start_scarico_btn.setEnabled(False)

    def annulla_scarico(self):
        print("Scarico annullato")
        self.ui.annulla_scarico_btn.setEnabled(False)
        self.ui.start_scarico_btn.setEnabled(True)
        self.ui.list_ordini.setSelectionMode(QAbstractItemView.SingleSelection)
        self.connection_thread.progressChanged.disconnect()
        self.ui.articoli_table.setEnabled(True)

    def start_connection_thread(self):
        self.connection_thread = ConnectionThread()
        self.connection_thread.start()

    def scanner_dispatch(self, sock_recv):
        if sock_recv.startswith("scan"):
            codice = sock_recv.split("scan")[1][1:]
            self.scanner_found_codice(codice)
        if sock_recv.startswith("disconnection"):
            if self.ui.annulla_scarico_btn.isEnabled():
                self.ui.makeErrorDialog(
                    title="Errore", text="Ricollegare uno scanner per iniziare lo scarico")
                self.ui.articoli_table.setEnabled(False)
        if sock_recv.startswith("conn"):
            addr = sock_recv.split("conn")[1][1:]
            self.ui.articoli_table.setEnabled(True)
            self.ui.makeInfoDialog(
                title="Connessione Scanner", text="Scanner Collegato!")

    def scanner_found_codice(self, codice):
        rows = self.ui.articoli_table.rowCount()
        for y in range(rows):
            items = [self.ui.articoli_table.item(
                y, x).text() for x in range(3)]
            if int(codice) == int(items[0]):
                new_n = int(items[2]) - 1
                if new_n < 0:
                    return
                self.ui.articoli_table.setItem(
                    y, 2, QTableWidgetItem(str(new_n)))

    def start_reset_ordini_thread(self):
        self.db_thread = DatabaseThread()
        self.start_spinner()
        self.db_thread.progressEnded.connect(self.ordini_thread_ended)
        self.db_thread.start()

    def ordini_thread_ended(self, orders):
        self.ui.list_ordini.clear()
        items = []
        for i in orders:
            item = QListWidgetItem()
            item.setText(i.codice_ordine)
            item.setData(QtCore.Qt.UserRole, i)
            self.ui.list_ordini.addItem(item)
        self.ui.spinner.stop()

    def start_spinner(self):
        self.ui.spinner = QtWaitingSpinner(self.ui.centralwidget)
        self.ui.spinner.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.ui.spinner.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui.spinner.setInnerRadius(15)
        self.ui.spinner.start()


window = window()
apply_stylesheet(app, theme="dark_blue.xml", invert_secondary=False)
stylesheet = app.styleSheet()
with open('media/css/style.css') as file:
    app.setStyleSheet(stylesheet + file.read())
window.ui.list_ordini.setCurrentRow(
    0)
app.exec_()
