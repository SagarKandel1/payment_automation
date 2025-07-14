import time
import base64
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
        options.device_name = "emulator-5554"  # Replace with your device ID
        options.automation_name = "UiAutomator2"
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"
        options.no_reset = True

        return options

    def start_session(self): #session start
        """Start Appium session"""
        try:
            options = self.setup_capabilities()
            self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            print("Settings app opened successfully!")
            return True
        except Exception as e:
            print(f" Failed to start session: {e}")
            return False

    def scroll_down(self):
        """Perform scroll down action"""
        try:
            # Get screen size for dynamic scrolling
            screen_size = self.driver.get_window_size()

            # Calculate scroll coordinates (from 80% to 20% of screen height)
            start_x = screen_size['width'] // 2
            start_y = int(screen_size['height'] * 0.8)
            end_y = int(screen_size['height'] * 0.2)

            # Perform scroll with smooth duration
            self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

        except Exception as e:
            print(f" Scroll failed: {e}")

    def find_system_section(self, max_scrolls=5):
        """Scroll down until System section is found"""
        print(" Looking for 'System' section...")

        for scroll_count in range(max_scrolls):
            try:
                # Try multiple ways to find System section
                system_element = None

                # Method 1: Look for exact text "System"
                try:
                    system_element = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().textContains("System")'
                    )
                except NoSuchElementException:
                    pass

                # Method 2: Look for "System" in different case
                if not system_element:
                    try:
                        system_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("system")'
                        )
                    except NoSuchElementException:
                        pass

                # Method 3: Look for common system-related text
                if not system_element:
                    try:
                        system_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("About phone")'
                        )
                        if system_element:
                            print(" Found 'About phone' (System section)")
                    except NoSuchElementException:
                        pass

                if system_element:
                    print(f" Found System section after {scroll_count + 1} scrolls!")
                    return system_element

            except Exception as e:
                print(f"️ Error during search: {e}")

            # Scroll down if not found
            print(f" Scrolling down... (attempt {scroll_count + 1}/{max_scrolls})")
            self.scroll_down()
            time.sleep(1.5)  # Wait for scroll to complete

        print(" Could not find System section after maximum scrolls")
        return None

    def close_app(self):
        """Close the Settings app"""
        try:
            # Method 1: Use home button
            self.driver.press_keycode(3)  # HOME key
            print(" Pressed home button")

            # Alternative method: Terminate app
            # self.driver.terminate_app("com.android.settings")

        except Exception as e:
            print(f" Error closing app: {e}")

    def run_automation(self):
        """Main automation execution"""
        print(" Starting Android Settings Automation")
        print("=" * 40)

        # Step 1: Start session and open Settings
        if not self.start_session():
            return False

        try:
            # Step 2: Wait for app to fully load
            time.sleep(3)
            print("📱 Settings app loaded")

            # Step 3: Scroll to find System section
            system_element = self.find_system_section()

            if system_element:
                print(" System section found!")

                # Optional: Highlight the found element by tapping it
                try:
                    system_element.click()
                    print(" Tapped on System section")
                    time.sleep(2)

                    # Go back to main settings
                    self.driver.back()
                    time.sleep(1)
                    print(" Returned to main Settings")

                except Exception as e:
                    print(f"️ Could not tap System section: {e}")

            # Step 4: Close the app
            print(" Closing Settings app...")
            self.close_app()
            time.sleep(2)

            print(" Automation completed successfully!")

        except Exception as e:
            print(f" Automation failed: {e}")

        finally:
            # Clean up session
            if self.driver:
                try:
                    self.driver.quit()
                    print(" Session ended")
                except Exception as e:
                    print(f" Error ending session: {e}")


# Usage
if __name__ == "__main__":
    automation = SettingsAutomation()
    automation.run_automation()


