# root routes and defailt views
from flask import redirect, render_template, request, flash, url_for
from flask_login import login_user, logout_user

from user.forms import LoginForm

from app import app


@app.route('/')
def homepage():
    name = request.args.get('name')
    if not name:
        name = '<unknown>'
    return render_template('homepage.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash('Successfully logged in as %s' % form.user.email, 'success')
            return redirect(request.args.get('next') or url_for('homepage'))
    else:
        form = LoginForm()
    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(request.args.get('next') or url_for('homepage'))