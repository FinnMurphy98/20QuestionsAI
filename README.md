# 20QuestionsAI

## Virtual Environment Setup & Installations

1. Download and install Python version 3.11.3

2. Assuming you have cloned the GitHub repository to your local machine and have made it your current directory. 

3. Create a virtual environment with the following command-line prompt: `python3 -m venv venv`

4. If you are using linux/macOS, activate your virtual environment with the following command-line prompt: `source venv/bin/activate`

5. If you are using windows, activate your virtual environment with the following command-line prompt: `venv\Scripts\activate`

6. Install the required packages from the requirements.txt file with the following command-line prompt: `python3 -m pip install -r requirements.txt`

## Database Creation and Migration

1. With the reopsitory as your current directory and your virtual environment active...

2.  The migration scripts are already in source control. You can create the database if it doesn't exist on your local machine with the following command-line prompt: `flask db upgrade`

3. If you make any changes to the database models, update the migration script with the following command-line prompt: `flask db migrate -m "update tables"`

4. Repeat step 2 after updating the migration script.

## Run the app

1. With the reopsitory as your current directory and your virtual environment active...

2. If it is your first time running, then you need to create a file in the same directory as this `README.md` file called `.flaskenv`. This file is for adding environment variables. This file will be ignored by git when committing.

3. In the `.flaskenv` file, write `FLASK_APP=20questionsAI.py` and save it. 

4. Add a secret key to the `.flaskenv` by writing on a new line: `SECRET_KEY=`*your_secret_key*

5. If you want to run the application with debug mode turned on, then add a new line to the `.flaskenv` file: `FLASK_DEBUG=1`

6. Launch the application with the following command-line prompt: `flask run`

7. If the webpage doesn't automatically open on your default browser, then copy the url in the terminal output into a browser window, i.e. http://127.0.0.1:5000

## Website Layout

### Index/Home Page (http://127.0.0.1:5000/)
- Welcome message
- Short description about website
- Option to create an account
- Option to login

### Login Page (http://127.0.0.1:5000/login)
- login fields and submit button

### Create account Page (http://127.0.0.1:5000/sign_up)
- sign up fields and submit button

### Logged-in/User Home Page (http://127.0.0.1:5000/username)
- button to return to current game page (if they left a new game before it finished)
- button to play a new game as questioner (if no current game)
- button to play new game as answerer (if no current game)
- display some the users stats (such as win rate)
- option to logout (returns to index page)
- button to navigate to history page

### New Game Page (http://127.0.0.1:5000/username/game/gameID)
- can scroll through all sent messages in the game
- labels for who is the questioner and who is the answerer
- a chat bar for entering text
- a counter that shows what question number the questioner is on
- a buttons that the user can press to finish the game: "ChatGPT wins" or "You win" or "cancelled"
- option to go back to users home page
- option to go to history page
- option to log out (returns to index page)

### History page (http://127.0.0.1:5000/username/history)
- all games they've played and the summary results displayed starting from most recent
- can click on a past game to bring up the messages that were displayed
- can search past games by keywords
- option to go back to users home page
- opion to log out (returns to index page)

### Past Game Page (http://127.0.0.1:5000/username/past_game/gameID)
- can scroll through messages that were sent
- labels for who was the questioner and who was the answerer
- game winner displayed (you or ChatGPT)
- option to go back to history page
- option to go to users home page
- option to log out (returns to index page)
