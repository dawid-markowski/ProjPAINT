from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.main.forms import EditProfileForm
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import User, Part
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    parts = db.session.scalars(sa.select(Part)).all()
    return render_template('index.html', title='Strona glowna', parts=parts)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    parts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, parts=parts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
