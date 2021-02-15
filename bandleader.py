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

# query the input by passing 'real python' in input to search
search_form = browser.find_element_by_id('search_form_input_homepage')
search_form.send_keys('real python')
search_form.submit()