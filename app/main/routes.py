from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.main.forms import EditProfileForm
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import User, Part, Order, OrderItem
from app.main import bp
from sqlalchemy import func

@bp.route('/')
@bp.route('/index')
def index():
    parts = db.session.scalars(sa.select(Part)).all()
    return render_template('index.html', title='Strona glowna', parts=parts)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))

    # Pobranie liczby zamówień
    order_count = db.session.scalar(
        sa.select(func.count(Order.id)).where(Order.user_id == user.id)
    ) or 0

    # Pobranie sumy wydanych pieniędzy
    total_spent = db.session.scalar(
        sa.select(func.sum(OrderItem.quantity * Part.price))
        .join(Order)
        .join(Part)
        .where(Order.user_id == user.id)
    ) or 0

    address_data_present = bool(user.address and user.city and user.postal_code)

    return render_template('user.html', user=user, order_count=order_count, total_spent=total_spent,address_data_present=address_data_present)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
    return render_template('edit_profile.html', title='Edit Profile', form=form)

