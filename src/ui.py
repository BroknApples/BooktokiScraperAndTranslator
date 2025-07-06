# Imports
import sys
import sys
from PySide6.QtWidgets import (
  QApplication,
  QWidget,
  QPushButton,
  QLabel,
  QVBoxLayout
)



# TODO: FIND A VERSION OF PYTHON OR WAY OF INSTALLING PACKAGES
# THAT ALLOWS YOU TO USE SELENIUM, SELENIUMBASE, GOOGLETRANS,
# AND PYQT6 ALL TOGETHER

class NovelScrapeGuiWindow(QWidget):
  """
  UI implementation for the NovelScrape Python Application

  HOW TO USE:

  app = QApplication(sys.argv)      \n
  window = NovelScrapeGUIWindow()   \n
  window.show()                     \n
  sys.exit(app.exec())              \n
  """

  def __init__(self):
    """
    Initialize all the UI
    """

    # Call the QWidget initialization function
    super().__init__()

    # Set Window Title and Size
    self.setWindowTitle("PyQt5 Example")
    self.resize(600, 500)

    # Create label and button
    self.label = QLabel("Click the button", self)
    self.button = QPushButton("Click Me", self)
    self.button.clicked.connect(self.on_click)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.label)
    self.setLayout(layout)
    layout.addWidget(self.button)

  def on_click(self):
    self.label.setText("Button clicked!")


# TODO: Move this into the novel_scrape.py file
def setupGui():
  # if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = NovelScrapeGuiWindow()
  window.show()
  app.exec()
  # sys.exit(app.exec()) to actually use in the main program