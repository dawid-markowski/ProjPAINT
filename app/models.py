from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    comments: so.WriteOnlyMapped['Comment'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Part(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    part_name: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                                 unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(240),index=True,
                                                   unique=True)

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