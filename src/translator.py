# Imports
import asyncio
from googletrans import Translator


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
  _translator: Translator = Translator()
  _src_lang: str
  _dest_lang: str

  # === Function: _translateInternal ===
  def _translateInternal(self, text: str, src_lang: str, dest_lang: str) -> str:
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
    translated_text = self._translator.translate(text, src=src_lang, dest=dest_lang)

    # Properly return the text property of the translation
    return translated_text.text

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


  # ******************************************** #
  # ****************** Public ****************** #
  # ******************************************** #

  # === Subclass: Languages ===
  class Languages():
    """
    Defines language string constants
    """
    
    # === Constants ===
    KOREAN: str = "ko"
    ENGLISH: str = "en"

  # === Function: __init__ ===
  def __init__(self, src_lang: str = Languages.KOREAN, dest_lang: str= Languages.ENGLISH):
    """
    Constructor -> Create an instance with a src and dest language already set (Default is Korean -> English)

    Params:
      src_lang: Language you wish to translate FROM
      dest_lang: Language you wish to translate TO
    """
    self.setSourceLanguage(src_lang)
    self.setDestinationLanguage(dest_lang)

  # === Function: translateString ===
  def translateString(self, text: str, src_lang: str = None, dest_lang: str = None) -> str:
    """
    Translate a string from some language to another

    Params:
      text: Text you want to translate
      src_lang: Language you wish to translate FROM | Default = None (Instead, it will use the one set in the TextTranslator object)
      dest_lang: Language you wish to translate TO | Default = None (Instead, it will use the one set in the TextTranslator object)
    
    Returns:
      str: Translated text
    """

    # If the default params are used, apply private variables in their place
    if (src_lang == None):
      # NOTE: If src lang is default, then dest lang is automatically default

      # TODO: Somehow check if the src/dest lang is set in the class, if not, catch some error
      src_lang = self.getSourceLanguage()
      dest_lang = self.getDestinationLanguage()
    elif (dest_lang == None):
      dest_lang = self.getDestinationLanguage()
    
    # Print log message
    print(f"Translating string...")

    # If the string is short enough, there is no need to chunkate it.
    # Just simply translate the string directly
    if (len(text) <= self._CHUNK_SIZE):
      return self._translateInternal(text, src_lang, dest_lang)

    # Chunkate text
    chunkated_text: list[str] = self._chunkateString(text)

    # Translate each chunk
    translated_chunks: list[str] = []
    for text_chunk in chunkated_text:
      translated_text = self._translateInternal(text_chunk, src_lang, dest_lang)
      translated_chunks.append(translated_text)

    # Return a single string instead of the chunks
    return "".join(translated_chunks)  
    
  # === Function: translateStringArray ===
  def translateStringArray(self, text_array: list[str], src_lang: str = None, dest_lang: str = None) -> list[str]:
    """
    Translate an array of strings from some language to another

    Params:
      text_array: Array of text you want to translate
      src_lang: Language you wish to translate FROM | Default = None (Instead, it will use the one set in the TextTranslator object)
      dest_lang: Language you wish to translate TO | Default = None (Instead, it will use the one set in the TextTranslator object)
    
    Returns:
      list[str]: Translated text array
    """

    # If the default params are used, apply private variables in their place
    if (src_lang == None):
      # NOTE: If src lang is default, then dest lang is automatically default

      # TODO: Somehow check if the src/dest lang is set in the class, if not, catch some error
      src_lang = self.getSourceLanguage()
      dest_lang = self.getDestinationLanguage()
    elif (dest_lang == None):
      dest_lang = self.getDestinationLanguage()
    
    # The final translated version of the array
    translated_array: list[str] = []

    # Translate each index of the array
    ARRAY_LENGTH: int = len(text_array)
    for i in range(0, ARRAY_LENGTH):
      # Print log message
      print(f"Translating array[{i}]...")

      # Get the text at this index
      text: str = text_array[i]

      # If the string is short enough, there is no need to chunkate it.
      # Just simply translate the string directly
      if (len(text) <= self._CHUNK_SIZE):
        translated_array[i] = self._translateInternal(text, src_lang, dest_lang)

      # Chunkate text
      chunkated_text: list[str] = self._chunkateString(text)

      # Translate each chunk
      translated_chunks: str = ""
      for text_chunk in chunkated_text:
        translated_text = self._translateInternal(text_chunk, src_lang, dest_lang)
        translated_chunks.append(translated_text)

      # Create a single string instead of chunks
      translated_array[i] = "".join(translated_chunks)

    # Return the translated array
    return translated_array


  # ******************************************** #
  # ************** Getters/Setters ************* #
  # ******************************************** #

  # === Function: setSourceLanguage ===
  def setSourceLanguage(self, value: str) -> None:
    """
    Set the language you wish to translate FROM

    Params:
      value: New source language
    """

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
  def setDestinationLanguage(self, value: str) -> None:
    """
    Set the language you wish to translate TO

    Params:
      value: New destination language
    """

    self._dest_lang = value

  # === Function: getDestinationLanguage ===
  def getDestinationLanguage(self) -> str:
    """
    Get the language this translator will translate TO

    Returns:
      str: Which language is the destination language
    """

    return self._dest_lang  