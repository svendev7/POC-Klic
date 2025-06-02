#!/usr/bin/env python
"""
UI Element Inspector Tool

This script helps identify UI elements in your application.
It provides both pywinauto and WinAppDriver approaches.

Usage:
    python inspect_elements.py --method pywinauto --app "path_to_app_or_window_title"
    python inspect_elements.py --method winappdriver --app "path_to_app"
"""

import argparse
import time
import os
import sys
import json
from pprint import pprint

def inspect_using_pywinauto(app_path_or_title, connect_method="start"):
    """
    Inspect UI elements using pywinauto.
    
    Args:
        app_path_or_title: Path to the executable or window title
        connect_method: 'start' to launch the app or 'connect' to connect to running app
    """
    try:
        from pywinauto import Application
        
        # Connect to or start the application
        if connect_method == "start":
            print(f"Starting application: {app_path_or_title}")
            app = Application(backend="uia").start(app_path_or_title)
        else:
            print(f"Connecting to application with title containing: {app_path_or_title}")
            app = Application(backend="uia").connect(title_re=f".*{app_path_or_title}.*")
        
        # Wait for the application to initialize
        time.sleep(2)
        
        # Get the top window
        main_window = app.top_window()
        
        print("\n===== MAIN WINDOW PROPERTIES =====")
        print(f"Window title: {main_window.window_text()}")
        print(f"Window class: {main_window.class_name()}")
        
        print("\n===== CONTROL IDENTIFIERS =====")
        main_window.print_control_identifiers()
        
        print("\n===== INTERACTIVE MODE =====")
        print("You can now interactively inspect elements.")
        print("The 'app' and 'main_window' variables are available.")
        print("Type 'exit()' or press Ctrl+D to exit.")
        
        # Save a reference to the app and main_window for interactive use
        globals()["app"] = app
        globals()["main_window"] = main_window
        
        # Enter interactive mode if running in terminal
        if os.isatty(sys.stdin.fileno()):
            import code
            code.interact(local=dict(globals(), **locals()))
        
    except ImportError:
        print("pywinauto not installed. Run: pip install pywinauto")
    except Exception as e:
        print(f"Error: {e}")

def inspect_using_winappdriver(app_path):
    """
    Inspect UI elements using WinAppDriver.
    Note: WinAppDriver must be running.
    
    Args:
        app_path: Path to the executable
    """
    try:
        from appium import webdriver
        from selenium.webdriver.common.by import By
        
        # WinAppDriver capabilities
        desired_caps = {}
        desired_caps["app"] = app_path
        desired_caps["platformName"] = "Windows"
        desired_caps["deviceName"] = "WindowsPC"
        
        print("Connecting to WinAppDriver (make sure it's running)...")
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps
        )
        
        # Wait for the application to initialize
        driver.implicitly_wait(10)
        
        print("\n===== WINDOW HANDLE =====")
        print(f"Window handle: {driver.current_window_handle}")
        
        print("\n===== UI HIERARCHY =====")
        # Get page source (XML representation of UI hierarchy)
        page_source = driver.page_source
        print(page_source)
        
        print("\n===== INTERACTIVE MODE =====")
        print("You can now interactively inspect elements.")
        print("The 'driver' variable is available.")
        print("Examples:")
        print("  element = driver.find_element(By.XPATH, '//Button')")
        print("  print(element.get_attribute('AutomationId'))")
        print("Type 'exit()' or press Ctrl+D to exit.")
        
        # Save a reference to the driver for interactive use
        globals()["driver"] = driver
        globals()["By"] = By
        
        # Enter interactive mode if running in terminal
        if os.isatty(sys.stdin.fileno()):
            import code
            code.interact(local=dict(globals(), **locals()))
            
        # Clean up
        driver.quit()
        
    except ImportError:
        print("Appium-Python-Client not installed. Run: pip install Appium-Python-Client")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="UI Element Inspector Tool")
    parser.add_argument("--method", choices=["pywinauto", "winappdriver"], required=True,
                       help="Inspection method to use")
    parser.add_argument("--app", required=True,
                       help="Application path or window title")
    parser.add_argument("--connect", action="store_true",
                       help="Connect to running app instead of starting it (pywinauto only)")
    
    args = parser.parse_args()
    
    if args.method == "pywinauto":
        connect_method = "connect" if args.connect else "start"
        inspect_using_pywinauto(args.app, connect_method)
    elif args.method == "winappdriver":
        inspect_using_winappdriver(args.app)

if __name__ == "__main__":
    main() 