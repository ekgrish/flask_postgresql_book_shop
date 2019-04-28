from urllib import parse
from urllib.parse import urlparse
from models import *
from app import logger
from sqlalchemy import text


class postDataHelper(object):

    def __init__(self, possible_params=['num']):
        self.possible_params = possible_params

    def post_data(self, url, id):
        parsed_params = self.parse_params(url)
        if parsed_params.get('error'):
            return parsed_params

        product = Product.query.filter_by(id=id)
        old = product.first_or_404().to_json()
        product = Product.query.filter_by(id=id).update(parsed_params)
        new = Product.query.filter_by(id=id).first().to_json()

        return {"old": old, "new": new}

    def parse_params(self, url):
        row_params = parse.parse_qs(urlparse(url).query)
        check_result = self.check_params(row_params)
        if check_result:
            logger.error(check_result.get('error'))
            return check_result

        parsed_params = {'quantity_in_stock': int(row_params.get('num')[0])}

        return parsed_params

    def check_params(self, parsed_result):
        possible_params_set = set(self.possible_params)
        received_params_set = set(parsed_result.keys())
        if not (received_params_set.issubset(possible_params_set)):
            differ_params = received_params_set.difference(possible_params_set)
            return {"error": "There are not possible params in request {}".format(differ_params)}
        return 0

# ?type=книга&author=Несуществующий&publishing_house=Издательство&publishing_year=1994&availability=True&order_by=type&reverse=True
