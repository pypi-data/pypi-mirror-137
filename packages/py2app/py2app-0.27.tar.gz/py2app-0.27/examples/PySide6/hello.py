from PySide6.QtWidgets import QApplication, QLabel

import sys

app = QApplication(sys.argv)
window = QLabel("<h2>Hello, World</h2>")
window.show()  

app.exec()
