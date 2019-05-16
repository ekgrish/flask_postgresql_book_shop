from urllib import parse
from urllib.parse import urlparse
from models import *
from sqlalchemy import text
from app import logger


class GetDataHelper(object):

    def __init__(self, possible_params_order=['order_by', 'reverse'],
                 possible_params_order_by=['type', 'author', 'publishing_house',
                                              'publishing_year', 'availability']):
        self.possible_params_order = possible_params_order
        self.possible_params_order_by = possible_params_order_by
        self.possible_params = possible_params_order + possible_params_order_by

    def get_data(self, url):

        parsed_params = self.parse_params(url)
        if parsed_params.get('error'):
            return parsed_params

        filter_params = parsed_params.get('filter')
        order_params = parsed_params.get('order')

        # TODO filter by author
        try:
            products_query = Product.query.filter_by(**filter_params)
        except Exception as e:
            return {"error": e}

        if order_params:
            request_str = order_params['order_by']
            if order_params.get('reverse'):
                request_str = request_str + ' desc'
            products_query = products_query.order_by(text(request_str))

        products = [product.to_json() for product in products_query.all()]

        return products

    def parse_params(self, url):
        row_params = parse.parse_qs(urlparse(url).query)
        check_result = self.check_params(row_params)
        if check_result:
            logger.error(check_result.get('error'))
            return check_result

        parsed_params = self.form_dict_for_query(row_params)

        return parsed_params

    def check_params(self, parsed_result):
        possible_params_set = set(self.possible_params)
        received_params_set = set(parsed_result.keys())
        if not (received_params_set.issubset(possible_params_set)):
            differ_params = received_params_set.difference(possible_params_set)
            return {"error": "There are not possible params in request {}".format(differ_params)}
        else:
            if 'order_by' in parsed_result and parsed_result['order_by'] in self.possible_params_order_by:
                return {
                    "error": "There are not possible params in request.order_by {}".format(parsed_result['order_by'])}

        # TODO check corret availability and reverse
        # TODO check if there are reverse, but there is no order_by

        return 0

    def form_dict_for_query(self, row_params):
        formed_result_filter = self.form_dict_for_filter(row_params)
        formed_result_order = self.form_dict_for_order(row_params)

        return {"filter": formed_result_filter, "order": formed_result_order}

    def form_dict_for_filter(self, row_params):
        formed_result_filter = {}
        # TODO check if number value is not possible to convert
        if row_params.get('title'):
            formed_result_filter['title'] = int(row_params['title'][0])
        if row_params.get('publishing_year'):
            formed_result_filter['publishing_year'] = int(row_params['publishing_year'][0])
        if row_params.get('type'):
            formed_result_filter['type_id'] = Type.query.filter_by(product_type=row_params['type'][0]).first().id
        if row_params.get('publishing_house'):
            formed_result_filter['publishing_house_id'] = PublishingHouse.query.filter_by(
                name=row_params['publishing_house'][0]).first().id
        # TODO for authors
        return formed_result_filter

    def form_dict_for_order(self, row_params):
        formed_result_order = {}
        # TODO check if number value is not possible to convert
        # TODO: loggigng here
        if row_params.get('order_by'):
            formed_result_order['order_by'] = row_params['order_by'][0]
        if row_params.get('reverse'):
            formed_result_order['reverse'] = bool(row_params['reverse'][0])

        return formed_result_order

# ?type=книга&author=Несуществующий&publishing_house=Издательство&publishing_year=1994&availability=True&order_by=type&reverse=True
