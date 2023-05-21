# 20QuestionsAI

![Tests](https://github.com/FinnMurphy98/20questionsAI/actions/workflows/tests.yml/badge.svg)

## Note to Markers
We encountered some errors with database migrations and had to delete and reinitialize the folder 
close to the end of the project. But the old migrations folder is included in the repository to show the full migration history. 

# Overview of the Application

The idea of the application is to facilitate 'loose' games of 20 Questions against ChatGPT. Loose meaning they are not tightly controlled by the application logic. ChatGPT is automatically prompted to play a game of 20 questions with you, but the prompt itself is open to change and refinement. ChatGPT can play along fairly well but sometimes needs to be kept on track with intelligent messaging. We rely on the honour system here, as users must decide whether they or ChatGPT won the game. Users can view the results and messages from their previous games on the history page. They can also view their personal stats such as their overall or role-specific win rate. 

# Documentation

## Virtual Environment Setup & Installations

1. Download and install the latest Python version

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

2. Launch the application using the command-line: `python3 20questionsAI.py` instead of `flask run` so the socket will work properly

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

### Past Game Page
- User can scrole through 

---
## API

This application uses openai's ChatCompletion.create() function that takes a model and list of messages as parameters. The model we use is ChatGPT 3.5 Turbo. The messages it accepts are dictionaries with two keys: role (user or assistant) and content. It provides a similar service to the ChatGPT on the openai website, only it does not manage message history. So to maintain a conversation, our application must keep track of message history and feed it to the ChatCompletion.create() method for every new response. We have wrapped up the chat completion api in our own method called chatgpt_response(). In order to use the API you need an openai api key. You can obtain one from the openai website after creating an account and registering a payment method. This key should be stored as an environment variable or in an environment file that is ingored by GIT. The api is not free but it is very cheap. It charges you on a per-token basis and has only cost us about 20 cents at the time of writing this (21st of May). 

---
## Database Models

### User
- Represents a user account for the website
- Columns: id (primary key), username (unique), email (unique), hashed password
- Methods: set password, check password, get users game stats

### Game
- Represents a game of 20 questions
- Columns: id (primary key), timestamp, user_id (foreign key) role, winner, finished
- user_id is the id of the user who played the game
- role is either 'Questioner' or 'Answerer'
- winner is true if the user won, false is they lost
- finished is true of the game was properly finished, false if not

### Message
- Represents a message sent by a user or by chatgpt
- Columns: id (primary key), timestamp, game_id (foreign key), role, content
- game_id is the id of the game the message was sent in
- role is either 'user' if it was sent by a user or 'assistant' if it was sent by chatgpt
- content is the content of the message

## Forms

### Login Form
- Requires username and password fields
- Optional 'remember me' field

### Registration Form
- Requires username, email and two matching passwords
- Username is validated if no other users have the same
- Email is validated if no other users have the same

### Finish Game Form
- When a user feels a game of 20 questions has come to a conclusion, they can submit this form to end it properly
- Tick box if the user one, leave unticked if they lost

---
## Route Handler Functions

### index (/)
- Renders the template for the index page

### login (/login)
- If the user attempts to access page when they are already logged in they will be redirected to their home page
- If they user sent a GET request for the page then the login template is rendered
- If the user sent a POST request and the login form is validated: 
    - database is queried to find the user
    - if a user is matched, and password unhashes hashed password then they are logged in a redirected to their home page
    - else they are send back to login page with a flashed error message
- If the user was redirected to the login page because they were trying to request a page that is blocked by login, then upon successful login they will be sent to that page.

### logout (/logout)
- Just logs out the user and redirects to the index page

### register (/register)
- Redicrects the user to the home page if they are already logged in
- If user makes a GET request then the register page is rendered
- If the user makes a post request and the form is validated:
    - creates a new user and sets the their password
    - flashes a 'congratulations' message
    - redirects to the user to the login page

### home (/home/username)
- Takes username as a parameter
- Returns a 403 Forbidden request if a user tries to access another users home page
- Renders the home page template and passes the users stats as a parameter

### role (/choose_role)
- Renders the role template

### new_game (/game/role)
- Takes role as a parameter
- If the user makes a GET request:
    - create a new game object and commit it to the database
    - store the game id as a session variable
    - set the initial prompt for chatgpt based on the users chosen role
    - if the role parameter is something other than Answerer or Questioner then return 404
    - add the initial prompt to the database as a message object
    - gets chatgpts response from the initial prompt and stores it in the database as a message object
- If the user makes a POST request and the form is validated:
    - update the game as a finished game
    - update the game winner as true or false based on the finish game form data
    - redirect to the history page

### history (/history)
- Takes optional arguments as filters for role and result (i.e. answerer, questioner, winner, loser)
- Retrieves all the users games from the database and paginates them with 15 games per page
- Renders the history template and passes the paginated games to it as a parameter

### past_game (/past_game)
- Takes a gameID as a parameter
- If a user is trying to view another users game then return 403 Forbidden response
- Retrieves all the messages attached to this specific game
- Renders the past_game page and passes the messages as a parameter

---
## Event Handler Functions

### message
- Uses FlaskSocketIO for live chat
- Socket operates on the new_game page
- Triggered by a socket.on('message') event
- Takes the message data sent from the client as a parameter
- Stores the clients message in the database
- Retrieves all the messages in the database so far that are associated with the current session game_id and feeds the messages to ChatGPT for a response.
- Stores chatgpts reply in the database and emits it back to the client

