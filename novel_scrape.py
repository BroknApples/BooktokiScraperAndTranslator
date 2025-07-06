# Imports
import asyncio
import os
from src.utils import (
  ensureModuleInstalled
)

# NOTE: Check that the required modules are installed
ensureModuleInstalled("selenium")
ensureModuleInstalled("seleniumbase")
ensureModuleInstalled("googletrans", "googletrans==4.0.0-rc1")

from src.scraper import Scraper
from src.translator import TextTranslator

# TODO: Try deep-translator for translation when done

# === Function: main ===
async def main() -> None:
  """
  Entry point for the program.

  Defines the objects needed to scrape and translate a novel
  """

  # Print some whitespace before starting
  print()

  # Setup directory if not already
  OUTPUT_DIRECTORY_ROOT: str = "translations/" # Directory that novels will be outputted to
  os.makedirs(OUTPUT_DIRECTORY_ROOT, exist_ok=True)

  running: bool = True # Is the application running
  scraper: Scraper = Scraper()
  translator: TextTranslator = TextTranslator()

  # NOTE: TEST TRANSLATION NOVEL (Academy's Undercover Professor) lol
  # https://booktoki468.com/novel/6219?book=일반소설

  # NOTE: Example:
  # untranslated_text: str = "아카데미 에위장취업당했다-277화"
  # translated_text: str = translator.translateString(untranslated_text)
  # print("The translated text is: " + translated_text)

  # TODO: Review this entire while loop and change to a ui-based version
  #       better yet, just put this entire while loop inside the ui.py file
  #       and have a class that accepts the translator/scraper as parameters
  #       for functions or something idk...
  while running:
    # Get the novel URL
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
      end_idx = "2147000000"
    end_idx = int(end_idx)
      
    # Get the directory to save files to
    output_directory: str = ""
    while (output_directory == ""):
      output_directory = input("Enter a name for your output directory: ")
    output_directory = OUTPUT_DIRECTORY_ROOT + output_directory
    
    # TODO: Do actual work here
    start = input("Start scrape? (y/n): ")
    if (start == "y"):
      # Scrape the novel

      # Initialize values in the scraper
      scraper.setNovelChapterListUrl(novel_url)

      # Initialize values in the translator
      # TODO: MAKE THESE ACTUALLY CHANGEABLE
      translator.setSourceLanguage(TextTranslator.Languages.KOREAN)
      translator.setDestinationLanguage(TextTranslator.Languages.ENGLISH)

      # Start the scrape
      chapter_data: list[str] = scraper.scrape(start_idx=start_idx, end_idx=end_idx)
      CHAPTER_DATA_SIZE: int = len(chapter_data)

      # Log text formatting
      print("Formatting text...")

      # Fix chapter data if necessary
      for i in range(CHAPTER_DATA_SIZE):
        # Prevent erros
        if (chapter_data[i] == None): continue

        # Replace weird ellipses characters with actual periods
        chapter_data[i] = chapter_data[i].replace('…', '...')

        # Replace one newline with 2, for visual seperation
        chapter_data[i] = chapter_data[i].replace("\n", "\n\n")

      # Log text formatting complete
      print("Text formatting complete!\n")

      # Translate the data
      translation_data: list[str] = translator.translateStringArray(chapter_data)
      
      # Create the directory to save to
      os.makedirs(output_directory, exist_ok=False)

      # Save the translated data to the disk
      CHAPTER_NAME: str = "Chapter " # NOTE: Appends the number to the end when using
      array_index: int = 0 # Used to actually index the array
      for i in range(start_idx, end_idx + 1):
        # Create chapter name
        curr_chapter_name: str = CHAPTER_NAME + str(i) + ".txt"

        # Write to file
        with open(output_directory + "/" + curr_chapter_name, "w", encoding="utf-8") as f:
          f.write(translation_data[array_index])
        
        # Increment array index
        array_index += 1
    
    continue_choice = input("Continue? (y/n): ")

    if (continue_choice != "y"):
      running = False


# Run the main script
asyncio.run(main())