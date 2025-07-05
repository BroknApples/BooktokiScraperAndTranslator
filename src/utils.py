# Imports
import importlib
import subprocess
import sys
import os

# === Constants ===
INT_MAX: int = sys.maxsize
INT_MIN: int = -sys.maxsize - 1

# === Function: ensureModuleInstalled ===
def ensureModuleInstalled(module_name, package_name=None):
  """
  Check if some module is installed on the system

  Params:
    module_name: Name of the module
    package_name: Custom install package (only use if its different from the module_name)
  """

  try:
    importlib.import_module(module_name)
  except ImportError:
    print(f"Module '{module_name}' not found.")
          
    # Prompt user if they wish to install the module
    choice = input(f"Do you want to install '{package_name or module_name}'? (y/n): ")
    if choice.lower() != 'y':
      print(f"Cannot proceed without '{module_name}'")
      sys.exit(1)

    # Attempt to install the missing module
    try:
      subprocess.check_call([sys.executable, "-m", "pip", "install", package_name or module_name])
    except subprocess.CalledProcessError:
      print(f"Failed to install '{package_name or module_name}'. Please install it manually.")
      sys.exit(1)
    
    # Try import again after install
    try:
      importlib.import_module(module_name)
    except ImportError:
      print(f"Module '{module_name}' is still not importable after installation. Cannot proceed.")
      sys.exit(1)

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