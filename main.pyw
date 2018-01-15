import random
import sys
import os.path
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QSystemTrayIcon, QStyle, QAction, QMenu
from gui import Ui_MainWindow
from parser_myzuka import *
from db import *
import time

# PATH = "C:\\Users\\Public\Downloads\\"
LINK = 'http://myzuka.club/Song/'


class NThread(QThread):
    signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def __init__(self, count, path):
        QThread.__init__(self)
        self.count = count
        self.path = path

    def run(self):
        db = Db()
        empty_page = 0
        j = 0
        last = db.select_last_id()
        s = set_session()
        progress = 0
        c = 100 / self.count
        i = 1
        k = 1

        while i <= self.count:
            page = last + k
            conn = set_connection(LINK, page, s)
            if type(conn[1]) != type(1):
                sp = spyder(conn, db, page)
                if sp:
                    try:
                        start = time.time()
                        download_file(s, sp, self.path)
                        end = time.time()
                        print(end - start)
                        i += 1
                        k += 1
                        self.sleep(random.randint(1,6))
                    except Exception:
                        k += 1
                    progress += c
                    self.signal.emit(progress)
                    self.log_signal.emit(sp[1])
                else:
                    k += 1
                    db.insert_empty_page(page, conn[0], 1)

            else:
                k += 1
                db.insert_empty_page(page, conn[0], 0)
                if j == i - 1:
                    j = i
                    empty_page += 1
                else:
                    j = 0
                    empty_page = 0
                if empty_page == 100:
                    break
            print('{} - {} - count {}'.format(page, i, self.count))
        s.close()
        self.sleep(5)
        print('Finish THREAD!!!!!!!!!!!!!!!!!!!')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Db()

        # добавляет иконку приложения в системный трей
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        # show_action = QAction("Show", self)
        # hide_action = QAction("Hide", self)
        # show_action.triggered.connect(self.show)
        # hide_action.triggered.connect(self.hide)
        # tray_menu = QMenu()
        # tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        # self.tray_icon.setContextMenu(tray_menu)
        # self.tray_icon.show()

        self.ui.btn_start.clicked.connect(self.start_app)
        self.ui.btn_exit.clicked.connect(self.close_app)
        self.ui.open_direct.clicked.connect(self.set_folder)

    def start_app(self):
        self.ui.log_out.clear()
        self.ui.progressBar.reset()
        self.ui.btn_start.setDisabled(True)
        try:
            path = os.path.normpath(self.path)
            self.db.update_path(path)
        except Exception:
            temp = self.db.get_path()
            if os.path.isdir(temp):
                path = os.path.normpath(temp)
            else:
                path = os.path.normpath(os.getcwd() + '\\songs')
                self.db.update_path(path)

        count = int(self.ui.text_input.text())
        self.helpthread = NThread(count, path)
        self.helpthread.start()
        self.helpthread.signal.connect(self.ui.progressBar.setValue)
        self.helpthread.log_signal.connect(self.ui.log_out.append)
        self.helpthread.finished.connect(self.close_thread)
        print('Work!!!')

    def close_thread(self):
        print('CLOSE THREAD!!!')
        self.ui.log_out.append('------------------Сделано!!!-------------------')
        self.ui.btn_start.setDisabled(False)

    def close_app(self):
        self.close()

    def set_folder (self):
        self.path = QFileDialog.getExistingDirectory(self, directory=self.db.get_path())



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())