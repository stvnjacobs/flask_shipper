from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Parcel(Form):
    sender_name = StringField('Full Name')
    sender_company = StringField('Company')
    sender_address1 = StringField('Address 1', validators=[DataRequired()])
    sender_address2 = StringField('Address 2')
    sender_city = StringField('City', validators=[DataRequired()])
    sender_state = StringField('State', validators=[DataRequired()])
    sender_zip_code = StringField('Zip', validators=[DataRequired()])
    receiver_name = StringField('Full Name')
    receiver_company = StringField('Company')
    receiver_address1 = StringField('Address 1', validators=[DataRequired()])
    receiver_address2 = StringField('Address 2')
    receiver_city = StringField('City', validators=[DataRequired()])
    receiver_state = StringField('State', validators=[DataRequired()])
    receiver_zip_code = StringField('Zip', validators=[DataRequired()])
    length = IntegerField('Length <small>(inches)</small>')
    width = IntegerField('Width <small>(inches)</small>')
    height = IntegerField('Height <small>(inches)</small>')
    weight = IntegerField('Weight <small>(ounces)</small>')