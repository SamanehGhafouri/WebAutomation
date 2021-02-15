from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# without GUI
# opts = Options()
# opts.headless = True
# assert opts.headless  # Operating in headless mode
# browser = Chrome(options=opts)
# browser.get('https://duckduckgo.com')
#######################################################################

# # with GUI
# browser = Chrome()
# browser.get('https://duckduckgo.com')
#
# # query the input by passing 'real python' in input to search
# search_form = browser.find_element_by_id('search_form_input_homepage')
# search_form.send_keys('real python')
# search_form.submit()
#
# # with this we can get the first item description in text in terminal
# results = browser.find_elements_by_class_name('result')
# print(results[0].text)

#######################################################################
# test the click button to play the music
browser = Chrome()
browser.get('https://bandcamp.com')
# browser.find_element_by_class_name('playbutton').click()

# find discover-item class
tracks = browser.find_elements_by_class_name('discover-item')
len(tracks)  # len of tracks
tracks[3].click() # find the 4th track and click
