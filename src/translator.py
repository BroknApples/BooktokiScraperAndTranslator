# Imports
import asyncio
from deep_translator import GoogleTranslator
from src.utils import printModuleSeparator

# NOTE: TEST TRANSLATION TEXT:
# translator = TextTranslator()
# untranslated_text: str = "아카데미 에위장취업당했다-277화"
# translated_text: str = translator.translateString(untranslated_text)
# print("The translated text is: " + translated_text)

class TextTranslator():
  """
  A class that allows you to translate strings or an array of string to another language
  """
  

  # ******************************************** #
  # ****************** Private ***************** #
  # ******************************************** #

  # === Constants ===
  _CHUNK_SIZE: int = 1250 # How many characters can be in one string when calling googletranslate's translate function

  # === Variables ===
  _translator: GoogleTranslator = None
  _src_lang: str
  _dest_lang: str

  def _translateStringInternal(self, text: str) -> str:
    """
    Does the actual work of translating a string

    Params:
      text: The string to translate
    
    Returns:
      str: The translated text
    """
    
    # If the string is short enough, there is no need to chunkate it.
    # Just simply translate the string directly
    if (len(text) <= self._CHUNK_SIZE):
      return self._translateInternal(text)

    # Chunkate text
    chunkated_text: list[str] = self._chunkateString(text)

    # Translate each chunk
    translated_chunks: list[str] = []
    for text_chunk in chunkated_text:
      translated_text = self._translateInternal(text_chunk)
      translated_chunks += translated_text
    
    # Return the translated string
    return "".join(translated_chunks)  

  # === Function: _translateInternal ===
  def _translateInternal(self, text: str) -> str:
    """
    Do the actual translation for a string

    Params:
      text: String to translate
      src_lang: Language to translate FROM
      dest_lang: Language to translate TO
    
    Returns:
      str: Translated version of the string
    """

    # Await the translation
    translated_text = self._translator.translate(text, src=self.getSourceLanguage(), dest=self.getDestinationLanguage())

    # Properly return the text property of the translation
    return translated_text

  # === Function: _chunkateString ===
  def _chunkateString(self, text: str) -> list:
    """
    Splits a string into chunks of a specific size

    Params:
      text: Text to chunkate
    
    Returns:
      list: Chunk list of the original string
    """

    # Log message
    print("Splitting strings into chunks...")
    
    # Length of the text
    TEXT_LENGTH: int = len(text)

    # Return this value
    chunks: list[str] = []

    # Do the chunking
    for i in range(0, TEXT_LENGTH, self._CHUNK_SIZE):
      chunks.append(text[i:i + self._CHUNK_SIZE])
    
    return chunks

  # === Function: _initializeTranslator ===
  def _initializeTranslator(self) -> None:
    """
    Initialize the google translator class object
    """
    
    self._translator = GoogleTranslator(source=self.getSourceLanguage(), target=self.getDestinationLanguage())

  # ******************************************** #
  # ****************** Public ****************** #
  # ******************************************** #

  # === Subclass: Languages ===
  class Languages():
    """
    Defines language string constants
    """
    
    # === Constants ===
    AUTO_DETECT: str = "auto"
    KOREAN: str = "ko"
    ENGLISH: str = "en"
    JAPANESE: str = "jp"

  # === Function: __init__ ===
  def __init__(self, src_lang: str = Languages.AUTO_DETECT, dest_lang: str= Languages.ENGLISH):
    """
    Constructor -> Create an instance with a src and dest language already set (Default is AUTO_DETECT -> English)

    Params:
      src_lang: Language you wish to translate FROM
      dest_lang: Language you wish to translate TO
    """

    self.setSourceLanguage(src_lang)
    self.setDestinationLanguage(dest_lang)

  # === Function: translateString ===
  def translateString(self, text: str, src_lang: str = None, dest_lang: str = None) -> str | None:
    """
    Translate a string from some language to another

    Params:
      text: Text you want to translate
      src_lang: Language you wish to translate FROM | Default = None (Instead, it will use the one set in the TextTranslator object)
      dest_lang: Language you wish to translate TO | Default = None (Instead, it will use the one set in the TextTranslator object)
    
    Returns:
      str | None: Translated text | None if an Error occurred
    """

    # Log the translation's start
    printModuleSeparator()
    print("Starting Translation...\n")

    # Set source and dest lang
    self.setSourceLanguage(src_lang)
    self.setDestinationLanguage(dest_lang)
    
     # If the src lang is None, then set to auto
    if (self.getSourceLanguage() == None):
      self.setSourceLanguage(TextTranslator.Languages.AUTO_DETECT)
    # If dest lang is None, then cannot proceed, so return None
    if (self.getDestinationLanguage() == None):
      return None

    # Initialize the translator
    self._initializeTranslator()

    # Print log message
    print(f"Translating string...")

    # Translate the text
    translated_text: str = self._translateStringInternal(text)

    # Log the translation's completion
    print("\nTranslation Complete!")
    printModuleSeparator()

    # Return a single string instead of the chunks
    return translated_text
    
  # === Function: translateStringArray ===
  def translateStringArray(self, text_array: list[str], src_lang: str = None, dest_lang: str = None) -> list[str] | None:
    """
    Translate an array of strings from some language to another

    Params:
      text_array: Array of text you want to translate
      src_lang: Language you wish to translate FROM | Default = None (Instead, it will use the one set in the TextTranslator object)
      dest_lang: Language you wish to translate TO | Default = None (Instead, it will use the one set in the TextTranslator object)
    
    Returns:
      list[str] | None: Translated text array | None if an Error occurred
    """

    # Log the translation's start
    printModuleSeparator()
    print("Starting Translation...\n")

    # Set source and dest lang
    self.setSourceLanguage(src_lang)
    self.setDestinationLanguage(dest_lang)
    
     # If the src lang is None, then set to auto
    if (self.getSourceLanguage() == None):
      self.setSourceLanguage(TextTranslator.Languages.AUTO_DETECT)
    # If dest lang is None, then cannot proceed, so return None
    if (self.getDestinationLanguage() == None):
      return None

    # Initialize the translator
    self._initializeTranslator()

    # Length of the array    
    ARRAY_LENGTH: int = len(text_array)

    # The final translated version of the array | Fill array with empty slots
    translated_array: list[str] = [None] * ARRAY_LENGTH

    # Translate each index of the array
    for i in range(ARRAY_LENGTH):
      # Print log message
      print(f"Translating array[{i}]...")

      # Get the text at this index
      translated_text: str = self._translateStringInternal(text_array[i])
      
      # Set the translated text in the array
      translated_array[i] = translated_text

    # Log the translation's completion
    print("\nTranslation Complete!")
    printModuleSeparator()

    # Return the translated array
    return translated_array


  # ******************************************** #
  # ************** Getters/Setters ************* #
  # ******************************************** #

  # === Function: setSourceLanguage ===
  def setSourceLanguage(self, value: str | None) -> None:
    """
    Set the language you wish to translate FROM

    Params:
      value: New source language
    """

    if (value != None):
     self._src_lang = value

  # === Function: getSourceLanguage ===
  def getSourceLanguage(self) -> str:
    """
    Get the language this translator will translate FROM

    Returns:
      str: Which language is the source language
    """

    return self._src_lang

  # === Function: setDestinationLanguage ===
  def setDestinationLanguage(self, value: str | None) -> None:
    """
    Set the language you wish to translate TO

    Params:
      value: New destination language
    """

    if (value != None):
      self._dest_lang = value

  # === Function: getDestinationLanguage ===
  def getDestinationLanguage(self) -> str:
    """
    Get the language this translator will translate TO

    Returns:
      str: Which language is the destination language
    """

    return self._dest_lang  