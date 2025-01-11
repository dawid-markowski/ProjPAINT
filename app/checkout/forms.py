from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CheckoutForm(FlaskForm):
    address = StringField("Adres", validators=[DataRequired(), Length(max=255)])
    city = StringField("Miasto", validators=[DataRequired(), Length(max=100)])
    postal_code = StringField("Kod pocztowy", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Złóż zamówienie")
