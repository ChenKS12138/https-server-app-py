
from PyQt5.QtWidgets import *
from os import path
from app.state import AppState
from infra.https import HttpsServerStatus
from app.middleware import static_middleware


def launch():
    state = AppState()
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    btn_cert = QPushButton('choose cert')
    btn_key = QPushButton('choose key')
    btn_root = QPushButton('choose root directory')
    btn_switch = QPushButton('start')

    state.server.bind_addr = ("0.0.0.0", 443)

    def handle_cert_click():
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) == 0:
                return
            filename = filenames[0]
            btn_cert.setText(path.basename(filename))
            state.server.cert = filename

    def handle_key_click():
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) == 0:
                return
            filename = filenames[0]
            btn_key.setText(path.basename(filename))
            state.server.key = filename

    def handle_root_click():
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if len(dirs) == 0:
                return
            dir = dirs[0]
            btn_root.setText(path.basename(dir))
            state.root_directory = dir

    def handle_switch_click():
        if state.server.status == HttpsServerStatus.Stop:
            state.server.launch(static_middleware(state.root_directory))
            btn_switch.setText("stop")
        else:
            state.server.shutdown()
            btn_switch.setText("start")

    btn_cert.clicked.connect(handle_cert_click)
    btn_key.clicked.connect(handle_key_click)
    btn_root.clicked.connect(handle_root_click)
    btn_switch.clicked.connect(handle_switch_click)

    layout.addWidget(btn_cert)
    layout.addWidget(btn_key)
    layout.addWidget(btn_root)
    layout.addWidget(btn_switch)

    window.setLayout(layout)
    window.show()
    app.exec_()
