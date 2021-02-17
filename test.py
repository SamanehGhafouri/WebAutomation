from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep, ctime
from collections import namedtuple
from threading import Thread
from os.path import isfile
import csv

BANDCAMP_FRONTPAGE = 'https://bandcamp.com/'


class Test():
    def __init__(self):
        self.browser = Chrome()
        self.browser.get(BANDCAMP_FRONTPAGE)

        self._current_track_number = 1
        self.track_list = []
        self.tracks()

    def tracks(self):

        sleep(1)
        discover_section = self.browser.find_element_by_class_name('discover-results')
        left_x = discover_section.location['x']
        right_x = left_x + discover_section.size['width']

        discover_items = self.browser.find_elements_by_class_name('discover-item')
        self.track_list = [t for t in discover_items
                           if t.location['x'] >= left_x and t.location['x'] < right_x]

        for (i, track) in enumerate(self.track_list):
            print('[{}]'.format(i+1))
            lines = track.text.split('\n')
            print('Album : {}'.format(lines[0]))
            print('Artist : {}'.format(lines[1]))
            if len(lines) > 2:
                print('Genre : {}'.format(lines[2]))

    def catalogue_pages(self):

        print('PAGES')
        for e in self.browser.find_elements_by_class_name('item-page'):
            print(e.text)
        print('')

    def more_tracks(self, page='next'):

        next_btn = [e for e in self.browser.find_elements_by_class_name('item-page')
                    if e.text.lower().strip() == str(page)]

        if next_btn:
            next_btn[0].click()
            # self.tracks()
            print(self.tracks())

    def play(self, track=None):

        if track is None:
            self.browser.find_element_by_class_name('playbutton').click()
        elif type(track) is int and track <= len(self.track_list) and track >= 1:
            self._current_track_number = track
            self.track_list[self._current_track_number - 1].click()

    def play_next(self):

        if self._current_track_number < len(self.track_list):
            self.play(self._current_track_number + 1)
        else:
            self.more_tracks()
            self.play()

    def pause(self):

        self.play()


if __name__ == '__main__':
    my_test = Test()
    my_test.tracks()
    my_test.catalogue_pages()
    my_test.more_tracks()
    my_test.play(9)
    my_test.play_next()
    my_test.pause()





