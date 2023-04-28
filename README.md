# 20QuestionsAI

## Setup & Installations

1. Download and install Python version 3.11.3

2. Assuming you have cloned the GitHub repository to your local machine and have made it your current directory. 

3. Create a virtual environment with the following command-line prompt: `python3 -m venv venv`

4. If you are using linux/macOS, activate your virtual environment with the following command-line prompt: `source venv/bin/activate`

5. If you are using windows, activate your virtual environment with the following command-line prompt: `venv\Scripts\activate`

6. Install the required packages from the requirements.txt file with the following command-line prompt: `python3 -m pip install -r requirements.txt`

## Run the app

1. With the reopsitory as your current directory and your virtual environment active...

2. If it is your first time running, then you need to create a file in the same directory as this `README.md` file called `.flaskenv`. 

3. In the `.flaskenv` file, write `FLASK_APP=20questionsAI.py` and save it. This file will be ignored by git when committing.

4. Launch the application with the following command-line prompt: `flask run`

5. If the webpage doesn't automatically open on your default browser, then copy the url in the terminal output into a browser window, i.e. http://127.0.0.1:5000

7. If you want to run the application with debug mode turned on, then add a new line to the `.flaskenv` file: `FLASK_DEBUG=1`