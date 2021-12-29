from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from os import path
from app.state import AppState
from infra.https import HttpsServerStatus
from app.middleware import static_middleware
import sys

# GUI界面初始化函数
def launch():
    state = AppState()
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    btn_cert = QPushButton('choose cert')
    btn_key = QPushButton('choose key')
    btn_root = QPushButton('choose root directory')
    btn_switch = QPushButton('start')
    font=QFont()

    # 设置服务器端的地址
    state.server.bind_addr = ("0.0.0.0", 443)

    # 选择证书按钮绑定的函数，获取证书文件路径
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

    # 选择私钥按钮绑定的函数，获取私钥文件路径
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
    
    # 选择初始化文件夹按钮绑定的函数，获取初始化文件夹路径
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
    
    # 控制服务器状态按钮绑定的函数
    def handle_switch_click():
        if state.server.status == HttpsServerStatus.Stop:

            # 调用HttpsServer类的luanch函数启动https服务
            state.server.launch(static_middleware(state.root_directory))
            btn_switch.setText("stop")
        else:

            # 调用HttpsServer类的shutdown函数关闭https服务
            state.server.shutdown()
            btn_switch.setText("start")
    
    # 按钮绑定对应函数
    btn_cert.clicked.connect(handle_cert_click)
    btn_key.clicked.connect(handle_key_click)
    btn_root.clicked.connect(handle_root_click)
    btn_switch.clicked.connect(handle_switch_click)
    
    # 按钮控件渲染进layout控件
    layout.addWidget(btn_cert)
    layout.addWidget(btn_key)
    layout.addWidget(btn_root)
    layout.addWidget(btn_switch)
    
    # 设置界面字体大小 （因为pyQT5子控件是自适应大小，按钮大小无法设置，通过设置字体改变按钮大小）
    font.setPointSize(18)

    # widget控件显示，并设置基础参数
    window.resize(450,280)
    window.setLayout(layout)
    window.setFont(font)
    window.setWindowTitle("https_server_py")
    window.show()
    sys.exit(app.exec_())
