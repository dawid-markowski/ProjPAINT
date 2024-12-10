from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tomek123'}
    parts = [
        {
            'part': {'name': 'tlumik'},
            'description': 'cos tam tlumi'
        },
        {
            'part': {'name': 'katalizator'},
            'description': 'czesto go kradna'
        }
    ]
    return render_template('index.html', title='Strona glowna', user=user, parts=parts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


