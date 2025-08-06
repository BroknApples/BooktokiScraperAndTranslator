# Imports
import sys
import os
import configparser


# === Class: OperatingSystems ===
class OperatingSystems():
  """
  Defines constants for different operating systems.
  """
  
  # === Constants ===
  WINDOWS: str = "win32"
  LINUX: str = "linux"
  MACOS: str = "darwin"


# === Class: Limits ===
class Limits():
  """
  Defines the maximum sizes of variable types in python, mainly numbers.
  """
  
  # === Constants ===
  INT_MAX: int = sys.maxsize
  INT_MIN: int = -sys.maxsize - 1


# NOTE: Commented out since it's kinda useless; this only saves 1 line of work.
# # === Function: loadConfigFile ===
# def loadConfigFile(filename: str) -> configparser.ConfigParser:
#   """
#   Read a config file into a ConfigParser object

#   Params:
#     filename: Name of the config file to read
  
#   Returns:
#     configparser.ConfigParser: Object used for config file parsing
#   """

#   config = configparser.ConfigParser()
#   return config.read(filename)


# === Function: splitRangeIntoChunks ===
def splitRangeIntoChunks(start: int, end: int, chunk_count: int) -> list[tuple[int]]:
  """
  Given a start, end, and chunk_count, create a list that defines each range of numbers

  Params:
    start: Starting number
    end: Ending number
    chunk_count: How many ways should this range be split by

  Returns:
    list[tuple[int]]: Correct ranges for each block
  """
  
  # Get the total size and the base chunk size (doesn't include the leftover odd digits)
  total: int = end - start + 1
  base_chunk: int = total // chunk_count
  remainder: int = total % chunk_count

  ranges: list[int] = [] * chunk_count
  current_starting_num = start

  for i in range(chunk_count):
    # Add one if the the current index is lower than the amount of indexes that should get a remainder
    chunk_size: int = base_chunk + (1 if i < remainder else 0)

    # Set start and end values
    start_val: int = current_starting_num
    end_val = current_starting_num + chunk_size - 1

    # Add values to the list as a tuple
    ranges.append((start, end))

    # Set new range's starting value
    current_starting_num = end + 1

  # Return properly created list
  return ranges


# === Function: createDirectory ===
def createDirectory(directory_path: str, exist_ok: bool = True) -> bool:
  """
  Attempt to create a directory

  Params:
    directory_path: Path of the directory to create
    exist_ok: The same as exist_ok in 'os.makedirs'

  Returns:
    bool: True/False of creation of the directory

  Raises:
    Exception if 'exist_ok' is False and the path is not valid/already exists
  """

  try:
    os.makedirs(directory_path, exist_ok=exist_ok)

    # If code reaches this point, no error in dir creation
    return True
  except Exception as e:
    print("Invalid output directory name.")
    return False


# === Function: formatNovelText ===
def formatNovelText(text: str) -> str:
  """
  Format a novel chapter's text to be more readable

  Params:
    text: Text to format
  
  Returns:
    str: A formatted version of the original text
  """

  # Replace weird ellipses characters with actual periods
  text = text.replace('…', '...')

  # Replace one newline with 2, for visual seperation
  text = text.replace("\n", "\n\n")

  # Return formatted text
  return text


# === Function: getFileContentsByLine ===
def getFileContentsByLine(filepath: str, remove_newlines: bool = True) -> list[str]:
  """
  Get the contents of a file sorted by each line

  Params:
    filepath: Path to the file to read
    remove_newlines: If this value is True, then newlines willbe removed on each line
  
  Returns:
    list[str]: List containing the contents of a line per index
  """

  # If the file doesn't exist, just return an empty list
  if (not os.path.exists(filepath)):
    return []

  # Create return value
  lines: list[str] = ""

  # Read file
  with open(filepath, "r") as file:
    # Get contents of the lines
    lines = file.readlines()
  
  # Strip newline characters from each line. They are kinda redundant since
  # they are obviously a newline. If you want to write back to the file, you
  # know a line needs newlines anyways
  if (remove_newlines):
    lines = [line.strip("\n") for line in lines]

  return lines


# === Function: filerKeysFromSet ===
def filterKeysFromSet(set, exclude_list: list) -> list:
  """
  Given some set of values, remove values that are in the exclude_list

  Params:
    set: Set to get a filtered set from
    exclude_list: List of values to exclude
  """

  return [v for v in set if v not in exclude_list]

# === Function: printModuleSeparator ===
def printModuleSeparator() -> None:
  """
  Print a sepator that is useful when looking at the terminal's print history when debugging
  """

  print("\n*********************************************************\n")


# NOTE: This is how a docstring should look
"""
Explain funtion purpose here.

Args:
  arg1: The first argument.
  arg2: The second argument.

Returns:
  Nothing.
"""