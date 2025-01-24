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
    #print(f"DEBUG: request.form = {request.form}")  # Dodaj na początku funkcji
    user = current_user

    if not user.cart or not user.cart.items:
        flash("Twój koszyk jest pusty!", "warning")
        return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()
    #print(f"DEBUG: form.validate_on_submit() = {form.validate_on_submit()}")  # Dodaj debugowanie
    if form.validate_on_submit():
        payment_method = request.form.get('payment_method')
        delivery_method = form.delivery_method.data
        #print(f"DEBUG: payment_method (from request.form) = {payment_method}")
        # Utwórz zamówienie
        order = Order(
            user=user,
            address=form.address.data,
            city=form.city.data,
            postal_code=form.postal_code.data,
            status='pending',
            payment_method = payment_method,
            delivery_method = delivery_method
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

        if payment_method == 'card':
            flash("Platnosc karta powiodla sie", "info")
            # Tutaj kod do przekierowania do bramki płatności
            return redirect(url_for('checkout.view_orders', order_id=order.id))  # Przykładowe przekierowanie
        elif payment_method == 'blik':
            flash("Platnosc blikiem powiodla sie", "info")
            # Tutaj kod do wygenerowania kodu BLIK i wyświetlenia instrukcji
            return redirect(url_for('checkout.view_orders', order_id=order.id))
        elif payment_method == 'pbr':
            #print("DEBUG: Obsługa płatności za pobraniem")  # Dodaj debugowanie
            flash("Zamówienie za pobraniem zostało złożone.", "success")
            return redirect(url_for('checkout.view_orders'))
        else:
            flash("Nieznana metoda płatności", "error")
            return redirect(url_for('cart.view_cart'))

    return render_template('checkout/checkout.html',form=form)


@bp.route('/orders', methods=['GET'])
@login_required
def view_orders():
    user = current_user
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/orders.html', orders=orders)
