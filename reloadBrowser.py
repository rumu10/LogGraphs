from selenium import webdriver
from selenium.webdriver.edge.options import Options


def attach_to_existing_browser():
    print("Starting...")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        driver = webdriver.Edge(options=options)
        print("Successfully attached to the existing browser session.")

        # Disable cache so that each refresh fetches fresh content
        driver.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})

        # Use a hard reload to bypass cache completely
        driver.execute_script("window.location.reload(true);")
        print("Browser tab reloaded with cache bypass.")

        # Optionally, do not quit the session if you plan on reusing it
        # driver.quit()  # Avoid terminating the session if you want to reattach later
        print("Selenium session remains active for further interactions.")
    except Exception as e:
        print(f"Failed to attach to the existing browser session: {e}")


if __name__ == "__main__":
    attach_to_existing_browser()
