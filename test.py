from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep, ctime
from collections import namedtuple
from threading import Thread
from os.path import isfile
import csv

BANDCAMP_FRONTPAGE = 'https://bandcamp.com/'
TrackRec = namedtuple('TrackRec', [
                                    'title',
                                    'artist',
                                    'artist_url',
                                    'album',
                                    'album_url',
                                    'timestamp'     # When you played it
                                    ])


class Test():
    def __init__(self, csvpath = None):

        self.database_path = csvpath
        self.database = []

        if isfile(self.database_path):
            with open(self.database_path, newline='') as dbfile:
                dbreader = csv.reader(dbfile)
                next(dbreader)
                self.database = [TrackRec._make(rec) for rec in dbreader]

        self.browser = Chrome()
        self.browser.get(BANDCAMP_FRONTPAGE)

        self._current_track_number = 1
        self.track_list = []
        self.tracks()

        self.database = []
        self._current_track_record = None

        self.thread = Thread(target=self._maintain)
        self.thread.daemon = True
        self.thread.start()

        self.tracks()

    def save_db(self):

        with open(self.database_path, 'w', newline='') as dbfile:
            dbwriter = csv.writer(dbfile)
            dbwriter.writerow(list(TrackRec._fields))
            for entry in self.database:
                dbwriter.writerow(list(entry))

    def _maintain(self):

        while True:
            self._update_db()
            sleep(20)

    def _update_db(self):

        try:
            check = (self._current_track_record is not None
                     and self._current_track_record is not None
                     and (len(self.database) == 0
                          or self.database[-1] != self._current_track_record)
                     and self.is_playing())
            if check:
                self.database.append(self._current_track_record)
                self.save_db()

        except Exception as e:
            print('error while updating the db: {}'.format(e))

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

        sleep(0.5)
        if self.is_playing():
            self._current_track_record = self.currently_playing()

    def play_next(self):

        if self._current_track_number < len(self.track_list):
            self.play(self._current_track_number + 1)
        else:
            self.more_tracks()
            self.play()

    def pause(self):

        self.play()

    def is_playing(self):

        playbtn = self.browser.find_element_by_class_name('playbutton')
        return playbtn.get_attribute('class').find('playing') > -1

    def currently_playing(self):

        try:
            if self.is_playing():
                title = self.browser.find_element_by_class_name('title').text
                album_detail = self.browser.find_element_by_css_selector('.detail-artist > a')
                album_title = album_detail.text
                album_url = album_detail.get_attribute('href').split('?')[0]
                artist_detail = self.browser.find_element_by_css_selector('.detail-artist > a')
                artist = artist_detail.text
                artist_url = artist_detail.get_attribute('href').split('?')[0]
                return TrackRec(title, artist, artist_url, album_title, album_url, ctime())
        except Exception as e:
            print('there was an error: {}'.format(e))

        return None



if __name__ == '__main__':
    my_test = Test('myhistory.csv')
    my_test.tracks()
    my_test.catalogue_pages()
    my_test.more_tracks()
    my_test.play(1)
    my_test.play_next()
    # my_test.pause()
    playing = my_test.is_playing()
    my_test.currently_playing()
    my_test.save_db()
    my_test._maintain()
    my_test._update_db()








