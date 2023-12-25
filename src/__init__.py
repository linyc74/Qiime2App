import sys
from PyQt5.QtWidgets import QApplication
from .view import View
from .io import IO
from .controller import Controller


__VERSION__ = '1.0.0-beta'


class EntryPoint:

    APP_ID = f'NYCU.Dentistry.Qiime2App.{__VERSION__}'

    model: IO
    view: View
    controller: Controller

    def main(self):
        self.config_taskbar_icon()

        app = QApplication(sys.argv)

        self.model = IO()
        self.view = View(model=self.model)
        self.controller = Controller(io=self.model, view=self.view)

        sys.exit(app.exec_())

    def config_taskbar_icon(self):
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.APP_ID)
        except ImportError as e:
            print(e, flush=True)
