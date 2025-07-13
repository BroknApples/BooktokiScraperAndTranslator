# Imports
import asyncio
import os
from src.scraper import Scraper
from src.translator import TextTranslator
from src.ui import setupGui

# NOTE: TEST TRANSLATION NOVEL (Academy's Undercover Professor) lol
# https://booktoki468.com/novel/6219?book=일반소설

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
  setupGui()

  # TODO: Review this entire while loop and change to a ui-based version
  #       better yet, just put this entire while loop inside the ui.py file
  #       and have a class that accepts the translator/scraper as parameters
  #       for functions or something idk...
  while running:
    pass


# Run the main script
asyncio.run(main())