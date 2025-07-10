from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"  # Your device ID
options.automation_name = "UiAutomator2"
options.app_package = "com.android.settings"
options.app_activity = ".Settings"

try:
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    print("Session created successfully!")

except Exception as e:
    print(f"Failed: {e}")

