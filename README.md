# KLIC Application Test Suite

This project contains automated tests for a KLIC application using both pywinauto and WinAppDriver frameworks.

## Overview

The test suite includes automated tests for the following functionality:

1. **Title Bar Controls**: Testing minimize and close buttons, and verifying version information.
2. **KLIC URL Input**: Testing valid and invalid URL inputs for KLIC notifications.
3. **ZIP File Import**: Testing valid and invalid ZIP file imports for KLIC notifications.
4. **Screenshot Comparison**: Comparing application screens with reference images.
5. **Navigation Controls**: Testing navigation buttons and screen transitions.

## Project Structure

```
PlanningStage/
│
├── tests/
│   ├── pywinauto/                    # pywinauto test scripts
│   │   ├── test_application.py       # pywinauto test cases
│   │   └── SETUP.md                  # Setup guide for pywinauto
│   │
│   ├── winappdriver/                 # WinAppDriver test scripts
│   │   ├── test_application.py       # WinAppDriver test cases
│   │   └── SETUP.md                  # Setup guide for WinAppDriver
│   │
│   ├── inspect_elements.py           # Tool to help identify UI elements
│   └── utils.py                      # Shared utility functions
│
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

## Getting Started

### Prerequisites

- Windows 10 or newer
- Python 3.7 or newer
- The application under test installed on your system
- For WinAppDriver tests: Windows Application Driver installed and running
- Windows SDK with Inspect tool (for identifying UI elements)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd PlanningStage
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. For WinAppDriver tests, follow the setup instructions in `tests/winappdriver/SETUP.md`

### Identifying UI Elements

Before running the tests with your application, you'll need to update the element identifiers in the test scripts. This project includes a tool to help you discover UI elements in your application:

#### Using the Element Inspection Tool

The `inspect_elements.py` script helps identify UI elements using either pywinauto or WinAppDriver:

```
# Using pywinauto to inspect a running application
python tests/inspect_elements.py --method pywinauto --app "Application Title" --connect

# Using pywinauto to launch and inspect an application
python tests/inspect_elements.py --method pywinauto --app "C:\Path\To\Application.exe"

# Using WinAppDriver to inspect an application (WinAppDriver must be running)
python tests/inspect_elements.py --method winappdriver --app "C:\Path\To\Application.exe"
```

The tool will:
1. Connect to or launch your application
2. Display information about the main window
3. Show the control hierarchy with element properties
4. Enter an interactive Python shell where you can inspect elements in real time

This information will help you update the test scripts with the correct element identifiers for your application.

#### Alternative Inspection Methods

1. For pywinauto, use `print_control_identifiers()` directly in your code
2. For WinAppDriver, use the Inspect tool from Windows SDK

The current test scripts use placeholder identifiers that need to be replaced with actual values from your application.

### Running Tests

#### Running pywinauto Tests

```
python -m tests.pywinauto.test_application
```

#### Running WinAppDriver Tests

1. Start WinAppDriver (as Administrator):
   ```
   "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
   ```

2. Run the tests:
   ```
   python -m tests.winappdriver.test_application
   ```

## Customization

1. **Application Path**: Update the application path in both test files to point to your application executable.
2. **Element Identifiers**: Replace placeholder identifiers with actual ones from your application.
3. **Test Data**: Update test data (URLs, file paths, etc.) with values appropriate for your application.
4. **Reference Images**: Create appropriate reference images for screenshot comparison tests.

## Best Practices

1. Run tests in a clean, controlled environment.
2. Ensure the application is in a known state before testing.
3. Add appropriate wait times to account for application response delays.
4. Keep reference screenshots up-to-date with UI changes.
5. Use descriptive test and variable names for better maintainability.