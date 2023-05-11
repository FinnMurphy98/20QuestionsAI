from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, FinishGameForm
from flask_login import current_user, login_user
from app.models import User, Game
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('home.html', user=user)

@app.route('/choose_role', methods=['GET', 'POST'])
def role():
    return render_template('role.html')

@app.route('/game/<role>', methods=['GET', 'POST'])
@login_required
def new_game(role):
    form = FinishGameForm()
    if form.validate_on_submit():
        game = Game(user_id=current_user.id, role=role, winner=form.winner.data)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('home', username=current_user.username))
    return render_template('new_game.html', role=role, form=form)

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    games = current_user.games
    return render_template('history.html', games=games)

@app.route('/history/<gameID>')
@login_required
def past_game(gameID):
    game = Game.query.filter_by(id=gameID).first_or_404()
    return render_template('past_game.html', game=game)