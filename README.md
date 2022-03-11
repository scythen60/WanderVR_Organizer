# WanderVR_Organizer
<pre>
Set of scripts to help rename and organize favorites in WanderVR

Requirements:
Google maps API key https://developers.google.com/maps/documentation/javascript/get-api-key
Selenium and chrome web driver https://chromedriver.chromium.org/downloads
python version 3.5 or later
python modules: reverse_geocoder, requests, selenium, bs4, pandas


Instructions:
Make sure you have backed up your Wander_Favorites.json file, and that a copy of it exists in the directory configured at the bottom of wanderorganize.py.

create wander.db with wander.db.sql

wanderclean.py - A way to flag broken panoids. Only used once in awhile to clear out deleted photospheres.
wandermake.py - Work in progress. Don't use.
wanderorganize.py - Main program that renames and alphabetically sorts Wander_Favorites.json in same directory. Make sure to create a backup!
wanderscrape.py - Scrapes tmp.txt in same directory for adhoc links. You can grab many links at once using network inspector in a browser and copying HAR text. Can also parse streetviewfun.com.
wanderview.py - Creates a static html page to view thumbnails / links to favorites. Needs more work to be useful.

</pre>
