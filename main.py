from bandleader import BandLeader
bl = BandLeader('myhistory.csv')
bl.play()           # Should start playing a track
bl.play(3)          # plays the third track in the listing
bl.play_next()      # advances the track
bl.more_tracks()    # see more music to play with
bl.browser.quit()   # close the webdriver instance

