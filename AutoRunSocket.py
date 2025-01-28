from selenium import webdriver
from selenium.webdriver.edge.options import Options


# Configure Selenium to attach to the existing Edge session
def attach_to_existing_browser():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Match the debugging port

    try:
        driver = webdriver.Edge(options=options)  # Connect to the existing session
        print("Successfully attached to the existing browser session.")

        # Reload the current tab
        driver.refresh()
        print("Browser tab reloaded.")

        # Keep the session open for further commands
        input("Press Enter to close the session or Ctrl+C to leave the browser running...")
    except Exception as e:
        print(f"Failed to attach to the existing browser session: {e}")


if __name__ == "__main__":
    attach_to_existing_browser()
