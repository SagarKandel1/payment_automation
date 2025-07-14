import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from screenrecording import save_recording_to_documents

class SettingsAutomation:
    def __init__(self):
        self.driver = None

    def setup_capabilities(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"  # Replace with actual device ID
        options.automation_name = "UiAutomator2"
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"
        options.no_reset = True
        return options

    def start_session(self):
        try:
            options = self.setup_capabilities()
            self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            print("Settings app opened successfully!")
            return True
        except Exception as e:
            print(f"Failed to start session: {e}")
            return False

    def scroll_down(self):
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] // 2
            start_y = int(screen_size['height'] * 0.8)
            end_y = int(screen_size['height'] * 0.2)
            self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
        except Exception as e:
            print(f"Scroll failed: {e}")

    def find_system_section(self, max_scrolls=5):
        print("Looking for 'System' section...")
        for scroll_count in range(max_scrolls):
            try:
                system_element = None
                for text in ["System", "system", "About phone"]:
                    try:
                        system_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiSelector().textContains("{text}")'
                        )
                        if system_element:
                            print(f"Found '{text}' section")
                            return system_element
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"Error during search: {e}")
            print(f"Scrolling down... (attempt {scroll_count + 1}/{max_scrolls})")
            self.scroll_down()
            time.sleep(1.5)
        print("Could not find System section after maximum scrolls")
        return None

    def close_app(self):
        try:
            self.driver.press_keycode(3)  # HOME key
            print("Pressed home button")
        except Exception as e:
            print(f"Error closing app: {e}")

    def run_automation(self):
        print("Starting Android Settings Automation")
        print("=" * 40)
        if not self.start_session():
            return False
        try:
            self.driver.start_recording_screen(
                options={
                    'timeLimit': '180',
                    'videoSize': '1280x720',
                    'bitRate': '4000000',
                    'videoFps': '30'
                }
            )
            time.sleep(3)
            print("Settings app loaded")

            system_element = self.find_system_section()
            if system_element:
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

            video_base64 = self.driver.stop_recording_screen()
            save_recording_to_documents(video_base64)
        except Exception as e:
            print(f"Automation failed: {e}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    print("Session ended")
                except Exception as e:
                    print(f"Error ending session: {e}")
