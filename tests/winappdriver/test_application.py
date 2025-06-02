import os
import time
import unittest
import pytest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import cv2
import numpy as np
from PIL import Image

class TestKLICApplicationWinAppDriver(unittest.TestCase):
    """Tests for the KLIC application using WinAppDriver."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test class by connecting to the application."""
        # WinAppDriver capabilities
        desired_caps = {}
        desired_caps["app"] = r"C:\Path\To\Your\Application.exe"  # Replace with actual path
        desired_caps["platformName"] = "Windows"
        desired_caps["deviceName"] = "WindowsPC"
        
        # Connect to WinAppDriver (make sure it's running on port 4723)
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps
        )
        
        # Wait for app to launch
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are done."""
        if cls.driver:
            cls.driver.quit()
    
    def test_01_title_bar_controls(self):
        """Test 1: Testing the title bar (minimize and close buttons)."""
        # Get the main window handle
        window_handle = self.driver.current_window_handle
        
        # Find minimize button using accessibility id
        minimize_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='MinimizeButton']")
        minimize_button.click()
        time.sleep(1)  # Allow time for minimize animation
        
        # Restore the window
        self.driver.switch_to.window(window_handle)
        time.sleep(1)
        
        # Check if window is visible (we're able to interact with it)
        try:
            self.driver.find_element(By.XPATH, "//Window")
            window_visible = True
        except NoSuchElementException:
            window_visible = False
        
        self.assertTrue(window_visible, "Window did not restore properly")
        
        # Check version information in the title bar
        title_element = self.driver.find_element(By.XPATH, "//Window/TitleBar")
        title_text = title_element.text
        self.assertIn("Version", title_text, "Version information not found in title bar")
        
        # Don't test close button as it would end the test prematurely
        # Just verify it exists
        close_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='CloseButton']")
        self.assertTrue(close_button.is_displayed(), "Close button not found")
    
    def test_02_klic_url_input(self):
        """Test 2: Testing URL input for KLIC notifications."""
        # Navigate to URL input screen
        url_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='UrlInputButton']")
        url_button.click()
        
        # Locate URL input field
        url_input = self.driver.find_element(By.XPATH, "//Edit[@AutomationId='UrlInputField']")
        
        # Test valid URL
        valid_url = "https://example.klic.nl/valid-notification"
        url_input.clear()
        url_input.send_keys(valid_url)
        
        # Click submit button
        submit_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='SubmitUrlButton']")
        submit_button.click()
        
        # Wait for and check success message
        wait = WebDriverWait(self.driver, 10)
        success_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='SuccessMessage']")
        ))
        self.assertTrue(success_message.is_displayed(), "Success message not displayed for valid URL")
        
        # Test invalid URL
        url_input.clear()
        url_input.send_keys("invalid-url")
        submit_button.click()
        
        # Wait for and check error message
        error_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='ErrorMessage']")
        ))
        self.assertTrue(error_message.is_displayed(), "Error message not displayed for invalid URL")
    
    def test_03_zip_file_import(self):
        """Test 3: Testing zip file import for KLIC notifications."""
        # Navigate to zip import screen
        zip_import_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='ZipImportButton']")
        zip_import_button.click()
        
        # Locate file selection button
        file_select_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='FileSelectButton']")
        file_select_button.click()
        
        # In the file dialog, enter valid zip path
        # Note: This is a simplified approach; handling file dialogs in WinAppDriver can be complex
        time.sleep(1)  # Wait for dialog to appear
        file_path_input = self.driver.find_element(By.XPATH, "//Edit[@AutomationId='1148']")  # Common file dialog edit field
        
        valid_zip_path = r"C:\Path\To\Valid\KlicFile.zip"
        file_path_input.send_keys(valid_zip_path)
        
        # Click Open button
        open_button = self.driver.find_element(By.XPATH, "//Button[@Name='Open']")
        open_button.click()
        
        # Wait for and check success message
        wait = WebDriverWait(self.driver, 10)
        success_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='ImportSuccessMessage']")
        ))
        self.assertTrue(success_message.is_displayed(), "Success message not displayed for valid zip import")
        
        # Test invalid zip file
        file_select_button.click()
        time.sleep(1)
        file_path_input = self.driver.find_element(By.XPATH, "//Edit[@AutomationId='1148']")
        
        invalid_zip_path = r"C:\Path\To\Invalid\File.txt"
        file_path_input.send_keys(invalid_zip_path)
        open_button = self.driver.find_element(By.XPATH, "//Button[@Name='Open']")
        open_button.click()
        
        # Wait for and check error message
        error_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='ImportErrorMessage']")
        ))
        self.assertTrue(error_message.is_displayed(), "Error message not displayed for invalid zip import")
    
    def test_04_screenshot_comparison(self):
        """Test 4: Comparing screenshots with reference images."""
        # Navigate to an existing notification screen
        notification_view_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='ViewNotificationButton']")
        notification_view_button.click()
        
        # Take screenshot of the current view
        self.driver.get_screenshot_as_file("current_notification_wd.png")
        
        # Compare with reference image
        reference_image_path = "reference_notification_wd.png"
        
        # Simple image comparison using OpenCV
        if os.path.exists(reference_image_path):
            current_img = cv2.imread("current_notification_wd.png")
            reference_img = cv2.imread(reference_image_path)
            
            # Convert images to same size if needed
            reference_img = cv2.resize(reference_img, (current_img.shape[1], current_img.shape[0]))
            
            # Calculate difference
            difference = cv2.absdiff(current_img, reference_img)
            difference_percentage = (np.sum(difference) / (current_img.shape[0] * current_img.shape[1] * current_img.shape[2] * 255)) * 100
            
            # If difference is less than 5%, consider images similar
            self.assertLess(difference_percentage, 5, f"Screenshots differ by {difference_percentage:.2f}%")
        else:
            self.skipTest("Reference image not found")
    
    def test_05_navigation_buttons(self):
        """Test 5: Testing navigation buttons."""
        # Test home button
        home_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='HomeButton']")
        home_button.click()
        
        # Verify home screen is loaded
        wait = WebDriverWait(self.driver, 10)
        home_screen_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='HomeScreenIndicator']")
        ))
        self.assertTrue(home_screen_element.is_displayed(), "Home screen not loaded")
        
        # Test settings button
        settings_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='SettingsButton']")
        settings_button.click()
        
        # Verify settings screen is loaded
        settings_screen_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='SettingsScreenIndicator']")
        ))
        self.assertTrue(settings_screen_element.is_displayed(), "Settings screen not loaded")
        
        # Test back button
        back_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='BackButton']")
        back_button.click()
        
        # Verify we returned to home screen
        home_screen_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='HomeScreenIndicator']")
        ))
        self.assertTrue(home_screen_element.is_displayed(), "Back button did not return to previous screen")
        
        # Test any other navigation buttons as needed
        notifications_button = self.driver.find_element(By.XPATH, "//Button[@AutomationId='NotificationsButton']")
        notifications_button.click()
        
        # Verify notifications screen is loaded
        notifications_screen_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//Text[@AutomationId='NotificationsScreenIndicator']")
        ))
        self.assertTrue(notifications_screen_element.is_displayed(), "Notifications screen not loaded")


if __name__ == "__main__":
    # This allows running the tests directly from this file
    unittest.main() 