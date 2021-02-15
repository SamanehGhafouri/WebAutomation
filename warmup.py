from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# without GUI
opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts)
browser.get('https://duckduckgo.com')
#######################################################################

# with GUI
browser = Chrome()
browser.get('https://duckduckgo.com')

# query the input by passing 'real python' in input to search
search_form = browser.find_element_by_id('search_form_input_homepage')
search_form.send_keys('real python')
search_form.submit()

# with this we can get the first item description in text in terminal
results = browser.find_elements_by_class_name('result')
print(results[0].text)

#######################################################################
# test the click button to play the music
browser = Chrome()
browser.get('https://bandcamp.com')
browser.find_element_by_class_name('playbutton').click()

# find discover-item class
tracks = browser.find_elements_by_class_name('discover-item')
len(tracks)  # len of tracks
tracks[3].click() # find the 4th track and click

#######################################################################
# Exploring the Catalogue
next_button = [e for e in browser.find_elements_by_class_name('item-page')
               if e.text.lower().find('next') > -1]

next_button.click()

discover_section = browser.find_element_by_class_name('discover-results')
left_x = discover_section.location['x']
right_x = left_x + discover_section.size['width']
discover_items = browser.find_element_by_class_name('discover_items')
tracks = [t for t in discover_items
              if t.location['x'] >= left_x and t.location['x'] < right_x]
assert len(tracks) == 8
