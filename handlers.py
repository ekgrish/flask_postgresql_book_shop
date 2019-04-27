import json

from flask import make_response
from flask import request, redirect, render_template, url_for, jsonify, abort
from sqlalchemy import orm

from app import app
from models import *
from get_data_helper import get_data_helper

get_data_helper = get_data_helper()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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


# TODO: error handler
@app.route('/product/<int:id>', methods=['GET'])
def show_product(id):
    try:
        product = Product.query.filter_by(id=id).first().to_json()
    except orm.exc.NoResultFound:
        abort(404)
    except Exception as e:
        pass
        # abort(209)
    return json.dumps(product)


# /products?filter=type&value=книга
# /products?filter=author&value=Несуществующий
# /products?filter=publishing_house&value=Издательство
# /products?filter=publishing_year&value=Издательство
# /products?filter=availability&value=True
# TODO: error handler
#?type=книга&author=Несуществующий&publishing_house=Издательство&publishing_year=1994&availability=True&order_by=type&reverse=True

@app.route('/products', methods=['GET'])
def show_products():
    result = get_data_helper.get_data(request.url)

    return json.dumps(result)
