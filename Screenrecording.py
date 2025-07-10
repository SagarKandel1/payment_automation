import time
import base64
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class SettingsAutomation:
    def __init__(self):
        self.driver = None

    def setup_capabilities(self):
        """Setup Appium capabilities for Android Settings"""
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"  # Replace with your device ID from adb devices
        options.automation_name = "UiAutomator2"
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"
        options.no_reset = True
        return options

    def start_session(self):
        """Start Appium session"""
        try:
            options = self.setup_capabilities()
            self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            print("Settings app opened successfully!")
            return True
        except Exception as e:
            print(f"Failed to start session: {e}")
            return False

    def scroll_down(self):
        """Perform scroll down action"""
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] // 2
            start_y = int(screen_size['height'] * 0.8)
            end_y = int(screen_size['height'] * 0.2)
            self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
        except Exception as e:
            print(f"Scroll failed: {e}")

    def find_system_section(self, max_scrolls=10):
        """Scroll down until System section is found"""
        print("Looking for 'System' section...")
        for scroll_count in range(max_scrolls):
            try:
                system_element = None
                try:
                    system_element = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().textContains("System")'
                    )
                except NoSuchElementException:
                    pass
                if not system_element:
                    try:
                        system_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("system")'
                        )
                    except NoSuchElementException:
                        pass
                if not system_element:
                    try:
                        system_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("About phone")'
                        )
                        if system_element:
                            print("Found 'About phone' (System section)")
                    except NoSuchElementException:
                        pass
                if system_element:
                    print(f"Found System section after {scroll_count + 1} scrolls!")
                    return system_element
            except Exception as e:
                print(f"Error during search: {e}")
            print(f"Scrolling down... (attempt {scroll_count + 1}/{max_scrolls})")
            self.scroll_down()
            time.sleep(1.5)
        print("Could not find System section after maximum scrolls")
        return None

    def close_app(self):
        """Close the Settings app"""
        try:
            self.driver.press_keycode(3)  # HOME key
            print("Pressed home button")
        except Exception as e:
            print(f"Error closing app: {e}")

    def save_recording_to_documents(self, video_base64, filename="test_evidence.mp4"):
        """Save the screen recording to the user's Documents folder"""
        documents_path = os.path.expanduser("~/Documents")
        if not os.path.exists(documents_path):
            os.makedirs(documents_path)
        file_path = os.path.join(documents_path, filename)
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(video_base64))
        print(f"Screen recording saved at: {file_path}")

    def run_automation(self):
        print("Starting Android Settings Automation")
        print("=" * 40)
        if not self.start_session():
            return False
        try:
            # Start screen recording
            self.driver.start_recording_screen(
                options={
                    'timeLimit': '180',         # up to 3 min
                    'videoSize': '1280x720',    # resolution
                    'bitRate': '4000000',       # quality
                    'videoFps': '30'            # frames per second
                }
            )
            time.sleep(3)
            print("Settings app loaded")
            system_element = self.find_system_section()
            if system_element:
                print("System section found!")
                try:
                    system_element.click()
                    print("Tapped on System section")
                    time.sleep(2)
                    self.driver.back()
                    time.sleep(1)
                    print("Returned to main Settings")
                except Exception as e:
                    print(f"Could not tap System section: {e}")
            print("Closing Settings app...")
            self.close_app()
            time.sleep(2)
            print("Automation completed successfully!")
            # Stop and save recording to Documents
            video_base64 = self.driver.stop_recording_screen()
            self.save_recording_to_documents(video_base64)
        except Exception as e:
            print(f"Automation failed: {e}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    print("Session ended")
                except Exception as e:
                    print(f"Error ending session: {e}")

if __name__ == "__main__":
    automation = SettingsAutomation()
    automation.run_automation()
