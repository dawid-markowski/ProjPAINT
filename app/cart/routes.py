from app.models import Part,Cart, CartItem
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request
from app import db
from app.cart import bp
import sqlalchemy as sa



@bp.route('/add_to_cart/<int:part_id>', methods=['POST'])
@login_required
def add_to_cart(part_id):
    user = current_user
    part = Part.query.get(part_id)
    if not part:
        return "Part not found", 404

    quantity = int(request.form.get('quantity', 1))

    # Utwórz koszyk, jeśli go nie ma
    if not user.cart:
        user.cart = Cart(user=user)
        db.session.add(user.cart)

    # Sprawdź, czy część jest już w koszyku
    cart_item = CartItem.query.filter_by(cart_id=user.cart.id, part_id=part_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart=user.cart, part=part, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('shop.part', part=part.part_name))


@bp.route('/cart', methods=['GET'])
@login_required
def view_cart():
    if not current_user.cart:
        return render_template('cart/cart.html', cart_items=None)

    # Pobierz elementy koszyka z bazy danych
    query = sa.select(CartItem).where(CartItem.cart_id == current_user.cart.id).options(
        sa.orm.joinedload(CartItem.part)  # Ładowanie powiązanej części
    )
    cart_items = db.session.scalars(query).all()

    cart = db.session.scalar(sa.select(Cart).where(CartItem.cart_id == Cart.id))

    return render_template('cart/cart.html', cart_items=cart_items,cart=cart)


@bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    # Pobierz CartItem z powiązanym obiektem part
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=current_user.cart.id).first()

    if cart_item:
        # Zapisz powiązany part w zmiennej przed usunięciem
        part_name = cart_item.part.part_name

        # Usuń CartItem
        db.session.delete(cart_item)
        db.session.commit()

        # Potwierdzenie usunięcia
        return redirect(url_for('cart.view_cart'))
    else:
        return 'Item not found in cart!', 404