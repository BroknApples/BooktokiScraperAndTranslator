# TODO: Try deep-translator for translation when done

import asyncio
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from googletrans import Translator
import re
import os

KOREAN = 'ko'
ENGLISH = 'en'

SEPERATOR = "*******************************"
CHUNK_SIZE = 1250 ## Size of the character chunks

## Returns the URL to the initial chapter to scrape
def getInitialChapterUrl(url: str, chapter_num: int) -> str:
  print(f"Starting scrape on chapter {chapter_num}:\n")
  
  # Open web novel chapter list page
  driver.uc_open_with_reconnect(url, reconnect_time=6)
  driver.uc_gui_click_captcha()
  
  chapter_element = driver.find_element(By.XPATH, f'//*[@data-index="{chapter_num}"]') # Finds the chapter on the novel description page
  
  html_content = chapter_element.get_attribute("innerHTML")
  match = re.search(r'href="(.*?)"', html_content)
  if match: # Starting chapter has been opened
    return match.group(1)

def findNextChapterUrl() -> str:
  next_chapter_link = driver.find_element("class name", "btn-resource.btn-next.at-tip") # Gets the link attached to the next chapter button
  
  html_content = next_chapter_link.get_attribute("innerHTML")
  match = re.search(r'href="(.*?)"', html_content)
  if match: # Chapter is found
    return match.group(1)
  else:
    return "None"

# Function to scrape data
def scrapeChapterUrl(url: str, target_id: str, chapter_num: int) -> any:
  print(f"Scraping Chapter {chapter_num} URL...")
  
  driver.uc_open_with_reconnect(url, reconnect_time=6)
  driver.uc_gui_click_captcha()
  
  try:
    element = driver.find_element("id", target_id)
    return element.text
  except Exception as e:
    print(f"Error: {e}")
    return None

# Splits a string into chunks of a specific size
def splitString(text: str) -> list:
  print("Splitting strings...")
  return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

# Translate from Korean to English (making it async)
async def translate(text: str, initial_lang: str, target_lang: str, str_num: int) -> str:
  if str_num > 0:
    print(f"Translating chunk #{str_num}...")
  async with Translator() as translator:
    translated_text = await translator.translate(text, src=initial_lang, dest=target_lang)
    return translated_text.text  # Access the translated text property

# Translate each individual chunk
async def translateChunks(chunks: list) -> list:
  print(f"Translating {len(chunks)} Chunks...")
  translated_chunks = []
  i = 1
  for chunk in chunks:
    translated = await translate(chunk, KOREAN, ENGLISH, i)  # translate the chunk
    translated_chunks.append(translated)
    i += 1
  return " ".join(translated_chunks)  # Combine the translated chunks

def main() -> None:
  html_id = "novel_content" # Modify to change what element is being scraped
  url = input("Enter novel URL: ")
  
  start_idx = "Uninitialized"
  while not start_idx.isdigit() and start_idx != "":
    start_idx = ""
    start_idx = input("Enter the starting chapter(Press ENTER for Chapter 1): ")
  if start_idx == "":
    start_idx = "1"
  
  end_idx = "Uninitialized"
  while not end_idx.isdigit() and end_idx != "":
    end_idx = ""
    end_idx = input("Enter the ending chapter(Press ENTER for the Latest Chapter): ")
  if end_idx == "":
    end_idx = "2147000000"
    
  output_file = input("Enter a name for your file(Press ENTER for Default value 'BooktokiNovelScrape'): ")
  if output_file == "":
    output_file = "BooktokiNovelScrape"
  
  # Comment to allow appending to already created files
  append = 0
  while os.path.exists("output/" + output_file + ".txt"):
    output_file += str(append)
    append += 1
  
  global driver
  driver = Driver(uc=True, headless=False)
  
  curr_url = getInitialChapterUrl(url, start_idx)
  for chapter_num in range (int(start_idx), int(end_idx)):
    korean_text = scrapeChapterUrl(curr_url, html_id, chapter_num)
    korean_text = korean_text.replace('…', '...')
    split_text = splitString(korean_text)
    english_text = asyncio.run(translateChunks(split_text))
    english_text = english_text.replace('\n', '\n\n')
    with open("output/" + output_file + ".txt", "a", encoding="utf-8") as file:
      file.write("\n\n" + SEPERATOR + " Chapter " + str(chapter_num) + " " + SEPERATOR + "\n\n")
      file.write(english_text)
      
    curr_url = findNextChapterUrl()
    
    # No next chapter found
    if (curr_url == "None"): break

  # Cleanup
  driver.quit()

main()

# This should probably get reformatted, but it works; Sooooo...