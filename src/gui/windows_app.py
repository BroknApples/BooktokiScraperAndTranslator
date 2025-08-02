# Imports
import sys
import configparser
from PySide6.QtCore import (
  Qt,
  QSize,
)
from PySide6.QtWidgets import (
  QMainWindow,
  QWidget,
  QToolBar,
  QGridLayout,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QPushButton,
  QSpacerItem,
  QSizePolicy,
)
from PySide6.QtGui import (
  QAction,
  QIcon,
)
from src.common.utils import Limits
from src.common.scraper import Scraper
from src.common.translator import TextTranslator


# === Class: NovelScrapeGuiWindow ===
class NovelScrapeGuiWindow(QMainWindow):
  """
  UI implementation for the NovelScrape Python Application

  HOW TO USE:

  app = QApplication(sys.argv)      \n
  window = NovelScrapeGUIWindow()   \n
  window.show()                     \n
  sys.exit(app.exec())              \n
  """


  # === Subclass: ConfigData ===
  class ConfigData():
    """
    Defines variables which correspond to a section/variable in the config.ini file
    """
    
    # === Constants ===
    WINDOW_SETTINGS_SECTION: str = "WindowSettings"
    WINDOW_NAME: str = "window_name"
    WINDOW_ICON_PATH: str = "window_icon_path"
    WINDOW_WIDTH: str = "window_width"
    WINDOW_HEIGHT: str = "window_height"
    MINIMUM_WINDOW_WIDTH: str = "minimum_window_width"
    MINIMUM_WINDOW_HEIGHT: str = "minimum_window_height"

    SCRAPER_SETTINGS_SECTION: str = "ScraperSettings"
    DEFAULT_SCRAPER_SETTINGS: str = "default_scraper_settings"

    TRANSLATOR_SETTINGS_SECTION: str = "TranslatorSettings"
    DEFAULT_SRC_LANGUAGE: str = "default_src_language"
    DEFAULT_DEST_LANGUAGE: str = "default_dest_language"


  # ******************************************** #
  # ****************** Private ***************** #
  # ******************************************** #
  

  # === Variables ===
  _config: configparser.ConfigParser
  _scraper: Scraper
  _translator: TextTranslator

  """ Variables for the scraper/translator settings """
  _thread_count: int = 1
  _start_idx: int = 0
  _end_idx: int = Limits.INT_MAX
  _src_lang: TextTranslator.Languages = TextTranslator.Languages.AUTO_DETECT
  _dest_lang: TextTranslator.Languages = TextTranslator.Languages.ENGLISH
  _novel_name: str = ""
  _format_text: bool = True

  """ Scraper Settings Params """
  _chapter_list_body_by: str = ""
  _chapter_list_body_element: str = ""
  _chapter_list_item_by: str = ""
  _chapter_list_item_element: str = ""
  _next_chapter_button_by: str = ""
  _next_chapter_button_element: str = ""
  _chapter_text_body_by: str = ""
  _chapter_text_body_element: str = ""

  # === Function: _setupToolbar ===
  def _setupToolbar(self) -> None:
    """
    Setup the side toolbar used for utilities
    """

    # Create and add toolbar to widget
    left_toolbar = QToolBar("Left Toolbar")
    self.addToolBar(Qt.LeftToolBarArea, left_toolbar)

    # Setup toolbar settings
    left_toolbar.setOrientation(Qt.Vertical)
    left_toolbar.setMovable(False)
    left_toolbar.setAllowedAreas(Qt.ToolBarArea.LeftToolBarArea)
    left_toolbar.setMinimumWidth(self.width() // 10)

    # Setup toolbar widgets
    left_toolbar.addAction(QAction("Option 1", self))
    left_toolbar.addAction(QAction("Option 2", self))


  # === Function: _setupCentralWidget ===
  def _setupCentralWidget(self) -> None:
    """
    Setup the central widget that contains all the boxes for scraping/translating
    """

    # Create widgets
    central_widget = QWidget()
    vbox_layout = QVBoxLayout(central_widget)

    grid_widget = QWidget()
    grid_layout = QGridLayout(grid_widget)

    hbox_widget = QWidget()
    hbox_layout = QHBoxLayout(hbox_widget)

    # Add widgets to the vbox layout
    vbox_layout.addWidget(grid_widget)
    vbox_layout.addWidget(hbox_widget, alignment=Qt.AlignmentFlag.AlignBottom)

    # Constants for readability
    ROW_ONE: int = 0
    ROW_TWO: int = 1
    ROW_THREE: int = 2
    ROW_FOUR: int = 3

    COLUMN_ONE: int = 0
    COLOMN_TWO: int = 1
    COLUMN_THREE: int = 2
    COLUMN_FOUR: int = 3

    # Add widgets to grid (row, column)
    grid_layout.addWidget(QPushButton("Button 1"),  ROW_ONE,       COLUMN_ONE)
    grid_layout.addWidget(QPushButton("Button 2"),  COLUMN_ONE,    COLOMN_TWO)
    grid_layout.addWidget(QPushButton("Button 3"),  ROW_TWO,       COLUMN_ONE)
    grid_layout.addWidget(QPushButton("Button 4"),  ROW_TWO,       COLOMN_TWO)

    # Setup start panel
    hbox_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    # Create start panel widgets
    start_button = QPushButton("Start")
    novel_name_label = QLabel("Novel Name: ")
    novel_name_line_edit = QLineEdit(self._novel_name)

    # Add wigets to the start panel
    hbox_layout.addWidget(novel_name_label, alignment=Qt.AlignmentFlag.AlignLeft)
    hbox_layout.addWidget(novel_name_line_edit, stretch=3)
    hbox_layout.addSpacerItem(QSpacerItem(self.width() // 3, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
    hbox_layout.addWidget(start_button, stretch=2)

    self.setCentralWidget(central_widget)


  # ******************************************** #
  # ****************** Public ****************** #
  # ******************************************** #

  # === Function: __init__ ===
  def __init__(self, config: configparser.ConfigParser) -> None:
    """
    Initialize all the UI widgets
    """

    # Call the QWidget initialization function
    super().__init__()

    # Set config object
    self._config = config

    # Create scraper and translator
    self._scraper = Scraper()
    self._translator = TextTranslator()

    # Set window title, size, and icon
    WS_SECTION: str = self.ConfigData.WINDOW_SETTINGS_SECTION
    WINDOW_NAME: str = self._config.get(WS_SECTION, self.ConfigData.WINDOW_NAME).strip('"')
    WINDOW_WIDTH: int = self._config.getint(WS_SECTION, self.ConfigData.WINDOW_WIDTH)
    WINDOW_HEIGHT: int = self._config.getint(WS_SECTION, self.ConfigData.WINDOW_HEIGHT)
    MIN_WINDOW_WIDTH: int = self._config.getint(WS_SECTION, self.ConfigData.MINIMUM_WINDOW_WIDTH)
    MIN_WINDOW_HEIGHT: int = self._config.getint(WS_SECTION, self.ConfigData.MINIMUM_WINDOW_HEIGHT)

    self.setWindowTitle(WINDOW_NAME)
    self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
    self.setWindowIcon(QIcon(self._config.get(WS_SECTION, self.ConfigData.WINDOW_ICON_PATH).strip('"')))

    # Setup widgets
    self._setupToolbar()
    self._setupCentralWidget()

  # ******************************************** #
  # ************** Signal Functions ************ #
  # ******************************************** #

  def _on_start_pressed(self) -> None:
    """
    Called when the start button is called
    """
    self._scraper.scrape(self._start_idx, self._end_idx, self._format_text)





# TODO: IDEAS
# 
# Have terminal log the whole scraping process in the ui. It will be accessed through the left sidebar and will automatically be switched to when scraping starts
# terminal will have a left + right side, one for scrape other for translate.
#
# Translating happens at the same time as scraping through some sort of 'await signal' type thing
# If an error occurs to either scraping/translating, the terminal will print a red message and turn the tab header red with an X
# If the scraping/translationg finishes the tab header will turn green with a checkmark
# 