from app.shop import bp
from app import db
import sqlalchemy as sa
from app.models import Part
from flask import render_template
from flask_login import login_required


@bp.route('/parts')
@login_required
def parts():
    parts = db.session.scalars(sa.select(Part)).all()
    return render_template('shop/parts.html', title='Czesci Samochodowe', parts=parts)


@bp.route('/parts/<part>')
@login_required
def part(part):
    query = sa.select(Part).where(Part.part_name == part)
    part= db.session.scalars(query).first()
    return render_template('shop/part.html',part=part)