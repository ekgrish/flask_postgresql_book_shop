from models import *
from flask import request, redirect, render_template, url_for
from app import app
from app import db
import json


@app.route('/')
def index():
    render_template('routs.html')

    return redirect(url_for('new_magazine'))


@app.route('/new_magazine')
def new_magazine():
    return render_template('new_magazine.html')


# fork for new and for existed with id
@app.route('/magazine', methods=['POST'])
def magazine_actions():
    magazine_dict = {}
    magazine_dict['publising_house_name'] = request.form['publishing_house']
    magazine_dict['title'] = request.form['title']
    magazine_dict['publishing_year'] = request.form['publishing_year']
    magazine_dict['quantity_in_stock'] = request.form['quantity_in_stock']
    magazine_dict['description'] = request.form['description']
    return redirect(url_for('index'))

#TODO: error handler
@app.route('/product/<int:id>', methods=['GET'])
def show_product(id):
    product = Product.query.filter_by(id=id).first().to_json()
    return json.dumps(product)

