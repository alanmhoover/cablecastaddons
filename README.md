# cablecastaddons
add ons for use with cablecast using the cablecast web api

Download.py is to automatically download Democracy Now! everyday.

Changeformat.py is to update shows that have been played and recorded for future replay from a stream (in our triggering use case, Free Speech TV).  In order to replay properly the shows need the following updates:  Format needs changed from network stream to video server; and the length (Duration needs updated to the file lengrth (typically one second less than the scheduled record time).  changeformat.py reads cablecastconfig.ini to get the ip address of the cablecast frontdoor and the login information to do the updates.  The ini file also specifies the format codes for the necessary formats.  Changeformat.py uses the passed in parameter as the id of a saved search to find the show to update.

ccapi.py retrieves config file options and provides re-used/re-usable functions.

addchapters.py reads a text file and inserts the chapter information therein to the VOD.  The first line of the file is the showid.  Subsequent lines start with a time code ([:ss]|[mm:ss]|[hh:mm:ss]) then text {description}.  The first 50 characters of {description} are placed in title, entire {description} is placed in body.
