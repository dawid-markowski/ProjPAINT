from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class CheckoutForm(FlaskForm):
    address = StringField("Adres", validators=[DataRequired(), Length(max=255)])
    city = StringField("Miasto", validators=[DataRequired(), Length(max=100)])
    postal_code = StringField("Kod pocztowy", validators=[DataRequired(), Length(max=20)])
    payment_method = SelectField('Metoda płatności',choices=[('card', 'Karta'), ('blik', 'BLIK'), ('pbr', 'Za pobraniem')],validators=[DataRequired()])
    card_number = StringField('Numer karty', validators=[Optional(), Length(min=16, max=19)])
    expiration_date = StringField('Data ważności',validators=[Optional(), Regexp(r'^\d{2}/\d{2}$', message="Format MM/YY")])
    cvv = StringField('CVV', validators=[Optional(), Length(min=3, max=4)])
    blik_code = StringField('Kod BLIK',validators=[Optional(), Length(min=6, max=6, message="Kod BLIK musi mieć 6 cyfr")])
    submit = SubmitField("Złóż zamówienie")

    def validate(self, extra_validators=None):
        print(f"DEBUG: self = {self}")
        print(f"DEBUG: hasattr(self, 'blik_code') = {hasattr(self, 'blik_code')}")


        initial_validation = super(CheckoutForm, self).validate(extra_validators=extra_validators)
        if not initial_validation:
            return False

        if self.payment_method.data == 'card':
            if not self.card_number.data or not self.expiration_date.data or not self.cvv.data:
                if not self.card_number.data:
                    self.card_number.errors.append('Numer karty jest wymagany przy płatności kartą.')
                if not self.expiration_date.data:
                    self.expiration_date.errors.append('Data ważności jest wymagana przy płatności kartą.')
                if not self.cvv.data:
                    self.cvv.errors.append('CVV jest wymagany przy płatności kartą.')
                return False

        elif self.payment_method.data == 'blik':
            if not self.blik_code.data:
                self.blik_code.errors.append('Kod BLIK jest wymagany przy płatności BLIK.')
                return False

        return True