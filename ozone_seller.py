import requests


class OzoneSeller:

    def __init__(self, data):
        self.id = data['id']
        self.key = data['key']
        self.url = data['url']
        self.version = data['version']

    def get_headers(self):
        return {
            'Client-id': self.id,
            'Api-Key': self.key,
        }

    def get_actions(self):
        '''Получение всех акций'''
        result = self.do_request('get', '/actions', {})
        all_actions = result['result'] if result['flag'] else {}
        return all_actions

    def get_candidates(self, action_id):
        '''Получение товаров подходящих к акции'''
        params = {
            "action_id": action_id,
            "limit": 10,
            "offset": 0,
        }
        result = self.do_request('post', '/actions/candidates', params)
        candidates = result['result']['products'] if result['flag'] else {}
        return candidates

    def add_product_to_action(self, action_id, product_id, action_price, stock):
        '''Добавление продукта к акции'''
        url = self.url + self.version + "/actions/products/activate"
        params = {
            "action_id": action_id,
            "products": [
                {
                    "action_price": action_price,
                    "product_id": product_id,
                    "stock": stock,
                }
            ]
        }
        result = self.do_request('post', '/actions/products/activate', params)
        products_actions = result['result']['product_ids'] if result['flag'] else {}
        return products_actions

    def do_request(self, type_request, type, params):
        '''Выполнение запросов'''
        url = self.url + self.version + type
        headers = self.get_headers()
        if type_request == 'get':
            result = requests.get(url, headers=headers)
        else:
            result = requests.post(url, headers=headers, params=params)
        if result.status_code == 200:
            return {'flag': True,  'result': result.json()['result']}
        else:
            print(result.json()['message'])
            return {'flag': False, 'result': {}}

