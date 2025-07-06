# Imports
import importlib
import subprocess
import sys
import os


""" Name of this script file """
SETUP_SCRIPT_FILENAME: str = "setup.py"

""" NOTE: Change this to 'False' if you want to run the setup script again"""
already_setup: bool = False

# === Function: setup ===
def setup():
  """
  Sets up the project for usage
  """

  # Check if the program is already set up
  if (already_setup):
    print("Project already set up. Exiting setup script.")

  # Header
  print("**************** NovelScrape Setup ****************")
  print("********      Created by 'BroknApples'       ******")
  print("********   NovelScrape version: 2.0.0 Setup  ******")
  print("***************************************************\n")

  # Ensure the user is ready to setup the project
  response: str = ""
  while (response != 'OK'):
    response = input("STOP. Before proceeding, ensure you have Python 3.12.8 using MSYS2 (Or another valid version) set up. Enter 'OK' to continue: ")
  
  # Ensure the user is really, really, really ready to setup the project
  are_you_sure: str = ""
  while (are_you_sure != 'YES'):
    are_you_sure = input("Are you sure you are ready to setup? Enter 'YES' to continue: ")

  # Log module installing
  print("Starting module installation...")

  # Install required modules
  ensureModuleInstalled("PySide6")
  ensureModuleInstalled("selenium")
  ensureModuleInstalled("seleniumbase")
  ensureModuleInstalled("deep-translator")

  # Log module installing
  print("Module installation complete!")

  setAsAlreadySetup()

  # Footer
  print("\n*************************************************")

# === Function: ensureModuleInstalled ===
def ensureModuleInstalled(module_name: str, module_version: str | None = None):
  """
  Check if some module is installed on the system

  Params:
    module_name: Name of the module
    module_version: The version of the package you wish to install
  """

  print(f"Ensuring required module '{module_name}' is installed.")

  # Check if the module should be installed with a specific version
  if (module_version != None):
    # First check if the correct version is already installed
    try:
      # Get the version of the installed module
      module = importlib.import_module(module_name)
      installed_version = getattr(module, '__version__', None)

      # If the correct version is already installed, just return
      if (installed_version == module_version):
        print("Correct version already installed. Skipping.")
    except ImportError:
      pass

    # Add the module's version to 'module_name'
    module_name += "==" + module_version
    
  try:
    # Import module
    importlib.import_module(module_name)
  except ImportError:
    print(f"Module '{module_name}' not found.")

    # Attempt to install the missing module
    print("Attempting to install module...")
    installModule(module_name)
    
    # Try import again after install
    try:
      importlib.import_module(module_name)
    except ImportError:
      print(f"Module '{module_name}' is still not importable after installation. Cannot proceed.")
      sys.exit(1)

# === Function: installModule ===
def installModule(module_name: str) -> None:
  """
  Install a module, or if not possible, quit the program

  Params:
    module_name: Name of the module to install
  """

  try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name, "--force-reinstall"])
  except subprocess.CalledProcessError:
    print(f"Failed to install '{module_name}'. Please install it manually.")
    sys.exit(1)

def setAsAlreadySetup() -> None:
  # Modify the 'already_setup' variable to mark it as already ran
  with open(SETUP_SCRIPT_FILENAME, "r") as f:
    lines = f.readlines()

  with open(SETUP_SCRIPT_FILENAME, "w") as f:
    for line in lines:
      if (line == "already_setup: bool = False"):
        f.write("already_setup: bool = True")
      else:
        f.write(line)


# Start program
setup()