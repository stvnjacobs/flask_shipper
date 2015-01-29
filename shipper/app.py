import os
import sys
import logging
import locale
import easypost
import newrelic.agent

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask.ext.assets import Environment, Bundle
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = os.environ['WTF_CSRF_ENABLED']
app.config['SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']
assets = Environment(app)

locale.setlocale( locale.LC_ALL, '')

easypost.api_key = os.environ['EASYPOST_TEST_KEY']

js = Bundle(
    'vendor/jquery/dist/jquery.min.js',
    'vendor/bootstrap/dist/js/bootstrap.min.js',
    'scripts/main.js',
    'scripts/dev.js',
    output='dist/bundle.js')
assets.register('js_all', js)

css = Bundle(
    'vendor/normalize.css/normalize.css',
    'vendor/bootstrap/dist/css/bootstrap.css',
    'styles/main.scss',
    filters='pyscss',
    output='dist/bundle.css')
assets.register('css_all', css)

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


@app.route('/')
def index():
    return redirect(url_for('create_shipment'))
    
@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/login')
# def login():
#     flash('Login has not yet been set up.')
#     return redirect(url_for('index'))

@app.route('/ship/')
def create_shipment():
    flash('This is a work in progress.  For more info, follow the About link above')
    flash('The forms are are auto filled simply to speed up development and testing.  Feel free to change to your hearts content!')

    parcel_form = Parcel()
    carriers = ['USPS', 'UPS']

    return render_template(
        '_ship_form.html',
        parcel_form=parcel_form,
        carriers=carriers
    )

@app.route('/rates/', methods=['POST'])
def rate_options():
    if request.method == 'POST':

        # if request.form['predefined_package'] == '':

        sender_address = {}
        sender_address['name'] = request.form['sender_name']
        sender_address['company'] = request.form['sender_company']
        sender_address['street1'] = request.form['sender_address1']
        sender_address['street2'] = request.form['sender_address2']
        sender_address['city'] = request.form['sender_city']
        sender_address['state'] = request.form['sender_state']
        sender_address['zip'] = request.form['sender_zip_code']

        receiver_address = {}
        receiver_address['name'] = request.form['receiver_name']
        receiver_address['company'] = request.form['receiver_company']
        receiver_address['street1'] = request.form['receiver_address1']
        receiver_address['street2'] = request.form['receiver_address2']
        receiver_address['city'] = request.form['receiver_city']
        receiver_address['state'] = request.form['receiver_state']
        receiver_address['zip'] = request.form['receiver_zip_code']

        parcel = {}
        parcel['length'] = request.form['length']
        parcel['width'] = request.form['width']
        parcel['height'] = request.form['height']
        parcel['weight'] = request.form['weight']
        # parcel['predefined_package'] = request.form['predefined_package']

        carriers = request.form.getlist('carrier')

        shipment = easypost.Shipment.create(
            to_address = receiver_address,
            from_address = sender_address,
            parcel = parcel
        )

        shipment_id = shipment.id

        # if request.form['buy_lowest'] == 'true':
        #     rate = shipment.lowest_rate()

        options = []

        for rate in shipment.rates:
            d = {}
            d['carrier'] = rate.carrier
            d['service'] = rate.service
            d['rate'] = locale.currency(float(rate.rate), grouping=True)
            d['id'] = rate.id
            d['guaranteed'] = rate.delivery_date_guaranteed
            d['days'] = rate.delivery_days
            options.append(d)

    return render_template(
        '_price_table.html',
        carriers=carriers,
        shipment=shipment,
        shipment_id=shipment_id,
        options=options,
        receiver_address=receiver_address,
        sender_address=sender_address,
        parcel=parcel
    )

@app.route('/rate/', methods=['POST'])
def show_rate():
    if request.method == 'POST':
        shipment_id = request.form['shipment_id']
        rate_id = request.form['rate']

        shipment = easypost.Shipment.retrieve(shipment_id)

    return render_template('_rate_details.html',
                            shipment_id=shipment_id,
                            rate_id=rate_id)

if __name__ == '__main__':
    # app.debug = True
    # app.run(host='0.0.0.0')
    app = newrelic.agent.wsgi_application()(app)
    app.run()
