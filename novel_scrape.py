"""

NOTE: TEST TRANSLATION NOVEL (Academy's Undercover Professor) lol
  link = https://booktoki468.com/novel/6219?book=일반소설

"""


# Imports
import asyncio
import sys
import os
import configparser
from src.gui.windows_app import NovelScrapeGuiWindow
from PySide6.QtWidgets import QApplication


if (__name__ == "__main__"):
  # Print some whitespace before starting
  print()

  # Load config
  CONFIG_FILE_PATH: str = "cfg/config.ini"
  config = configparser.ConfigParser()
  config.read(CONFIG_FILE_PATH)

  # Setup default output directory if not already
  OUTPUT_DIRECTORY_ROOT: str = config.get("General", "novel_save_directory").strip('"')
  os.makedirs(OUTPUT_DIRECTORY_ROOT, exist_ok=True)

  app = QApplication(sys.argv)
  window = NovelScrapeGuiWindow(config)
  window.show()
  sys.exit(app.exec())
