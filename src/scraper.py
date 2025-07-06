# Imports
import math
import re
import asyncio
from enum import Enum
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from src.utils import (
  INT_MAX,
  printModuleSeparator,
  getFileContentsByLine
)


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

    class Tags():
      """
      Holds constants for an html element's type
      """

      ID: str = "id"
      CLASS_NAME: str = "class name"
      X_PATH = By.XPATH
      X_PATH_STR: str = "By.XPATH" # Needed for string-matching to choose the correct tag type

    class Elements():
      """
      Holds constants/functions for generating HtmlElementData element names
      """

      FILL_VALUE: str = "{_VALUE_}"

      @staticmethod
      def fillElementWithValue(element: str, value: str) -> str:
        """
        Fill a slot in an element that has the string "_VALUE_" somewhere in it, which represents
        that a place should be replaced with a value at some point

        Params:
          element: String to modify
          value: Value to insert at some position

        Returns:
          str: Modified string with the value inserted in the place of the FILL_VALUE constnat
        """

        # If the fill value constant is in the string, then we should replace something
        if (Scraper.HtmlElementData.Elements.FILL_VALUE in element):
          new_element: str = element.replace(Scraper.HtmlElementData.Elements.FILL_VALUE, str(value))
          return new_element
        
        # The fill value constant wasn't present, so we just return the original value
        return element
  

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

  # === Function: _getHrefFromHtmlElement ===
  def _getHrefFromHtmlElement(self, element) -> str | None:
    """
    Get the href element embedded within an html element

    Params:
      element: Element to check
    
    Returns:
      str | None: The href element embedded within the element OR None if there is no href element
    """

    # Get the html content and search for whatever href element is present
    html_content = element.get_attribute("innerHTML")
    match = re.search(r'href="(.*?)"', html_content)

    # If there is some href element, then the button does contain a link!
    if match: 
      return match.group(1)
    # Else, return None since it doesn't exist
    else:
      return None

  # === Function: _getInitialChapterUrl ===
  def _getInitialChapterUrl(self, chapter_num: int) -> str:
    """
    Get the url to the initial chapter to scrape

    Params:
      chapter_num: Chapter to start scraping on (If this chapter doesnt exist, this function will return None)

    Returns:
      str | None: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """

    # Open web novel chapter list page
    self._driver.uc_open_with_reconnect(self.getNovelChapterListUrl(), reconnect_time=self._RECONNECT_TIME)
    self._driver.uc_gui_click_captcha()
    
    # Get the params to be used in 'find_element'
    data_params: Scraper.HtmlElementData = self.getChapterListReadChapterButtonHtmlData()
    
    # If the data params includes a FILL_VALUE,
    # fill that value with the starting chapter
    if (self.HtmlElementData.Elements.FILL_VALUE in data_params.element):
      data_params.element = Scraper.HtmlElementData.Elements.fillElementWithValue(data_params.element, chapter_num)

    try:
      # Get the target element on the chapter list page
      target_element = self._driver.find_element(data_params.tag, data_params.element) 

      # Return the link OR 'None' if it doesn't exist
      return self._getHrefFromHtmlElement(target_element)

    except Exception as e:
      # If there is no such element, print the error and return 'None'
      print(f"Error: {e}")
      return None
    
  # === Function: _findNextChapterUrl ===
  def _findNextChapterUrl(self) -> str | None:
    """
    Get the URL for the next chapter button. Use when on a chapter page.

    Returns:
      str | None: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """

    # Get the params to be used in 'find_element'
    data_params: Scraper.HtmlElementData = self.getNextChapterButtonHtmlData()

    try:
      # Get the target element
      target_element = self._driver.find_element(data_params.tag, data_params.element)

      # Return the link OR 'None' if it doesn't exist
      return self._getHrefFromHtmlElement(target_element)

    except Exception as e:
      # If there is no such element, print the error and return 'None'
      print(f"Error: {e}")
      return None

  # === Function: _scrapeChapter ===
  def _scrapeChapter(self, url: str) -> str | None:
    """
    Does the actual scraping of chapter data. Utilizes '_chapter_text_body_htmldata'

    Params:
      url: Url to scrape data from

    Returns:
      str | None: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """
    
    self._driver.uc_open_with_reconnect(url, reconnect_time=self._RECONNECT_TIME)
    self._driver.uc_gui_click_captcha()
    
    # Get the params to be used in 'find_element'
    data_params: Scraper.HtmlElementData = self.getChapterTextBodyHtmlData()

    try:
      # Get the target element
      element = self._driver.find_element(data_params.tag, data_params.element)
    
      # Return the element's text if possible
      return element.text

    except Exception as e:
      # If there is no such element, print the error and return 'None'
      print(f"Error: {e}")
      return None

  # === Function: _fillHtmlElementData ===
  def _fillHtmlElementData(self, html_element_data: HtmlElementData, lines: list[str]) -> HtmlElementData:
    """
    Fills the html element data from some data arrays

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
          if (value == self.HtmlElementData.Tags.X_PATH_STR):
            value = self.HtmlElementData.Tags.X_PATH

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

  # === Function: __init__ ===
  def __init__(self, novel_url: str = "") -> None:
    """
    Constructor -> Sets novel chapter list url and elements to check now

    Args:
      novel_url: Url of the novel's chapter list to scrape
    """

    # Load the default settings
    # TODO: Eventually add some actual '_default_settings' variable that can be used to change the default sraper settings
    self.loadScraperSettings("booktoki.txt")

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

    print(f'Loading from file path: "{full_file_path}"')

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

    full_file_path: str = self._SCRAPER_SETTINGS_DIRECTORY_PATH + "/" + filename

    # TODO: Implment -> Save the current element data in the file

  # === Function: scrape ===
  def scrape(self, start_idx: int = 0, end_idx: int = INT_MAX) -> list[str]:
    """
    Starts the scraping of a booktoki novel.

    NOTE: Must have called these functions:
      'setNovelUrl()'

    Args:
      novel_url: Link to the webpage that contains the chapter list
      start_idx: Chapter number to start the scrape.    NOTE: Constraints: (start_idx <= end_idx)
      end_idx: Chapter to end the scrape at.    NOTE: Constraints: (end_idx >= start_idx)

    Returns:
      list[str]: List of the untranslated novel chapters (list[0] = untranslated starting chapter, ..., list[n] = untranslated ending chapter)
    """
    
    # Setup driver
    self.initializeWebDriver()

    # Check if the proper varables have been instantiated
    if (self.getNovelChapterListUrl() == ""):
      return []

    # Enforce index constraints
    if (end_idx < start_idx):
      end_idx = start_idx

    # Print module seperator
    printModuleSeparator()

    # Log starting message
    print(
      "Starting Scrape With Parameters: \n"
      "\tNovel Url: " + self.getNovelChapterListUrl() + "\n"
      "\tStarting Chapter: " + str(start_idx) + "\n"
      "\tEnding Chapter: " + str(end_idx) + "\n"
    )

    # Create empty container for each chapter's text data
    chapter_text: list[str] = []
    
    # Get the url for the first chapter
    curr_url: str = self._getInitialChapterUrl(start_idx)

    # Scrape each chapter in the specified range
    for chapter_num in range (int(start_idx), int(end_idx) + 1):
      # If the chapter url doesn't exist, leave loop to prevent errors
      if (curr_url == "None"): break

      # Log chapter scraping progess
      print(f"Scraping chapter #{chapter_num}...")


      # TODO: Implement a check that if a page is left going afk for long enough,
      #       it will attepmt to redo the scrape from this chapter index


      # Get the text for this chapter
      curr_chapter_text: str = self._scrapeChapter(curr_url)
      chapter_text.append(curr_chapter_text)
      
      # Get the next chapter's URL
      curr_url = self._findNextChapterUrl()

    # Close driver
    self.uninitializeWebDriver()

    # Log the scrape's completion
    print("\nScraping Complete!")

    # Print module seperator
    printModuleSeparator()

    # Return the chapter data
    return chapter_text
  

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
    self._driver.close()
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