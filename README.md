Project for a free betting website (fantasy league) on soccer championships.

Made with the web developement framework *Flask*.

# Installation

1. Install python3 (tested with python 3.7.2)
2. Clone the repo and CD into it
3. Install required Python packages: `pip install -r requirements.txt`
4. Change the config.py file and link it to your database.
5. Create the DB: `flask db upgrade`
6. Populate the database `flask create-enums`


# Testing the website

Type `flask run`

And go to http://127.0.0.1:5000/ to access the home page
