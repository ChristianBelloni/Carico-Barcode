from PyQt5 import QtCore, QtGui, QtWidgets


class StandardDialog(QtWidgets.QMessageBox):
    def __init__(self):
        super().__init__()


class Ui_MainWindow(QtWidgets.QMainWindow):
    # custom signals
    ui_done = QtCore.pyqtSignal()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ver_lay_list_ordini = QtWidgets.QVBoxLayout()
        self.ver_lay_list_ordini.setObjectName("ver_lay_list_ordini")
        self.ordini_label = QtWidgets.QLabel(self.centralwidget)
        self.ordini_label.setObjectName("ordini_label")
        self.ver_lay_list_ordini.addWidget(self.ordini_label)
        self.list_ordini = QtWidgets.QListWidget(self.centralwidget)
        self.list_ordini.setObjectName("list_ordini")
        self.list_ordini.setMaximumSize(200, 16777215)
        self.ver_lay_list_ordini.addWidget(self.list_ordini)
        self.horizontalLayout_2.addLayout(self.ver_lay_list_ordini)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.ver_lay_list_articoli = QtWidgets.QVBoxLayout()
        self.ver_lay_list_articoli.setObjectName("ver_lay_list_articoli")

        self.articoli_table = QtWidgets.QTableWidget(self.centralwidget)
        self.articoli_table.setObjectName("articoli_table")
        self.articoli_table.setColumnCount(3)
        self.articoli_table.setHorizontalHeaderLabels(
            ['codice ean', 'descrizione', 'N.'])

        self.articoli_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.articoli_table.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)

        self.articoli_table.setFocusPolicy(QtCore.Qt.NoFocus)
        palette = self.articoli_table.palette()
        palette.setBrush(QtGui.QPalette.Highlight,
                         palette.brush(QtGui.QPalette.Base))
        palette.setBrush(QtGui.QPalette.HighlightedText,
                         palette.brush(QtGui.QPalette.Text))
        self.articoli_table.setPalette(palette)
        self.articoli_table.setColumnWidth(0, 200)
        self.articoli_table.setColumnWidth(2, 60)
        self.articoli_table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.articoli_table.verticalHeader().hide()

        self.ver_lay_list_articoli.addWidget(self.articoli_table)
        self.btn_scarico_layout = QtWidgets.QHBoxLayout()

        self.btn_scarico_layout.setObjectName("btn_scarico_layout")

        self.start_scarico_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_scarico_btn.setObjectName("start_scarico_btn")

        self.btn_scarico_layout.addWidget(self.start_scarico_btn)

        self.annulla_scarico_btn = QtWidgets.QPushButton(self.centralwidget)
        self.annulla_scarico_btn.setEnabled(False)
        self.annulla_scarico_btn.setObjectName("annulla_scarico_btn")

        self.btn_scarico_layout.addWidget(self.annulla_scarico_btn)

        self.ver_lay_list_articoli.addLayout(self.btn_scarico_layout)

        self.horizontalLayout_2.addLayout(self.ver_lay_list_articoli)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1189, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.show()
        self.MainWindow = MainWindow
        self.ui_done.emit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ordini_label.setText(_translate("MainWindow", "Ordini"))
        self.start_scarico_btn.setText(
            _translate("MainWindow", "Inizia Scarico"))
        self.annulla_scarico_btn.setText(
            _translate("MainWindow", "Annulla Scarico"))

        print("Finished translation")

    def makeErrorDialog(self, title="", text="", confirm_txt="", cancel_txt=""):
        dialog = StandardDialog()
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setIcon(QtWidgets.QMessageBox.Critical)

        retval = dialog.exec()

    def makeInfoDialog(self, title="", text="", confirm_txt="", cancel_txt=""):
        dialog = StandardDialog()
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setIcon(QtWidgets.QMessageBox.Information)

        retval = dialog.exec()
