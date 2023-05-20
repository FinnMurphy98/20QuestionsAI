# 20QuestionsAI

![Tests](https://github.com/FinnMurphy98/20questionsAI/actions/workflows/tests.yml/badge.svg)

---
# Documentation

## Virtual Environment Setup & Installations

1. Download and install Python version 3.11.3

2. Assuming you have cloned the GitHub repository to your local machine and have made it your current directory. 

3. Create a virtual environment with the command-line: `python3 -m venv venv`

4. If you are using linux/macOS, activate your virtual environment with the command-line: `source venv/bin/activate`

5. If you are using windows, activate your virtual environment with the command-line: `venv\Scripts\activate`

6. Install the required packages from the requirements.txt file with the command-line: `python3 -m pip install -r requirements.txt`

## Database Creation and Migration

1. With the reopsitory as your current directory and your virtual environment active...

2. The migration scripts are already in source control. You can create the database if it doesn't exist on your local machine with the command-line: `flask db upgrade`

3. If you make any changes to the database models, update the migration script using the command-line: `flask db migrate -m "update tables"`

4. Repeat step 2 after updating the migration script.

## Secret Environment Variables

1. Create a file called `.env` in the top level directory which will be ignored by git. 

2. On the first line of your `.env` file, write `SECRET_KEY=`*your_secret_key*

3. On the second line, add your openai api key: `OPENAI_KEY`=*your_openai_api_key*

## Run the app

1. With the reopsitory as your current directory and your virtual environment active...

2. Launch the application using the command-line: `python3 20questionsAI.py`

3. If the webpage doesn't automatically open on your default browser, then copy the url in the terminal output into a browser window, i.e. http://127.0.0.1:5000

## Testing

1. To run all functional and unit tests in the command-line, run `python -m pytest`. Sometimes deprecaition warnings can be overwhelming, so to ignore them, instead run `python -m pytest -p no:warnings`

2. To see the test coverage as well, run: `python -m pytest --cov=app -p no:warnings`

---
## Front-end Website Layout

### Navigation Bar (not logged in)
- Link to index page (20questionsAI)
- Link to login page

### Navigation Bar (logged in)
- Link to index page (20questionsAI)
- Link to home page
- Link to play new game
- Link to history page
- Username in top right corner (hover brings up logout link)

### Index Page
- Description about the website
- Login link in the navigation bar

### Login Page
- Login form: username, password and remember me fields
- Link to register if you don't have an account
- Successful login redirects to users home page, or wherever the user was trying to navigate to before login
- Unsuccessful login redirects back to login page with flashed messages

### Register Page
- Registraion form: username, email, password and repeat password fields
- Successful registration redirects user to login page
- Unsuccessful registration redirects back to registration fields with flashed messages

### Home Page
- Displays username
- Displays users statistics:
- Total number of games played, number played as answerer, number played as questioner
- Total number of wins, number of wins as answerer, number of wins as questioner
- Total win rate, win rate as answerer, win rate as questioner

### Choose Role Page
- When user selects new game from navigation bar, they taken to this page first to choose a role
- Button to select answerer or button to select Questioner
- After selecting role, user is taken to new game page

### New Game Page
- Chat box to talk with ChatGPT in a game of 20 questions
- First two messages are automatically generated
- First message is the initial prompt to get ChatGPT to play. It changes depending on the chosen role.
- Second message is the first reply from ChatGPT. 
- All messages after that are from live chat between user and ChatGPT. 
- Form to submit the game once the user thinks its over: tick if you won field

### History page
- all games they've played and the summary results displayed starting from most recent
- can click on a past game to bring up the messages that were displayed
- can search past games by keywords
- option to go back to users home page
- option to log out (returns to index page)

### Past Game Page (http://127.0.0.1:5000/username/past_game/gameID)
- can scroll through messages that were sent
- labels for who was the questioner and who was the answerer
- game winner displayed (you or ChatGPT)
- option to go back to history page
- option to go to users home page
- option to log out (returns to index page)
