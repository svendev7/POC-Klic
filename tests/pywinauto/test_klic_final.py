import time
import pytest
import sys
import pyperclip
from pywinauto import Application
from pywinauto.keyboard import send_keys

class TestKLIC:
    
    @pytest.fixture(scope="class")
    def app_connection(self):
        print("5 seconden wachten - start nu de KLIC-viewer...")
        time.sleep(5)
        
        possible_titles = ["Kadaster KLIC-viewer", "KLIC-viewer", "Kadaster KLIC viewer"]
        
        app = None
        main_window = None
        
        for title in possible_titles:
            try:
                app = Application(backend="uia").connect(title=title)
                main_window = app.window(title=title)
                main_window.exists()
                break
            except:
                continue
        
        if not app:
            app = Application(backend="uia").connect(path="Kadaster KLIC-viewer.exe")
            main_window = app.top_window()
        
        yield app, main_window
        
    def find_any_element(self, main_window, auto_id=None, name=None):
        try:
            all_elements = main_window.descendants()
            
            for elem in all_elements:
                try:
                    elem_auto_id = elem.automation_id()
                    elem_name = elem.window_text()
                    elem_type = str(type(elem))
                    
                    legacy_name = ""
                    try:
                        legacy_name = elem.legacy_properties().get('Name', '')
                    except:
                        pass
                    
                    if 'StaticWrapper' in elem_type:
                        continue
                    
                    if not (hasattr(elem, 'click') or hasattr(elem, 'select') or hasattr(elem, 'invoke')):
                        continue
                        
                    if auto_id and elem_auto_id == auto_id:
                        return elem
                        
                    if name and (elem_name == name or legacy_name == name):
                        return elem
                        
                except:
                    continue
                    
            return None
                
        except:
            return None
    
    def click_element(self, elem):
        for method_name in ['click', 'select', 'invoke']:
            try:
                if hasattr(elem, method_name):
                    getattr(elem, method_name)()
                    return method_name
            except:
                continue
        return None
        
    def test_1_bestand_import(self, app_connection):
        app, main_window = app_connection
        
        folder_button = self.find_any_element(main_window, auto_id="select-folder", name="Lokale KLIC-levering openen")
        
        if folder_button is None:
            try:
                folder_button = main_window.child_window(auto_id="select-folder").wait('visible', timeout=5)
            except:
                try:
                    folder_button = main_window.child_window(title="Lokale KLIC-levering openen").wait('visible', timeout=5)
                except:
                    assert False, "Folder knop echt niet gevonden!"
        
        method = self.click_element(folder_button)
        assert method is not None, "Folder knop kon niet worden geklikt!"
        time.sleep(2)
        
        pyperclip.copy("25G0042326_1")
        send_keys("^a")
        time.sleep(2)
        send_keys("^v")
        time.sleep(2)
        send_keys("{ENTER}")
        time.sleep(2)
        send_keys("{ENTER}")
        time.sleep(2)
    
    def test_2_navigatie_meer(self, app_connection):
        app, main_window = app_connection
        
        meer_button = self.find_any_element(main_window, auto_id="navMeer", name="Meer")
        assert meer_button is not None, "Meer knop niet gevonden!"
        
        method = self.click_element(meer_button)
        assert method is not None, "Meer knop kon niet worden geklikt!"
        time.sleep(2)
        
        andere_levering_button = self.find_any_element(main_window, auto_id="openAndereLevering", name="Open andere KLIC-levering")
        assert andere_levering_button is not None, "Open andere KLIC-levering knop niet gevonden!"
        
        method = self.click_element(andere_levering_button)
        assert method is not None, "Open andere KLIC-levering knop kon niet worden geklikt!"
        time.sleep(2)
    
    def test_3_url_invoer(self, app_connection):
        app, main_window = app_connection
        
        url_field = self.find_any_element(main_window, auto_id="download-veld")
        assert url_field is not None, "URL veld niet gevonden!"
        
        method = self.click_element(url_field)
        assert method is not None, "URL veld kon niet worden geklikt!"
        time.sleep(2)
        
        pyperclip.copy("https://service10.acceptatie.kadaster.nl/gds2/download/public/454b36da-aa53-48a4-9ab4-b6d632d861bf")
        send_keys("^a")
        time.sleep(2)
        send_keys("^v")
        time.sleep(2)
        send_keys("{ENTER}")
        time.sleep(2)
        send_keys("{ENTER}")
        time.sleep(2)
    
    def test_4_venster_controls(self, app_connection):
        app, main_window = app_connection
        
        try:
            main_window.minimize()
            time.sleep(2)
            
            main_window.restore()
            time.sleep(2)
            
            send_keys("%{F4}")
            time.sleep(2)
            
        except Exception as e:
            try:
                app.kill()
            except:
                pass
            assert False, f"Venster controls faalden: {e}"

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "-s", __file__])) 