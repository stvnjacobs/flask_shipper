import os
import sys
import logging
import locale
import easypost
import newrelic.agent
from helpers.weights import convert_weight_to_oz

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask.ext.assets import Environment, Bundle

from forms.parcel import Parcel

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
    flash('This is a work in progress.  More info is on the <a href="/about">About</a> page.')
    flash('The forms are auto filled to speed up development and testing.  If you come from the internet, feel free to clear them and try it out!')

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
        if request.form['weight-unit'] == 'oz':
            parcel['weight'] = request.form['weight']
        else:
            parcel['weight'] = convert_weight_to_oz(float(request.form['weight']), request.form['weight-unit'])
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
