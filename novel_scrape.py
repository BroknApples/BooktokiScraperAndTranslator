# Imports
import asyncio
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

  running: bool = True # Is the application running
  scraper: Scraper = Scraper()
  translator: TextTranslator = TextTranslator()

  # TESTING THE SCRAPER SETTINGS LOADER:
  scraper.testLoad()

  # NOTE: Example:
  # untranslated_text: str = "아카데미 에위장취업당했다-277화"
  # translated_text: str = translator.translateString(untranslated_text)
  # print("The translated text is: " + translated_text)

  while (running):
    # TESTING -> Temporary print choices instead of ui variables
    pass


# Run the main script
asyncio.run(main())