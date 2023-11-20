# MTGSinglesBulkSearch
Bulk search for MTGSingles.co.nz (not affiliated with the site owners)

PLEASE NOTE:
Currently, on top of the code itself, it takes an extra one second per card as it needs to search for every card and waits for one second between searches as to not overwhelm the website. For EDH decks, this may mean a runtime of about 2 minutes. 

REQUIREMENTS (Windows only):
Python 3 installed.
Firefox installed in the default location (otherwise you'll need to change the path in the code).
Geckodriver for Firefox (the .exe from the .zip file in the same folder as the Python file), found below:
https://github.com/mozilla/geckodriver/releases
Selenium installed through Python 3, can be installed by opening a command prompt and entering "pip install selenium".

Deck lists need to be in the following formatting in a .txt file named "decklist.txt" in the same folder as the Python file. An example is provided. The formatting must be as follows:
One card name per line,  no quantities or editions. 

The console currently shows a list of stores with the total number of cards. The names of the cards themselves along with the price of each is written to a .txt file named "cardlocations.txt" that will be created in the same folder as the Python file. 

I'm in the process of developing a version that can be hosted on a web page, currently has an extremely basic web page and still needs formatting to be fixed. The templates folder and the main_web.py file are only necessary when attempting to run the web version. 
