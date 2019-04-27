from urllib import parse
from urllib.parse import urlparse
from models import *
from sqlalchemy import asc, desc, text


class get_data_helper(object):

    def __init__(self, possible_parametrs_order=['order_by', 'reverse'],
                 possible_parametrs_order_by=['type', 'author', 'publishing_house',
                                              'publishing_year', 'availability']):
        self.possible_parametrs_order = possible_parametrs_order
        self.possible_parametrs_order_by = possible_parametrs_order_by
        self.possible_parametrs = possible_parametrs_order + possible_parametrs_order_by

    def parse_parametrs(self, url):
        parsed_params = parse.parse_qs(urlparse(url).query)
        check_result = self.check_parametrs(parsed_params)
        if check_result:
            return check_result

        formed_params = self.form_dict_for_query(parsed_params)
        try:
            kwargs = formed_params.get('filter')
            products_query = Product.query.filter_by(**kwargs)
        except Exception as e:
            return {"error": e}

        if formed_params.get('order'):
            if formed_params['order'].get('reverse'):
                request_str = formed_params['order']['order_by'] + ' desc'
            else:
                request_str = formed_params['order']['order_by']
            products_query = products_query.order_by(text(request_str))

        products_json = [product.to_json() for product in products_query.all()]

        return products_json

    def check_parametrs(self, parsed_result):
        possible_params_set = set(self.possible_parametrs)
        received_params_set = set(parsed_result.keys())
        if not (received_params_set.issubset(possible_params_set)):
            differ_params = received_params_set.difference(possible_params_set)
            return {"error": "There Productare not possible params in request {}".format(differ_params)}
        else:
            if 'order_by' in parsed_result and parsed_result['order_by'] in self.possible_parametrs_order_by:
                return {
                    "error": "There are not possible params in request.order_by {}".format(parsed_result['order_by'])}

        # TODO check corret availability and reverse

        return 0

    def form_dict_for_query(self, parsed_result):
        formed_result_filter = {}
        formed_result_order = {}
        if parsed_result.get('title'):
            formed_result_filter['title'] = int(parsed_result['title'][0])
        if parsed_result.get('publishing_year'):
            formed_result_filter['publishing_year'] = int(parsed_result['publishing_year'][0])
        if parsed_result.get('type'):
            formed_result_filter['type_id'] = Type.query.filter_by(product_type=parsed_result['type'][0]).first().id
        if parsed_result.get('publishing_house'):
            formed_result_filter['publishing_house_id'] = PublishingHouse.query.filter_by(
                name=parsed_result['publishing_house'][0]).first().id
        #TODO for authors

        if parsed_result.get('order_by'):
            formed_result_order['order_by'] = parsed_result['order_by'][0]
        if parsed_result.get('reverse'):
            formed_result_order['reverse'] = bool(parsed_result['reverse'][0])
        # TODO: str to num
        # TODO str to bool
        return {"filter": formed_result_filter, "order": formed_result_order}

# ?type=книга&author=Несуществующий&publishing_house=Издательство&publishing_year=1994&availability=True&order_by=type&reverse=True
