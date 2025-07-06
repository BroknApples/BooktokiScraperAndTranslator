# Imports
import sys
import os

# === Constants ===
INT_MAX: int = sys.maxsize
INT_MIN: int = -sys.maxsize - 1

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