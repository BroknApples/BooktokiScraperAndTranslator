"""

NOTE: TEST TRANSLATION NOVEL (Academy's Undercover Professor) lol
  link = https://booktoki468.com/novel/6219?book=일반소설

"""


# Imports
import asyncio
import os
import threading
from src.common.scraper import Scraper
from src.common.translator import TextTranslator
from src.common.utils import (
  Limits,
  createDirectory,
  splitRangeIntoChunks
)


# === Constants ===
OUTPUT_DIRECTORY_ROOT: str = "translations" # Directory that novels will be outputted to

# === Function: executeScrapeAndTranslate ===
def executeScrapeAndTranslate(novel_url: str, scraper_settings_filename: str, start_idx: int, end_idx: int, output_directory: str) -> list[str]:
  """
  Does the actual work for scraping and translating a novel

  Params:
    start_idx: Chapter to start on
    end_idx: Chapter to end on


  Returns:
    list[str]: The translated chapter data
  """

  # Create scraper and translator object
  scraper: Scraper = Scraper()
  translator: TextTranslator = TextTranslator()

  # Set the scraper settings
  if (scraper_settings_filename != ""):
    scraper.loadScraperSettings(scraper_settings_filename)

  # Initialize values in the scraper
  scraper.setNovelChapterListUrl(novel_url)

  # Initialize values in the translator
  # TODO: MAKE THESE ACTUALLY CHANGEABLE
  translator.setSourceLanguage(TextTranslator.Languages.KOREAN)
  translator.setDestinationLanguage(TextTranslator.Languages.ENGLISH)

  # Start the scrape
  chapter_data: list[str] = scraper.scrape(start_idx=start_idx, end_idx=end_idx, format_text=True)
  CHAPTER_DATA_SIZE: int = len(chapter_data)

  # Translate the data
  translation_data: list[str] = translator.translateStringArray(chapter_data)

  # Error during translation
  if (translation_data == None):
    print("Could not translate the data. Please use a valid translation language.")
    sys.exit(1)

  # Create the directory to save to
  while not createDirectory(output_directory, False):
    print("Invalid output directory name.")

    output_directory = ""
    while (output_directory == ""):
      output_directory = ""
      output_directory = input("Enter a name for your output directory: ")
    output_directory = OUTPUT_DIRECTORY_ROOT + "/" + output_directory

  # Save the translated data to the disk
  NOVEL_DATA_ARRAY_SIZE: int = len(translation_data)
  CHAPTER_NAME: str = "Chapter " # NOTE: Appends the number to the end when using
  array_index: int = 0 # Used to actually index the array
  for i in range(start_idx, start_idx + NOVEL_DATA_ARRAY_SIZE):
    # Create chapter name
    curr_chapter_name: str = CHAPTER_NAME + str(i) + ".txt"

    # Write to file
    with open(output_directory + "/" + curr_chapter_name, "w", encoding="utf-8") as f:
      f.write(translation_data[array_index])
    
    # Increment array index
    array_index += 1

# === Function: main ===
async def main() -> None:
  """
  Entry point for the program.

  Defines the objects needed to scrape and translate a novel
  """

  # Print some whitespace before starting
  print()

  # Setup translations directory, if not already done
  os.makedirs(OUTPUT_DIRECTORY_ROOT, exist_ok=True)

  running: bool = True # Is the application running

  while running:
    scraper_settings_filename: str = "Uninitialized"
    while ".txt" not in scraper_settings_filename and scraper_settings_filename != "":
      scraper_settings_filename = ""
      scraper_settings_filename = input("Enter the scraper settings filename (Press Enter for 'Booktoki'): ")
    if (scraper_settings_filename == ""):
      scraper_settings_filename = "booktoki.ini"

    # Get the novel URL
    # TODO: pip install validators and check if the url is a valid url before proceeding
    novel_url: str = input("Enter the novel URL: ")

    # Get the starting chapter index
    start_idx = "Uninitialized"
    while not start_idx.isdigit() and start_idx != "":
      start_idx = ""
      start_idx = input("Enter the starting chapter(Press ENTER for Chapter 1): ")
    if start_idx == "":
      start_idx = "1"
    start_idx = int(start_idx)
    
    # Get the ending chapter 
    end_idx = "Uninitialized"
    while not end_idx.isdigit() and end_idx != "":
      end_idx = ""
      end_idx = input("Enter the ending chapter(Press ENTER for the Latest Chapter): ")
    if end_idx == "":
      end_idx = Limits.INT_MAX
    end_idx = int(end_idx)
      
    # Get the directory to save files to
    output_directory: str = ""
    while (output_directory == ""):
      output_directory = input("Enter a name for your output directory: ")
    output_directory = OUTPUT_DIRECTORY_ROOT + "/" + output_directory

    # Scrape the novel
    start = input("Start scrape? (y/n): ")
    if (start == "y"):
      # TODO: Fix the threading issues (can't safely create multiple browsers so only set threading for translation and writing to disk)
      thread_count = 1

      # How many chapters should each thread do?
      thread_ranges: list[tuple[int]] = splitRangeIntoChunks(start_idx, end_idx, thread_count)

      # Create threads
      threads: list[threading.Thread] = [None] * thread_count
      for i in range(thread_count):
        threads[i] = threading.Thread(target=executeScrapeAndTranslate, args=(novel_url, scraper_settings_filename, thread_ranges[i][0], thread_ranges[i][1], output_directory))
      
      # Start threads
      for t in threads:
        t.start()
      
      # Join threads
      for t in threads:
        t.join()
    
    continue_choice = input("Translate another novel? (y/n): ")

    if (continue_choice != "y"):
      running = False


# Run the main script
asyncio.run(main())