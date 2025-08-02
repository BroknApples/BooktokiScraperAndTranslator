# Imports
import time
import re
import configparser
from enum import Enum
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from src.common.utils import (
  Limits,
  printModuleSeparator,
  getFileContentsByLine,
  formatNovelText
)


# === Class: Scraper ===
class Scraper():
  """
  A class that allows you to scrape chapter data from a booktoki novel page
  """


  # === Subclass: HtmlElementData ===
  class HtmlElementData():
    """
    Holds the 2 things needed call find_element() on the seleniumbase webdriver
    """


    # === Subclass: Bys ===
    class Bys():
      """
      Holds constants for an html element's type
      """

      ID: str = "id"
      CLASS_NAME: str = "class name"
      X_PATH: str = "xpath"
      CSS_SELECTOR: str = "css selector"


    # === Subclass: Elements ===
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


    # === Constants ===
    BY: str = "by"
    ELEMENT: str = "element"
    BY_MAP: dict = {
      Bys.ID : By.ID,
      Bys.CLASS_NAME : By.CLASS_NAME,
      Bys.X_PATH : By.XPATH,
      Bys.CSS_SELECTOR : By.CSS_SELECTOR
    }


    # === Variables ===
    by = None # Type of element by to search this element with | NOTE: Use HtmlElement.Bys.XXX
    element: str = None # Actual element to find
  

    # === Function: applyByMap ===
    def applyByMap(self) -> None:
      """
      Apply the by map to a HtmlElementData object
      """

      self.by = self.BY_MAP.get(self.by)


  # ******************************************** #
  # ****************** Private ***************** #
  # ******************************************** #


  # === Constants ===
  # TODO: I HATE THE NAMING OF THESE VARIABLES BUT I DONT KNOW HOW TO FIX IT WITHOUT MAKING THEM VERY VAGUE
  _SCRAPER_SETTINGS_DIRECTORY_PATH: str = "cfg/scraper_settings"
  _SCRAPER_SETTINGS_CHAPTER_LIST_BODY_HTMLDATA_HEADER: str = "ChapterListBodyHtmlData"
  _SCRAPER_SETTINGS_CHAPTER_LIST_ITEM_HTMLDATA_HEADER: str = "ChapterListItemHtmlData"
  _SCRAPER_SETTINGS_NEXT_CHAPTER_BUTTON_HTMLDATA_HEADER: str = "NextChapterButtonHtmlData"
  _SCRAPER_SETTINGS_CHAPTER_TEXT_BODY_HTMLDATA_HEADER: str = "ChapterTextBodyHtmlData"

  """ How long with nothing happening until the webpage attempts to reconnect """
  _RECONNECT_TIME: int = 6


  # === Variables ===
  _wait = None
  _driver = None
  _novel_chapter_list_url: str = ""

  """ The HTML data when you are on the chapter list webpage that corresponds the list of chapters """
  _chapter_list_body_htmldata: HtmlElementData = HtmlElementData()

  """ The HTML data when you are on the chapter list webpage that corresponds to an actual item in the chapter list"""
  _chapter_list_item_htmldata: HtmlElementData = HtmlElementData()
  
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
  def _getInitialChapterUrl(self, chapter_num: int) -> str | None:
    """
    Get the url to the initial chapter to scrape

    Params:
      chapter_num: Chapter to start scraping on (If this chapter doesnt exist, this function will return None)

    Returns:
      str | None: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """

    # Open web novel chapter list page
    try:
      self._driver.uc_open_with_reconnect(self.getNovelChapterListUrl(), reconnect_time=self._RECONNECT_TIME)
      self._driver.uc_gui_click_captcha()

      # # Loop through each <li> element and print its data-index attribute and text
      # for i, li in enumerate(list_items):
      #   data_index = li.get_attribute("data-index")
      #   text = li.text
      #   print(f"Item {i} - data-")

      try:
        # Get the target <ul> element on the chapter list page
        list_body_params: Scraper.HtmlElementData = self.getChapterListBodyHtmlData()
        ul_element = self._wait.until(EC.presence_of_element_located((list_body_params.by, list_body_params.element)))

        # Find all <li> elements inside that <ul>
        list_item_params: Scraper.HtmlElementData = self.getChapterListItemHtmlData()
        list_items = ul_element.find_elements(list_item_params.by, list_item_params.element)

        # Return the link OR 'None' if it doesn't exist | NOTE: Get the Nth from the end chapter num
        # TODO: Get the ending chapter number by taking the size of the list_items array (only if it was assigned 'Limits.INT_MAX' ofc)
        return self._getHrefFromHtmlElement(list_items[-chapter_num])

      # Element not found
      except NoSuchElementException:
        print("No such element.")
        return None

      # Other error
      except Exception as e:
        print(f"Error: [{e}]")
        return None
    
    # Web driver was closed
    except WebDriverException:
      print("Exited WebDriver early, returning None.")
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
      target_element = self._driver.find_element(data_params.by, data_params.element)

      # Return the link OR 'None' if it doesn't exist
      return self._getHrefFromHtmlElement(target_element)
    # Element not found
    except NoSuchElementException:
      print("No such element.")
      return None

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
      str OR None: The URL to the initial chapter to scrape OR None if the webpage doesn't exist
    """
    
    try:
      self._driver.uc_open_with_reconnect(url, reconnect_time=self._RECONNECT_TIME)
      self._driver.uc_gui_click_captcha()
      
      # Get the params to be used in 'find_element'
      data_params: Scraper.HtmlElementData = self.getChapterTextBodyHtmlData()

      try:
        # Get the target element
        element = self._driver.find_element(data_params.by, data_params.element)
      
        # Return the element's text if possible
        return element.text

      # Element not found
      except NoSuchElementException:
        print("No such element.")
        return None


      except Exception as e:
        # If there is no such element, print the error and return 'None'
        print(f"Error: {e}")
        return None
    
    # Web driver was closed
    except WebDriverException:
      print("Exited WebDriver early, returning None.")
      return None
  

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
    self.loadScraperSettings("booktoki.ini")

    self.setNovelChapterListUrl(novel_url)


  # === Function: initializeWebDriver ===
  def initializeWebDriver(self) -> None:
    """
    Initialize the web driver object
    """

    self._driver = Driver(uc=True, headless=False)
    self._wait = WebDriverWait(self._driver, self._RECONNECT_TIME)
  

  # === Function: uninitializeWebDriver ===
  def uninitializeWebDriver(self) -> None:
    """
    Reset the driver object to null to reset/close the browser session
    """
    
    self._driver.close()
    self._driver = None
    self._wait = None
  

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

    # Log filename
    print(f'Loading Scraper Settings: "{filename}"\n')

    # Get full file path
    full_file_path: str = ""
    if (path_override):
      # If true, then the filename is the full path
      full_file_path += filename
    else:
      # If false(default value), then the filename is just the name of the file that is in the expected location
      full_file_path += self._SCRAPER_SETTINGS_DIRECTORY_PATH + "/" + filename

    # Get the line data of the file
    config = configparser.ConfigParser()
    config.read(full_file_path)

    # Get sections
    chapter_list_body_section = config[Scraper._SCRAPER_SETTINGS_CHAPTER_LIST_BODY_HTMLDATA_HEADER]
    chapter_list_item_section = config[Scraper._SCRAPER_SETTINGS_CHAPTER_LIST_ITEM_HTMLDATA_HEADER]
    next_chapter_button_section = config[Scraper._SCRAPER_SETTINGS_NEXT_CHAPTER_BUTTON_HTMLDATA_HEADER]
    text_body_section = config[Scraper._SCRAPER_SETTINGS_CHAPTER_TEXT_BODY_HTMLDATA_HEADER]

    # List body
    self._chapter_list_body_htmldata.by = chapter_list_body_section.get(Scraper.HtmlElementData.BY).strip('"')
    self._chapter_list_body_htmldata.element = chapter_list_body_section.get(Scraper.HtmlElementData.ELEMENT).strip('"')

    # List item
    self._chapter_list_item_htmldata.by = chapter_list_item_section.get(Scraper.HtmlElementData.BY).strip('"')
    self._chapter_list_item_htmldata.element = chapter_list_item_section.get(Scraper.HtmlElementData.ELEMENT).strip('"')

    # Next chapter button
    self._next_chapter_button_htmldata.by = next_chapter_button_section.get(Scraper.HtmlElementData.BY).strip('"')
    self._next_chapter_button_htmldata.element = next_chapter_button_section.get(Scraper.HtmlElementData.ELEMENT).strip('"')

    # Text body
    self._chapter_text_body_htmldata.by = text_body_section.get(Scraper.HtmlElementData.BY).strip('"')
    self._chapter_text_body_htmldata.element = text_body_section.get(Scraper.HtmlElementData.ELEMENT).strip('"')

    # Print results
    print(f"[{Scraper._SCRAPER_SETTINGS_CHAPTER_LIST_BODY_HTMLDATA_HEADER}]: "
          f'\n{Scraper.HtmlElementData.BY} = "{self._chapter_list_body_htmldata.by}"'
          f'\n{Scraper.HtmlElementData.ELEMENT} = "{self._chapter_list_body_htmldata.element}"'
           "\n")
    
    print(f"[{Scraper._SCRAPER_SETTINGS_CHAPTER_LIST_ITEM_HTMLDATA_HEADER}]: "
          f'\n{Scraper.HtmlElementData.BY} = "{self._chapter_list_item_htmldata.by}"'
          f'\n{Scraper.HtmlElementData.ELEMENT} = "{self._chapter_list_item_htmldata.element}"'
          "\n")
    
    print(f"[{Scraper._SCRAPER_SETTINGS_NEXT_CHAPTER_BUTTON_HTMLDATA_HEADER}]: "
          f'\n{Scraper.HtmlElementData.BY} = "{self._next_chapter_button_htmldata.by}"'
          f'\n{Scraper.HtmlElementData.ELEMENT} = "{self._next_chapter_button_htmldata.element}"'
          "\n")
    
    print(f"[{Scraper._SCRAPER_SETTINGS_CHAPTER_TEXT_BODY_HTMLDATA_HEADER}]: "
          f'\n{Scraper.HtmlElementData.BY} = "{self._chapter_text_body_htmldata.by}"'
          f'\n{Scraper.HtmlElementData.ELEMENT} = "{self._chapter_text_body_htmldata.element}"'
          "")
    
    # Apply the by map
    self._chapter_list_body_htmldata.applyByMap()
    self._chapter_list_item_htmldata.applyByMap()
    self._next_chapter_button_htmldata.applyByMap()
    self._chapter_text_body_htmldata.applyByMap()

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
  def scrape(self, start_idx: int = 0, end_idx: int = Limits.INT_MAX, format_text: bool = True) -> list[str]:
    """
    Starts the scraping of a booktoki novel.

    NOTE: Must have called these functions:
      'setNovelUrl()'

    Args:
      novel_url: Link to the webpage that contains the chapter list
      start_idx: Chapter number to start the scrape.    NOTE: Constraints: (start_idx <= end_idx)
      end_idx: Chapter to end the scrape at.    NOTE: Constraints: (end_idx >= start_idx)
      format_text: Should the text be formatted into a more readable form (extra whitespaces, replace some characters, etc.)?

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
      "\tText Formatting: " + str(format_text) + "\n"
    )

    # Create empty container for each chapter's text data
    chapter_text: list[str] = []
    
    # Get the url for the first chapter
    curr_url: str = self._getInitialChapterUrl(start_idx)

    # Scrape each chapter in the specified range
    for chapter_num in range (int(start_idx), int(end_idx) + 1):
      # If the chapter url doesn't exist, leave loop to prevent errors
      if (curr_url == None): break

      # Log chapter scraping progess
      print(f"Scraping chapter #{chapter_num}...")


      # TODO: Implement a check that if a page is left going afk for long enough,
      #       it will attepmt to redo the scrape from this chapter index


      # Get the text for this chapter
      curr_chapter_text: str = self._scrapeChapter(curr_url)

      # Format text, if set
      if (format_text):
        curr_chapter_text = formatNovelText(curr_chapter_text)

      # Return if no data was recieved
      if (curr_chapter_text == None): break

      # Append chapter text to array
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


  # # === Function: setThreadCount ===
  # def setThreadCount(self, thread_count: int = None) -> None:
  #   """
  #   Set the number of threads to be used when scraping the novel

  #   Params:
  #     thread_count: New thread count for the scraper
  #   """
  #   self._thread_count = thread_count


  # # === Function: getThreadCount ===
  # def getThreadCount(self) -> int:
  #   """
  #   Get the number of threads to be used when scraping the novel

  #   Returns:
  #     int: The thread count for the scraper
  #   """
  #   return self._thread_count


  # === Function: setChapterListBodyHtmlData ===
  def setChapterListBodyHtmlData(self, by, element: str) -> None:
    """
    Set the HTML data that points to the chapter list body's html data

    Params:
      by: The element type to search for
      element: The element's name ('button.open-menu', 'db.cs-rm', etc.)
    """

    self._chapter_list_body_htmldata.by = by
    self._chapter_list_body_htmldata.element = element


  # === Function: getChapterListBodyHtmlData ===
  def getChapterListBodyHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to a list body

    Returns:
      HtmlElementData: Data structure that outlines the html element that corresponds to the 'chapter list body'
    """

    return self._chapter_list_body_htmldata
  

  # === Function: setChapterListItemHtmlData ===
  def setChapterListItemHtmlData(self, by, element: str) -> None:
    """
    Set the HTML data that points to the chapter list item's html data

    Params:
      by: The element type to search for
      element: The element's name ('button.open-menu', 'db.cs-rm', etc.)
    """

    self._chapter_list_item_htmldata.by = by
    self._chapter_list_item_htmldata.element = element


  # === Function: getChapterListItemHtmlData ===
  def getChapterListItemHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to a list item

    Returns:
      HtmlElementData: Data structure that outlines the html element that corresponds to the 'chapter list item'
    """

    return self._chapter_list_item_htmldata


  # === Function: setNextChapterButtonHtmlData ===
  def setNextChapterButtonHtmlData(self, by, element: str) -> None:
    """
    Set the HTML data that points to the next chapter button on a chapter page

    Params:
      by: The element type to search for
      element: The element's name ('button.open-menu', 'db.cs-rm', etc.)
    """

    self._next_chapter_button_htmldata.by = by
    self._next_chapter_button_htmldata.element = element


  # === Function: getNextChapterButtonHtmlData ===
  def getNextChapterButtonHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to the next chapter button on a chapter page

    Returns:
      HtmlElementData: Data structure that outlines the html element that corresponds to the 'next chapter button'
    """

    return self._next_chapter_button_htmldata


  # === Function: setChapterTextBodyHtmlData ===
  def setChapterTextBodyHtmlData(self, by, element: str) -> None:
    """
    Set the HTML data that points to the text of an actual chapter

    Params:
      by: The element type to search for
      element: The element's name ('button.open-menu', 'db.cs-rm', etc.)
    """

    self._chapter_text_body_htmldata.by = by
    self._chapter_text_body_htmldata.element = element


  # === Function: getChapterTextBodyHtmlData ===
  def getChapterTextBodyHtmlData(self) -> HtmlElementData:
    """
    Get the HTML data that points to the text of an actual chapter

    Returns:
      HtmlElementData: Data structure that outlines the html element that corresponds to the 'chapter text body'
    """
    return self._chapter_text_body_htmldata 