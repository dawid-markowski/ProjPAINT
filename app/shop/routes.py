from app.shop import bp
from app import db
import sqlalchemy as sa
from app.models import Part, Cart, CartItem
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user



@bp.route('/parts')
@login_required
def parts():
    parts = db.session.scalars(sa.select(Part)).all()
    return render_template('shop/parts.html', title='Czesci Samochodowe', parts=parts)


@bp.route('/parts/<part>', methods=['GET', 'POST'])
@login_required
def part(part):
    print(part)
    query = sa.select(Part).where(Part.part_name == part)
    part= db.session.scalars(query).first()
    return render_template('shop/part.html',part=part)

