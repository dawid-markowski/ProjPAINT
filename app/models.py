from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from app import app
from time import time


class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    is_admin = so.mapped_column(sa.Boolean, default=False)

    comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        back_populates='author')
    cart: so.Mapped['Cart'] = so.relationship('Cart', back_populates='user', uselist=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Part(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    part_name: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                                 unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(240),index=True,
                                                   unique=True)
    #group: so.Mapped[str] = so.mapped_column(sa.String(64),index=True)

    comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        back_populates='p_commented')

    def __repr__(self):
        return '<Part {}>'.format(self.part_name)

class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(360), index=True,
                                            unique=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Part.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='comments')
    p_commented: so.Mapped[Part] = so.relationship(back_populates='comments')
    def __repr__(self):
        return '<Comment {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return db.session.get(User,int(id))


class Cart(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, unique=True)
    user: so.Mapped[User] = so.relationship('User', back_populates='cart')
    items: so.WriteOnlyMapped['CartItem'] = so.relationship('CartItem', back_populates='cart', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cart of User {self.user_id}>'

class CartItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    cart_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Cart.id), index=True)
    part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Part.id), index=True)
    quantity: so.Mapped[int] = so.mapped_column(default=1)

    cart: so.Mapped[Cart] = so.relationship('Cart', back_populates='items')
    part: so.Mapped[Part] = so.relationship('Part')

    def __repr__(self):
        return f'<CartItem {self.quantity}x {self.part.part_name} in Cart {self.cart_id}>'