from app.checkout import bp
from app import db
import sqlalchemy as sa
from app.models import Part, Cart, CartItem, Order, OrderItem
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.checkout.forms import CheckoutForm



@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user = current_user

    if not user.cart or not user.cart.items:
        flash("Twój koszyk jest pusty!", "warning")
        return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()
    if form.validate_on_submit():
        # Utwórz zamówienie
        order = Order(
            user=user,
            address=form.address.data,
            city=form.city.data,
            postal_code=form.postal_code.data,
            status='pending'
        )
        db.session.add(order)

        cart_items_query = sa.select(CartItem).where(CartItem.cart_id == user.cart.id)
        cart_items = db.session.scalars(cart_items_query).all()

        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                part=cart_item.part,
                quantity=cart_item.quantity,
            )
            db.session.add(order_item)

        if not user.cart.items:
            flash("Twój koszyk jest pusty!", "warning")
            return redirect(url_for('cart.cart'))

        # Usuń przedmioty z koszyku uzytkownika
        db.session.query(CartItem).filter_by(cart_id=user.cart.id).delete()
        db.session.commit()

        flash("Zamówienie zostało zrealizowane!", "success")
        return redirect(url_for('checkout.view_orders'))

    return render_template('checkout/checkout.html',form=form)


@bp.route('/orders', methods=['GET'])
@login_required
def view_orders():
    user = current_user
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/orders.html', orders=orders)
