import sys

from PyQt6.QtWidgets import QApplication

from fraud.view import View
from fraud.controller import Controller
from fraud.models import Model

def main(args = None):

    app = QApplication(sys.argv)
    view = View()
    view.show()
    model = Model()
    controller = Controller(view, model)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
    
    