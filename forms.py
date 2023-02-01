from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError, DateField
from wtforms.fields import IntegerField, SelectField
import datetime

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')


class NewCustomerForm(FlaskForm):
    GivenName = StringField('name', validators=[validators.DataRequired()])
    Surname = StringField('name', validators=[validators.DataRequired()])
    City = StringField('city', validators=[validators.DataRequired()])
    Streetaddress = StringField('streetaddress', validators=[validators.DataRequired()])
    Zipcode = IntegerField('zipcode', validators=[validators.DataRequired()])
    Country = StringField('streetaddress', validators=[validators.DataRequired()])
    NationalId = IntegerField('zipcode', validators=[validators.DataRequired()])
    CountryCode = SelectField('countryCode',choices=[('46','+46'),('41','+41'),('42','+42')])
    Birthday = DateField('Birthday', validators=[validators.DataRequired()])
    EmailAddress = StringField('emailaddress', validators=[validators.DataRequired()])
    Telephone = StringField('Telephone', validators=[validators.DataRequired()])

