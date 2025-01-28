from selenium import webdriver
from selenium.webdriver.edge.options import Options


# Configure Selenium to attach to the existing Edge session
def attach_to_existing_browser():
    print("starting")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Match the debugging port

    try:
        driver = webdriver.Edge(options=options)  # Connect to the existing session
        print("Successfully attached to the existing browser session.")


        # Reload the current tab
        driver.refresh()
        print("Browser tab reloaded.")
        print("Page reloaded.", flush=True)

        # Close the Selenium WebDriver instance but leave the browser running
        driver.quit()  # Disconnect Selenium without closing the browser
        print("Disconnected Selenium session. Browser remains open.")
    except Exception as e:
        print(f"Failed to attach to the existing browser session: {e}")


if __name__ == "__main__":

    attach_to_existing_browser()

#
# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
#
# # Path to EdgeDriver executable
# EDGE_DRIVER_PATH = r"C:\WebDriver\msedgedriver.exe"  # Update this path
#
# # Set up options for Microsoft Edge
# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_argument("--start-maximized")  # Open browser in maximized mode
# # Add more options if needed, e.g., headless mode:
# # options.add_argument("--headless")  # Run in headless mode (no UI)
#
# # Set up the Service object
# service = Service(EDGE_DRIVER_PATH)
#
# # Start the WebDriver and open Microsoft Edge
# driver = webdriver.Edge(service=service, options=options)
#
# # Open a website
# driver.refresh()
# driver.quit()

