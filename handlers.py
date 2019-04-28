import json

#from flask import make_response, abort
from flask import request, redirect, render_template, url_for
#from sqlalchemy import orm
import logging
from app import app
from models import *
from get_data_helper import get_data_helper
from post_data_helper import postDataHelper

logger = logging.getLogger()
get_data_helper = get_data_helper()
post_data_helper = postDataHelper()
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_magazine')
def new_magazine():
    return render_template('new_magazine.html')


# TODO: error handler
@app.route('/product/<int:product_id>', methods=['GET'])
def show_product(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404().to_json()
    app.logger.info('Get product with id=%s:successfully', product_id)
    return json.dumps(product)

# /product/1?num=6
@app.route('/product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    result = postDataHelper.post_data(request.url, id)
    app.logger.info('Update product availability with id=%s:successfully', product_id)
    return json.dumps(result)

#?type=книга&author=Несуществующий&publishing_house=Издательство&publishing_year=1994&availability=True&order_by=type&reverse=True
@app.route('/products', methods=['GET'])
def show_products():
    result = get_data_helper.get_data(request.url)
    app.logger.info('Show products:successfully')
    return json.dumps(result)
