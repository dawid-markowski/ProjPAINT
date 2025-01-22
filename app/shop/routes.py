from app.shop import bp
from app import db
import sqlalchemy as sa
from app.models import Part, Cart, CartItem
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user



@bp.route('/parts', methods=['GET'])
@login_required
def parts():
    search_query = request.args.get('search', '')  # Pobieramy parametr "search" z URL
    if search_query:
        parts = db.session.scalars(sa.select(Part).where(sa.func.lower(Part.part_name).like(sa.func.lower(f'%{search_query}%')))).all()  # Wyszukiwanie po nazwie, podstawowe
    else:
        parts = db.session.scalars(sa.select(Part)).all()
    return render_template('shop/parts.html', title='Czesci Samochodowe', parts=parts)


@bp.route('/parts/<part>', methods=['GET', 'POST'])
@login_required
def part(part):
    query = sa.select(Part).where(Part.part_name == part)
    part= db.session.scalars(query).first()
    return render_template('shop/part.html',part=part)

