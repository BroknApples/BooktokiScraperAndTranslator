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
  QComboBox,
  QCheckBox,
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
  _chapter_list_body_by: any = None
  _chapter_list_body_element: str = ""
  _chapter_list_item_by: any = None
  _chapter_list_item_element: str = ""
  _next_chapter_button_by: any = None
  _next_chapter_button_element: str = ""
  _chapter_text_body_by: any = None
  _chapter_text_body_element: str = ""

  """ Widgets """
  # ROW ONE | COL ONE
  _chapter_list_body_by_combo_box_widget: QComboBox
  _chapter_list_body_element_line_edit_widget: QLineEdit

  # ROW ONE | COL TWO
  _chapter_list_item_by_combo_box_widget: QComboBox
  _chapter_list_item_element_line_edit_widget: QLineEdit

  # ROW TWO | COL ONE
  _next_chapter_button_by_combo_box_widget: QComboBox
  _next_chapter_button_element_line_edit_widget: QLineEdit

  # ROW TWO | COL TWO
  _chapter_text_body_by_combo_box_widget: QComboBox
  _chapter_text_body_element_line_edit_widget: QLineEdit
  
  # ROW THREE | COL ONE
  _start_idx_line_edit_widget: QLineEdit
  _end_idx_line_edit_widget: QLineEdit

  # ROW THREE | COL ONE
  _src_lang_combo_box_widget: QComboBox
  _dest_lang_combo_box_widget: QComboBox

  # ROW FOUR | COL ONE
  _format_text_check_box_widget: QCheckBox
  # TODO: Add more lil settings here.

  # ROW FOUR | COL TWO
  _thread_count_combo_box_widget: QComboBox

  # START BUTTON AREA -- WIDGETS
  _novel_name_line_edit_widget: QLineEdit


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


  # === Function: _createQHBoxWidget ===
  def _createQHBoxWidget(self, widgets: list) -> QWidget:
    """
    Given a list of widgets, create an HBox widget filled in the order they appear

    Params:
      widgets: list of widgets to add to a new QHboxWidget

    Returns:
      QWidget: A widget with an HBoxLayout filled with the widgets from the 'widgets' param
    """

    # Setup widget
    hbox_widget = QWidget()
    hbox_layout = QHBoxLayout(hbox_widget)

    # Add child widgets
    for widget in widgets:
      hbox_layout.addWidget(widget)

    return hbox_widget


  # === Function: _setupCentralWidget ===
  def _setupCentralWidget(self) -> None:
    """
    Setup the central widget that contains all the boxes for scraping/translating
    """

    #################################
    ### Constants for readability ###
    #################################

    ROW_ONE: int = 0
    ROW_TWO: int = 1
    ROW_THREE: int = 2
    ROW_FOUR: int = 3
    ROW_FIVE: int = 4

    COLUMN_ONE: int = 0
    COLUMN_TWO: int = 1
    COLUMN_THREE: int = 2
    COLUMN_FOUR: int = 3
    COLUMN_FIVE: int = 4

    ##########################
    ####  Create Widgets  ####
    ##########################

    central_widget = QWidget()
    vbox_layout = QVBoxLayout(central_widget)

    grid_widget = QWidget()
    grid_layout = QGridLayout(grid_widget)

    hbox_widget = QWidget()
    hbox_layout = QHBoxLayout(hbox_widget)

    # Add widgets to the vbox layout
    vbox_layout.addWidget(grid_widget)
    vbox_layout.addWidget(hbox_widget, alignment=Qt.AlignmentFlag.AlignBottom)

    # Set layout settings
    vbox_layout.setStretch(0, 1)  # Let grid_widget expand
    vbox_layout.setStretch(1, 0)  # Let hbox_widget take only what it needs

    #########################################
    ### Add widgets to grid (row, column) ###
    #########################################

    #########################
    ### ROW ONE | COL ONE ###
    #########################

    # Setup widgets
    self._chapter_list_body_by_combo_box_widget = QComboBox()
    self._chapter_list_body_element_line_edit_widget = QLineEdit()
    self._chapter_list_body_element_line_edit_widget.setPlaceholderText("Ex: 'ul.list-body'")

    # Create hbox widget and add to grid layout
    chapter_list_body_hbox = self._createQHBoxWidget([self._chapter_list_body_by_combo_box_widget, self._chapter_list_body_element_line_edit_widget])
    chapter_list_body_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(chapter_list_body_hbox, ROW_ONE, COLUMN_ONE)
    
    #########################
    ### ROW ONE | COL TWO ###
    #########################

    # Setup widgets
    self._chapter_list_item_by_combo_box_widget = QComboBox()
    self._chapter_list_item_element_line_edit_widget = QLineEdit()
    self._chapter_list_item_element_line_edit_widget.setPlaceholderText("Ex: 'li.list-item'")

    # Create hbox widget and add to grid layout
    chapter_list_item_hbox = self._createQHBoxWidget([self._chapter_list_item_by_combo_box_widget, self._chapter_list_item_element_line_edit_widget])
    chapter_list_item_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(chapter_list_item_hbox, ROW_ONE, COLUMN_TWO)

    #########################
    ### ROW TWO | COL ONE ###
    #########################

    # Setup widgets
    self._next_chapter_button_by_combo_box_widget = QComboBox()
    self._next_chapter_button_element_line_edit_widget = QLineEdit()
    self._next_chapter_button_element_line_edit_widget.setPlaceholderText("Ex: 'btn-resource.btn-next.at-tip'")

    # Create hbox widget and add to grid layout
    next_chapter_button_hbox = self._createQHBoxWidget([self._next_chapter_button_by_combo_box_widget, self._next_chapter_button_element_line_edit_widget])
    next_chapter_button_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(next_chapter_button_hbox, ROW_TWO, COLUMN_ONE)

    #########################
    ### ROW TWO | COL TWO ###
    #########################

    # Setup widgets
    self._chapter_text_body_by_combo_box_widget = QComboBox()
    self._chapter_text_body_element_line_edit_widget = QLineEdit()
    self._chapter_text_body_element_line_edit_widget.setPlaceholderText("Ex: 'novel_content'")

    # Create hbox widget and add to grid layout
    chapter_text_body_hbox = self._createQHBoxWidget([self._chapter_text_body_by_combo_box_widget, self._chapter_text_body_element_line_edit_widget])
    chapter_text_body_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(chapter_text_body_hbox, ROW_TWO, COLUMN_TWO)
    
    ###########################
    ### ROW THREE | COL ONE ###
    ###########################

    # Setup widgets
    self._start_idx_line_edit_widget = QLineEdit()
    self._start_idx_line_edit_widget.setPlaceholderText("Ex: '1'")

    self._end_idx_line_edit_widget = QLineEdit()
    self._end_idx_line_edit_widget.setPlaceholderText("Ex: '100'")

    # Create hbox widget and add to grid layout
    start_end_idx_hbox = self._createQHBoxWidget([self._start_idx_line_edit_widget, self._end_idx_line_edit_widget])
    start_end_idx_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(start_end_idx_hbox, ROW_THREE, COLUMN_ONE)

    ###########################
    ### ROW THREE | COL TWO ###
    ###########################

    # Setup widgets
    self._src_lang_combo_box_widget = QComboBox()

    self._dest_lang_combo_box_widget = QComboBox()

    # Create hbox widget and add to grid layout
    src_dest_lang_hbox = self._createQHBoxWidget([self._src_lang_combo_box_widget, self._dest_lang_combo_box_widget])
    src_dest_lang_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(src_dest_lang_hbox, ROW_THREE, COLUMN_TWO)

    ##########################
    ### ROW FOUR | COL ONE ###
    ##########################

    # Setup widgets
    format_text_label = QLabel("Format Text: ")
    self._format_text_check_box_widget = QCheckBox()

    # Create hbox widget and add to grid layout
    primary_settings_hbox = self._createQHBoxWidget([format_text_label, self._format_text_check_box_widget])
    primary_settings_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(primary_settings_hbox, ROW_FOUR, COLUMN_ONE)

    ##########################
    ### ROW FOUR | COL TWO ###
    ##########################

    # Setup widgets
    thread_count_label = QLabel("Thread Count: ")
    self._thread_count_combo_box_widget = QComboBox()

    # Create hbox widget and add to grid layout
    secondary_settings_hbox = self._createQHBoxWidget([thread_count_label, self._thread_count_combo_box_widget])
    secondary_settings_hbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    grid_layout.addWidget(secondary_settings_hbox, ROW_FOUR, COLUMN_TWO)

    ####################################
    ### START BUTTON AREA -- WIDGETS ###
    ####################################

    # Setup start panel itself
    hbox_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    hbox_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    # Create/setup start panel widgets
    start_button = QPushButton("Start")
    novel_name_label = QLabel("Novel Name: ")
    self._novel_name_line_edit_widget = QLineEdit()
    self._novel_name_line_edit_widget.setPlaceholderText("Ex: 'My Web Novel'")

    # Add wigets to the start panel
    hbox_layout.addWidget(novel_name_label, alignment=Qt.AlignmentFlag.AlignLeft)
    hbox_layout.addWidget(self._novel_name_line_edit_widget, stretch=3)
    hbox_layout.addSpacerItem(QSpacerItem(self.width() // 3, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
    hbox_layout.addWidget(start_button, stretch=2)

    # Set this as the central widget of the window
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


  # === Function: _on_start_pressed ===
  def _on_start_pressed(self) -> None:
    """
    Called when the start button is called
    """

    # TODO: Enter settings set into the scraper

    self._scraper.scrape(self._start_idx, self._end_idx, self._format_text)
  

  # === Function: _on_novel_link_changed ===
  def _on_novel_link_changed(self) -> None:
    """
    Function that is triggered when the novel link line-edit is changed
    """

    pass
  

  # === Function: _on_start_index_changed ===
  def _on_start_index_changed(self) -> None:
    """
    Function that is triggered when the start index line-edit is changed
    """

    pass
  

  # === Function: _on_end_index_changed ===
  def _on_end_index_changed(self) -> None:
    """
    Function that is triggered when the end index line-edit is changed
    """

    pass
  

  # === Function: _on_translation_thread_count_changed ===
  def _on_translation_thread_count_changed(self) -> None:
    """
    Function that is triggered when the thread count for translation is changed
    """

    pass
  

  # === Function: _on_chapter_list_body_element_changed ===
  def _on_chapter_list_body_element_changed(self) -> None:
    """
    Function that is triggered when the chapter list body's "element" line-edit is changed
    """

    pass


  # === Function: _on_chapter_list_item_element_changed ===
  def _on_chapter_list_item_element_changed(self) -> None:
    """
    Function that is triggered when the chapter list item's "element" line-edit is changed
    """

    pass


  # === Function: _on_next_chapter_button_element_changed ===
  def _on_next_chapter_button_element_changed(self) -> None:
    """
    Function that is triggered when the next chapter button's "element" line-edit is changed
    """

    pass
  

  # === Function: _on_chapter_text_body_element_changed ===
  def _on_chapter_text_body_element_changed(self) -> None:
    """
    Function that is triggered when the chapter text body's "element" line-edit is changed
    """

    pass





# TODO: IDEAS
# 
# Have terminal log the whole scraping process in the ui. It will be accessed through the left sidebar and will automatically be switched to when scraping starts
# terminal will have a left + right side, one for scrape other for translate.
#
# Translating happens at the same time as scraping through some sort of 'await signal' type thing
# If an error occurs to either scraping/translating, the terminal will print a red message and turn the tab header red with an X
# If the scraping/translationg finishes the tab header will turn green with a checkmark
# 