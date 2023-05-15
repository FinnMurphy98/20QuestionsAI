from app import app, db, openai
from flask import Response, render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegistrationForm, FinishGameForm
from flask_login import current_user, login_user
from app.models import User, Game, Message
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from flask_socketio import emit
from openai import ChatCompletion
from app.constants import ANSWERER_PROMPT, QUESTIONER_PROMPT

@app.route('/')
def index():
    """
    Route handler for the index page.
    """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route handler for the login page. 
    """
    if current_user.is_authenticated:
        return redirect(url_for('home', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)

@app.route('/logout')
def logout():
    """
    Route handler for logout. 
    Does not render a page, instead redirects to index page.
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route handler for register page. 
    Logged-in users are redirected to index page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered with an account!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/home/<username>')
@login_required
def home(username):
    """
    Route handler for the user home page. 
    Page displays users stats and invites them to begin a new game. 
    If user is trying to access another users home page, return 403 Forbidden response.
    """
    if current_user.username != username:
        return Response(status=403)
    user = User.query.filter_by(username=username).first_or_404()
    stats = user.stats()
    return render_template('home.html', user=user, stats=stats)

@app.route('/choose_role', methods=['GET', 'POST'])
def role():
    """
    Route handler for the role page. 
    User selects a role before a new game. 
    """
    return render_template('role.html')

@app.route('/game/<role>', methods=['GET', 'POST'])
@login_required
def new_game(role):
    """
    Route handler for the new_game page.
    Users can chat with ChatGPT in a game of 20 questions. 
    Resets session variables for a new game. 
    The initial prompt for ChatGPT will be different depending on the users role.
    Upon valid form submit: every message in the session messages is committed to the database. 
    If the role is not 'Questioner' or 'Answerer', return 404 Not Found response.
    """
    session['role'] = role
    prompt = ''
    if role == 'Answerer':
        prompt += ANSWERER_PROMPT
    elif role == 'Questioner':
        prompt += QUESTIONER_PROMPT
    else:
        return Response(status=404)
    session['messages'] = [{"timestamp": datetime.utcnow(), "role": "user", "content": prompt}]
    completion = ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )
    reply = completion['choices'][0]['message']['content']
    session['messages'].append({"timestamp": datetime.utcnow(), "role": "assistant", "content": reply})
    form = FinishGameForm()
    if form.validate_on_submit():
        game = Game(user_id=current_user.id, role=role, winner=form.winner.data)
        db.session.add(game)
        db.session.commit()
        for msg in session['messages']:
            message = Message(timestamp=msg['timestamp'], game_id=game.id, role=msg['role'], content=msg['content'])
            db.session.add(message)
        db.session.commit()
        return redirect(url_for('home', username=current_user.username))
    return render_template('new_game.html', role=role, form=form, prompt=prompt, reply=reply)

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    """
    Route handler for the history page. 
    Displays users past games in order of most recent by default. 
    User can filter which games are displayed on the page by date, role and winner. 
    """
    games = current_user.games
    return render_template('history.html', games=games)

@app.route('/history/<gameID>')
@login_required
def past_game(gameID):
    """
    Route handler for the past_game page. 
    Displays the messages, role and winner result for a previously played game. 
    If the game was played by another user, then return 403 Forbidden response.
    """
    game = Game.query.filter_by(id=gameID).first_or_404()
    if current_user.id != game.user_id:
        return Response(status=403)
    messages = game.messages
    return render_template('past_game.html', game=game, messages=messages)