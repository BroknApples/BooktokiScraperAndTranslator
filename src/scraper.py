# Imports
import math
import re
import asyncio
from enum import Enum
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from utils import (
  INT_MAX,
  printModuleSeparator,
  getFileContentsByLine
)


class HtmlElementTag():
  """
  Holds constants for an html element's type
  """

  ID: str = "id"
  CLASS_NAME: str = "class name"
  X_PATH = By.XPATH
  X_PATH_STR: str = "By.XPATH" # Needed for string-matching to choose the correct tag type


class Scraper():
  """
  A class that allows you to scrape chapter data from a booktoki novel page
  """

  # === Subclass: HtmlElementData ===
  class HtmlElementData():
    """
    Holds the 2 things needed call find_element() on the seleniumbase webdriver
    """
    
    tag = None # Type of element tag to search this element with | NOTE: Use HtmlElementTag.XXX
    element: str = None # Actual element to find

  # ******************************************** #
  # ****************** Private ***************** #
  # ******************************************** #

  # === Constants ===
  # TODO: I HATE THE NAMING OF THESE VARIABLES BUT I DONT KNOW HOW TO FIX IT WITHOUT MAKING THEM VERY VAGUE
  _SCRAPER_SETTINGS_DIRECTORY_PATH: str = "scraper_settings"
  _SCRAPER_SETTINGS_TITLE_HEADER_LINE: str = "[Title]"
  _SCRAPER_SETTINGS_CHAPTER_LIST_READ_CHAPTER_BUTTON_HTMLDATA_HEADER_LINE: str = "[ChapterListReadChapterButtonHtmlData]"
  _SCRAPER_SETTINGS_NEXT_CHAPTER_BUTTON_HTMLDATA_HEADER_LINE: str = "[NextChapterButtonHtmlData]"
  _SCRAPER_SETTINGS_CHAPTER_TEXT_BODY_HTMLDATA_HEADER_LINE: str = "[ChapterTextBodyHtmlData]"
  _SCRAPER_SETTINGS_HTMLDATA_TAG: str = "tag="
  _SCRAPER_SETTINGS_HTMLDATA_ELEMENT: str = "element="

  """ How long with nothing happening until the webpage attempts to reconnect """
  _RECONNECT_TIME: int = 6

  # === Variables ===
  _driver = None
  _novel_chapter_list_url: str = ""

  # TODO: I HATE THE NAMING OF THESE VARIABLES BUT I DONT KNOW HOW TO FIX IT WITHOUT MAKING THEM VERY VAGUE
  """ The HTML data when you are on the chapter list webpage that corresponds to obtaining the link to any given chapter """
  _chapter_list_read_chapter_button_htmldata: HtmlElementData = HtmlElementData()
  
  """ The HTML data used to go to the next chapter when on the reading page for a chapter """
  _next_chapter_button_htmldata: HtmlElementData = HtmlElementData()

  """ The HTML data for the actual text of a chapter """
  _chapter_text_body_htmldata: HtmlElementData = HtmlElementData()

  # === Function: _getInitialChatperUrl ===
  def _getInitialChapterUrl(self, starting_chapter_number: int) -> str:
    """
    Get the url to the initial chapter to scrape

    Returns:
      any: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """

    # Log data
    print(f"Starting scrape on chapter {chapter_num}:\n")
    
    # TODO: Check this functions and the ones below,

    # Open web novel chapter list page
    self._driver.uc_open_with_reconnect(self.getNovelChapterListUrl(), reconnect_time=self._RECONNECT_TIME)
    self._driver.uc_gui_click_captcha()
    
    # NOTE: make this a changeable parameter (this can be the default tho)
    chapter_element = self._driver.find_element(By.XPATH, f'//*[@data-index="{chapter_num}"]') # Finds the chapter on the novel description page
    
    html_content = chapter_element.get_attribute("innerHTML")
    match = re.search(r'href="(.*?)"', html_content)
    if match: # Starting chapter has been opened
      return match.group(1)

  # === Function: _findNextChapterUrl ===
  def _findNextChapterUrl(self) -> str:
    # NOTE: make this a changeable parameter (this can be the default tho)
    next_chapter_link = self._driver.find_element("class name", "btn-resource.btn-next.at-tip") # Gets the link attached to the next chapter button
    
    html_content = next_chapter_link.get_attribute("innerHTML")
    match = re.search(r'href="(.*?)"', html_content)
    if match: # Chapter is found
      return match.group(1)
    else:
      return "None"

  # === Function: _scrapeChapterUrl ===
  def _scrapeChapterUrl(self, url: str, target_id: str, chapter_num: int) -> any:
    print(f"Scraping Chapter {chapter_num} URL...")
    
    self._driver.uc_open_with_reconnect(url, reconnect_time=6)
    self._driver.uc_gui_click_captcha()
    
    try:
      element = self._driver.find_element("id", target_id)
      return element.text
    except Exception as e:
      print(f"Error: {e}")
      return None

  # === Function: _loadHtmlElementData ===
  def _fillHtmlElementData(self, html_element_data: HtmlElementData, lines: list[str]) -> HtmlElementData:
    """
    Load the html element data from a scraper settings file

    Params:
      html_element_data: The HtmlElementData data structure you wihs to fill
      lines: The data you wish to input into the structure

    Returns:
      HtmlElementData: The data-filled structure
    """
    
    for line in lines:
      LINE_LENGTH: int = len(line)

      # line_type is what will be compared to find the actual data of the elemnt
      line_type: str = ""
      for ch in line:
        # When a quotation mark (") is reached, then you know that is the start of the actual data, so break
        if (ch == '"'): break
        line_type += ch
      
      if (line_type == self._SCRAPER_SETTINGS_HTMLDATA_TAG):
        # Start from index 5 to read the data, stop at LINE_LENGTH-1
        value = line[5 : LINE_LENGTH-1]

        # If value is "null", then no point in assigning it
        if (value != "null"):
          # Log tag assigning
          print("tag -> " + value)

          # Some tags have a special value that is represented by a string
          if (value == HtmlElementTag.X_PATH_STR):
            value = HtmlElementTag.X_PATH

          html_element_data.tag = value
      
      elif (line_type == self._SCRAPER_SETTINGS_HTMLDATA_ELEMENT):
        # Start from index 9 to read the data, stop at LINE_LENGTH-1
        value = line[9 : LINE_LENGTH-1]

        # If value is "null", then no point in assigning it
        if (value != "null"):
          # Log element assigning
          print("element -> " + value)

          html_element_data.element = value

    return html_element_data
  
  
  # ******************************************** #
  # ****************** Public ****************** #
  # ******************************************** #

  def testLoad(self) -> None:
    """
    TEST LOADING FUNCTIONS OUT
    """

    path: str = "booktoki.txt"

    self.loadScraperSettings(path, True)

  # === Function: __init__ ===
  def __init__(self, novel_url: str = "") -> None:
    """
    Constructor -> Sets novel chapter list url and elements to check now

    Args:
      novel_url: Url of the novel's chapter list to scrape
    """
    self.setNovelChapterListUrl(novel_url)

  # === Function: loadScraperSettings ===
  def loadScraperSettings(self, filename: str, path_override: bool = False) -> None:
    """
    Loads in settings from a file

    Params:
      filename: Name of the file to load from
      path_override: If this value is "True" then the filename is assumed to be the full path
    """
    
    # Print a module separator
    printModuleSeparator()

    # Get full file path
    full_file_path: str = ""
    if (path_override):
      # If true, then the filename is the full path
      full_file_path += filename
    else:
      # If false(default value), then the filename is just the name of the file that is in the expected location
      full_file_path += self._SCRAPER_SETTINGS_DIRECTORY_PATH + "/" + filename

    # Get the line data of the file
    lines: list[str] = getFileContentsByLine(full_file_path)
    LINE_COUNT: int = len(lines)

    # Check the contents of the file
    i: int = 0
    while (i < LINE_COUNT):
      # This line is the title header line, so the next will be the title 
      if (lines[i] == self._SCRAPER_SETTINGS_TITLE_HEADER_LINE):
        i += 1
        
        # Log title
        print(f'Loading Scraper Settings: "{lines[i]}"\n')
      
      # This line is the read chapter button header line, so the next two lines will contain the "tag" and "element" data
      elif (lines[i] == self._SCRAPER_SETTINGS_CHAPTER_LIST_READ_CHAPTER_BUTTON_HTMLDATA_HEADER_LINE):
        # Log chapter list read chapter button html element data
        print(f'Loading Chapter List Read Chapter Button HTML Element Data:')
        
        # Go to tag element line
        contents: list[str] = lines[i+1 : i+3]
        self._fillHtmlElementData(self._chapter_list_read_chapter_button_htmldata, contents)
        i += 2

        # Print empty line if not the last loop-through
        if (i != LINE_COUNT-1):
          print()

      # This line is the next chapter button header line, so the next two lines will contain the "tag" and "element" data
      elif (lines[i] == self._SCRAPER_SETTINGS_NEXT_CHAPTER_BUTTON_HTMLDATA_HEADER_LINE):
        # Log next chapter buton html element data
        print(f'Loading Next Chapter Button HTML Element Data:')

        contents: list[str] = lines[i+1 : i+3]
        self._fillHtmlElementData(self._next_chapter_button_htmldata, contents)
        i += 2

        # Print empty line if not the last loop-through
        if (i != LINE_COUNT-1):
          print()
      
      # This line is the chapter text body header line, so the next two lines will contain the "tag" and "element" data
      elif (lines[i] == self._SCRAPER_SETTINGS_CHAPTER_TEXT_BODY_HTMLDATA_HEADER_LINE):
        # Log chapter text body html element data
        print(f'Loading Chapter Text Body HTML Element Data:')
        
        contents: list[str] = lines[i+1 : i+3]
        self._fillHtmlElementData(self._chapter_text_body_htmldata, contents)
        i += 2

        # Print empty line if not the last loop-through
        if (i != LINE_COUNT-1):
          print()

      # Always increment by 1
      i += 1
    
    # Print a module separator
    printModuleSeparator()

  # === Function: saveScraperSettings ===
  def saveScraperSettings(self, filename: str) -> None:
    """
    Saves scraper settings into a file

    Params:
      filename: Name of the file that contains the scraper settings. This will be located in the 'self._SCRAPER_SETTINGS_FOLDER' directory
    """

    full_file_path: str = _SCRAPER_SETTINGS_DIRECTORY_PATH + "/" + filename

    # TODO: Save the current element data in the file

  # === Function: scrape ===
  def scrape(self, start_idx: int = 0, end_idx: int = INT_MAX) -> list:
    """
    Starts the scraping of a booktoki novel.

    NOTE: Must have called these functions:
      'setNovelUrl()'

    Args:
      novel_url: Link to the webpage that contains the chapter list
      start_idx: Chapter number to start the scrape.    NOTE: Constraints: (start_idx <= end_idx)
      end_idx: Chapter to end the scrape at.    NOTE: Constraints: (end_idx >= start_idx)

    Returns:
      list: List of the untranslated novel chapters (list[0] = untranslated starting chapter, ..., list[n] = untranslated ending chapter)
    """

    # Setup driver
    self.initializeWebDriver()

    # Check if the proper varables have been instantiated
    if (self.getNovelUrl() == ""):
      return []

    # Enforce index constraints
    if (end_idx < start_idx):
      end_idx = start_idx

    # Log starting message
    print(
      "Starting scrape with params: \n"
      "\tNovel Url: " + self.getNovelUrl() + "\n"

      "\tStarting Chapter Number: " + "\n"
      "\tEnding Chapter Number: " + str(end_idx)
    )

    # TODO: Do scrape here

    # Close driver
    self.uninitializeWebDriver()
  

  # ******************************************** #
  # ************** Getters/Setters ************* #
  # ******************************************** #

  # === Function: initializeWebDriver ===
  def initializeWebDriver(self) -> None:
    """
    Initialize the web driver object
    """
    self._driver = Driver(uc=True, headless=False)
  
  # === Function: uninitializeWebDriver ===
  def uninitializeWebDriver(self) -> None:
    """
    Reset the driver object to null to reset/close the browser session
    """
    self._driver = None

  # === Function: setNovelChapterListUrl ===
  def setNovelChapterListUrl(self, value: str) -> None:
    """
    Sets the url to the booktoki novel you want to scrape chapter data from

    Args:
      value: Url to the booktoki novel you wish to scrape
    """
    self._novel_chapter_list_url = value
  
  # === Function: getNovelChapterListUrl ===
  def getNovelChapterListUrl(self) -> str:
    """
    Gets the novel url set in a 'Scraper' object

    Returns:
      str: Url to the booktoki novel you wish to scrape
    """
    return self._novel_chapter_list_url

  # === Function: setChapterListReadChapterButtonHtmlData ===
  def setChapterListReadChapterButtonHtmlData(self, tag, element: str) -> None:
    """
    Set the HTML data that points to the read chapter button of an
    """

    self._chapter_list_read_chapter_button_htmldata.tag = tag
    self._chapter_list_read_chapter_button_htmldata.element = element

  # === Function: getChapterListReadChapterButtonHtmlData ===
  def getChapterListReadChapterButtonHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to the read chapter button of an
    """

    return self._chapter_list_read_chapter_button_htmldata

  # === Function: setNextChapterButtonHtmlData ===
  def setNextChapterButtonHtmlData(self, tag, element: str) -> None:
    """
    Set the HTML data that points to the next chapter button on a chapter page
    """

    self._next_chapter_button_htmldata.tag = tag
    self._next_chapter_button_htmldata.element = element

  # === Function: getNextChapterButtonHtmlData ===
  def getNextChapterButtonHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to the next chapter button on a chapter page
    """

    return self._next_chapter_button_htmldata

  # === Function: setChapterTextBodyHtmlData ===
  def setChapterTextBodyHtmlData(self, tag, element: str) -> None:
    """
    Set the HTML data that points to the text of an actual chapter
    """

    self._chapter_text_body_htmldata.tag = tag
    self._chapter_text_body_htmldata.element = element

  # === Function: getChapterTextBodyHtmlData ===
  def getChapterTextBodyHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to the text of an actual chapter
    """
    return self._chapter_text_body_htmldata