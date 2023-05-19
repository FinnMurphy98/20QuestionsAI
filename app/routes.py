from app import bp, db, ANSWERER_PROMPT, QUESTIONER_PROMPT
from flask import Response, render_template, flash, redirect, url_for, request, session
from app.forms import LoginForm, RegistrationForm, FinishGameForm
from flask_login import current_user, login_user
from app.models import User, Game, Message
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.openai.chat import chatgpt_response

@bp.route('/')
def index():
    """
    Route handler for the index page.
    """
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route handler for the login page. 
    Redirects user to home if already logged in.
    """
    if current_user.is_authenticated:
        return redirect(url_for('app.home', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('app.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('app.home', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)

@bp.route('/logout')
@login_required
def logout():
    """
    Route handler for logout. 
    Does not render a page, instead redirects to index page.
    """
    logout_user()
    return redirect(url_for('app.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route handler for register page. 
    Logged-in users are redirected to index page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('app.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered with an account!')
        return redirect(url_for('app.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/home/<username>')
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

@bp.route('/choose_role', methods=['GET', 'POST'])
def role():
    """
    Route handler for the role page. 
    User selects a role before a new game. 
    """
    return render_template('role.html')

@bp.route('/game/<role>', methods=['GET', 'POST'])
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
    prompt = ''
    if role == 'Answerer':
        prompt += ANSWERER_PROMPT
    elif role == 'Questioner':
        prompt += QUESTIONER_PROMPT
    else:
        return Response(status=404)
    session['messages'] = [{"timestamp": datetime.utcnow(), "role": "user", "content": prompt}]
    messages = [{"role": "user", "content": prompt}]
    reply = chatgpt_response(messages)
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
        return redirect(url_for('app.history'))
    return render_template('new_game.html', role=role, form=form, prompt=prompt, reply=reply)

@bp.route('/history')
@bp.route('/history/<arg1>')
@bp.route('/history/<arg1>/<arg2>')
@login_required
def history(**kwargs):
    """
    Route handler for the history page. 
    Displays users past games in order of most recent by default. 
    User can filter which games are displayed on the page by date, role and winner. 
    """
    page = request.args.get('page', 1, type=int)
    per_page = 15
    filters = list(kwargs.values())
    games = current_user.games.order_by(Game.timestamp.desc())
    if ('Answerer' in filters and 'Questioner' in filters) or ('Winner' in filters and 'Loser' in filters):
        return Response(status=404)
    if 'Answerer' in filters:
        games = current_user.games.filter_by(role='Answerer').order_by(Game.timestamp.desc())
    if 'Questioner' in filters:
        games = current_user.games.filter_by(role='Questioner').order_by(Game.timestamp.desc())
    if 'Winner' in filters:
        games = games.filter_by(winner=True).order_by(Game.timestamp.desc())
    if 'Loser' in filters:
        games = games.filter_by(winner=False).order_by(Game.timestamp.desc())
    paginated = games.paginate(page=page, per_page=per_page)
    return render_template('history.html', games=paginated)

@bp.route('/past_game/<gameID>')
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