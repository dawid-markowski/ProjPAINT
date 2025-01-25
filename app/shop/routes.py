from app.shop import bp
from app import db
import sqlalchemy as sa
from app.models import Part, Cart, CartItem
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user



@bp.route('/parts', methods=['GET'])
@login_required
def parts():
    # Pobieramy parametry z URL
    search_query = request.args.get('search', '')
    selected_categories = request.args.getlist('categories')
    sort_option = request.args.get('sort', 'asc')

    query = sa.select(Part)

    if search_query:
        query = query.where(sa.func.lower(Part.part_name).like(sa.func.lower(f'%{search_query}%')))

    if selected_categories and 'all' not in selected_categories:
        query = query.where(Part.group.in_(selected_categories))

    if sort_option == 'asc':
        query = query.order_by(Part.price.asc())
    elif sort_option == 'desc':
        query = query.order_by(Part.price.desc())

    parts = db.session.scalars(query).all()

    return render_template('shop/parts.html', title='Części Samochodowe', parts=parts)


@bp.route('/parts/<part>', methods=['GET', 'POST'])
@login_required
def part(part):
    query = sa.select(Part).where(Part.part_name == part)
    part= db.session.scalars(query).first()
    return render_template('shop/part.html',part=part)

