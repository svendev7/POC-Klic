#!/usr/bin/env python
"""
Debug script to see what elements are available in the KLIC-viewer
"""

from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError

def inspect_elements():
    try:
        # Connect to KLIC-viewer
        print("Connecting to KLIC-viewer...")
        app = Application(backend="uia").connect(title="Kadaster KLIC-viewer")
        main_window = app.window(title="Kadaster KLIC-viewer")
        
        print("✓ Connected successfully!")
        print(f"Window title: {main_window.window_text()}")
        
        # Print all control identifiers with more depth
        print("\n=== CONTROL IDENTIFIERS (Depth 5) ===")
        main_window.print_control_identifiers(depth=5)
        
        # Try to find specific elements
        print("\n=== SEARCHING FOR SPECIFIC ELEMENTS ===")
        
        target_elements = [
            "download-veld",
            "select-folder", 
            "navMeer",
            "giaToggle",
            "panelHeadingSluitenKnop", 
            "openAndereLevering"
        ]
        
        for element_id in target_elements:
            try:
                element = main_window.child_window(auto_id=element_id)
                if element.exists():
                    print(f"✓ Found: {element_id}")
                    print(f"  Control type: {element.element_info.control_type}")
                    print(f"  Is visible: {element.is_visible()}")
                    print(f"  Is enabled: {element.is_enabled()}")
                else:
                    print(f"✗ Not found: {element_id}")
            except Exception as e:
                print(f"✗ Error finding {element_id}: {e}")
        
        print("\n=== ALL CHILD ELEMENTS ===")
        try:
            children = main_window.children()
            print(f"Found {len(children)} child elements:")
            for i, child in enumerate(children[:10]):  # Show first 10
                try:
                    auto_id = child.automation_id()
                    control_type = child.element_info.control_type
                    name = child.window_text()
                    print(f"  {i+1}. AutomationId: '{auto_id}', Type: {control_type}, Name: '{name}'")
                except Exception as e:
                    print(f"  {i+1}. Error getting info: {e}")
                    
        except Exception as e:
            print(f"Error getting children: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_elements() 