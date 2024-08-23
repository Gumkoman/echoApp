from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy



def setup_appium_connection(app_package, app_activity):
    # Define the Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Set up desired capabilities
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        appPackage=app_package,
        appActivity=app_activity,
        newCommandTimeout=360,
        adbExecTimeout=40000,
        fullReset=False,
        noReset=True
    )

    # Load capabilities into UiAutomator2Options
    options = UiAutomator2Options()
    options.load_capabilities(capabilities)

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)

    # Start the specified app activity
    driver.execute_script('mobile: shell', {
        'command': 'am',
        'args': ['start', '-n', f'{app_package}/{app_activity}']
    })

    return driver

if __name__ == '__main__':
    # Replace these with your app's package and activity
    app_package = 'com.EveryTalk.Global'
    app_activity = 'com.cybertel.mcptt.ui.main.EveryTalkMain'

    # Setup the Appium connection
    driver = setup_appium_connection(app_package, app_activity)

    # Drop into the Python shell
    import code
    code.interact(local=locals())