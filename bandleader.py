from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# without GUI
# opts = Options()
# opts.headless = True
# assert opts.headless  # Operating in headless mode
# browser = Chrome(options=opts)
# browser.get('https://duckduckgo.com')

# with GUI
browser = Chrome()
browser.get('https://duckduckgo.com')