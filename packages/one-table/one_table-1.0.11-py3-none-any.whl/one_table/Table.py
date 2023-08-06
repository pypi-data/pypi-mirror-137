import copy
import re
from decimal import Decimal

from cerberus import Validator

from one_table.Utils import get_iso_8601_date


class Table(object):
    def __init__(self, params: dict):
        if 'name' not in params:
            raise Exception('Missing name property')
        self.debug = params.get('debug', False)
        self.table_name = params['name']
        self.schema = params['schema']
        self.models = params['schema']['models']
        self.client = params['client'].Table(params['name'])
        self.pk_key = self.schema['indexes']['primary']['hash']
        self.sk_key = self.schema['indexes']['primary']['sort']

    def prepare_insert_data(self, model, data):
        pass

    def create(self, model, data_):
        _schema = copy.deepcopy(self.models[model])
        sk = self.models[model][self.sk_key]['value']
        pk = self.models[model][self.pk_key]['value']
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        v = Validator(_schema)
        v.validate(data_)
        if v.validate(data_):
            data_[self.pk_key] = pk.format(**data_)
            data_[self.sk_key] = sk.format(**data_)
            data_['createdAt'] = get_iso_8601_date()
            data_['updatedAt'] = get_iso_8601_date()
            data_['_type'] = model
            self.client.put_item(Item=data_)
            return {k: v for k, v in data_.items() if k in _schema.keys()}
        else:
            raise Exception(v.errors)

    def get_model(self, model):
        return self.models[model]

    def update(self, model, data_):
        _schema = copy.deepcopy(self.models[model])
        _data = copy.deepcopy(data_)
        sk = self.models[model][self.sk_key]['value']
        pk = self.models[model][self.pk_key]['value']
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        pk_keys = re.findall(r'\{([A-Za-z0-9_]+)\}', pk)
        sk_keys = re.findall(r'\{([A-Za-z0-9_]+)\}', sk)
        index_keys = pk_keys + sk_keys
        for item in _schema:
            if item in index_keys:
                _schema[item]['required'] = True
            else:
                _schema[item]['required'] = False

        v = Validator(_schema)
        v.validate(data_)
        if v.validate(data_):
            data_key = data_.keys()
            expression_attribute_names = {}
            expression_attribute_values = {}
            update_expression = []
            data_['updated_at'] = get_iso_8601_date()
            for idx, key in enumerate(data_key):
                expression_attribute_names['#k{}'.format(idx)] = key
                expression_attribute_values[':v{}'.format(idx)] = data_[key]
                update_expression.append('#k{} = :v{}'.format(idx, idx))

            pk_key_parsed = pk.format(**data_)
            sk_key_parsed = sk.format(**data_)

            request = {
                'ConditionExpression': '(attribute_exists({})) and (attribute_exists({}))'.format(self.pk_key,
                                                                                                  self.sk_key),
                'ExpressionAttributeNames': expression_attribute_names,
                'ExpressionAttributeValues': expression_attribute_values,
                'UpdateExpression': 'set {}'.format(', '.join(update_expression)),
                'ReturnValues': 'ALL_NEW',
                'Key': {
                    'pk': pk_key_parsed,
                    'sk': sk_key_parsed
                }
            }
            if self.debug:
                print(request)
            response = self.client.update_item(**request)
            # _schema["createdAt"] = ""
            # _schema["updateAt"] = ""
            if 'Attributes' in response:
                return {k: v for k, v in response['Attributes'].items() if k in _schema.keys()}
            return response
        else:
            raise Exception(v.errors)

    def get(self, model, key, value):
        _schema = copy.deepcopy(self.models[model])
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        request = {
            'ExpressionAttributeNames': {
                '#n0': self.schema['indexes']['primary']['hash'],
                '#n1': self.schema['indexes']['primary']['sort'],
                '#_2': key

            },
            'ExpressionAttributeValues': {
                ':v0': '{}#{}'.format(model, value),
                ':v1': '{}#'.format(model),
                ':_2': value

            },
            'FilterExpression': '#_2 = :_2',
            'KeyConditionExpression': '#n0 = :v0 and begins_with(#n1, :v1)',
        }
        _schema["createdAt"] = ""
        _schema["updatedAt"] = ""
        if self.debug:
            print(request)
        response = self.client.query(**request)
        if len(response['Items']) > 0:
            return {k: v for k, v in response['Items'][0].items() if k in _schema.keys()}

        return response['Items']

    def find(self, model, key, value, limit=100, next_key=None):
        _schema = copy.deepcopy(self.models[model])
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        pk = self.models[model][self.pk_key]['value']

        request = {
            'ExpressionAttributeNames': {
                '#n0': self.schema['indexes']['primary']['hash'],
                '#n1': self.schema['indexes']['primary']['sort'],
                '#_2': key

            },
            'ExpressionAttributeValues': {
                ':v0': pk.format(**{key: value}),
                ':v1': '{}#'.format(model),
                ':_2': value

            },
            'FilterExpression': '#_2 = :_2',
            'KeyConditionExpression': '#n0 = :v0 and begins_with(#n1, :v1)',
            "ConsistentRead": False,
            "ScanIndexForward": True,
            "Limit": limit,
        }
        if next_key:
            request['ExclusiveStartKey'] = next_key
        _schema["createdAt"] = ""
        _schema["updatedAt"] = ""
        if self.debug:
            print(request)
        response = self.client.query(**request)
        if len(response['Items']) > 0:
            r = []
            for idx, item in enumerate(response['Items']):
                r.append({k: v for k, v in item.items() if k in _schema.keys()})
            return r

        return response['Items']

    def counter(self, model, action, query):
        _schema = copy.deepcopy(self.models[model])
        action = "+" if action == "increment" else "-"
        request = {"Key": {
            self.pk_key: query[self.pk_key],
            self.sk_key: query[self.sk_key],
        },
            "UpdateExpression": "set #att = #att {} :val".format(action),
            "ExpressionAttributeValues": {
                ':val': Decimal(1)
            },
            'ReturnValues': 'ALL_NEW',
            "ExpressionAttributeNames": {
                "#att": query["key"]
            }}
        if self.debug:
            print(request)
        response = self.client.update_item(**request)
        return response.get('Attributes')

    def find_by_sort_key(self, model: str, query: dict, limit=100, next_key=None):
        _schema = copy.deepcopy(self.models[model])
        del _schema[self.pk_key]
        del _schema[self.sk_key]
        request = {
            'ExpressionAttributeNames': {
                '#n0': self.schema['indexes']['primary']['hash'],
                '#n1': self.schema['indexes']['primary']['sort'],

            },
            'ExpressionAttributeValues': {
                ':v0': '{}'.format(query[self.pk_key]),
                ':v1': '{}'.format(list(query[self.sk_key].values())[0]),

            },
            'KeyConditionExpression': '#n0 = :v0 and {}(#n1, :v1)'.format(list(query[self.sk_key].keys())[0]),
            "ConsistentRead": False,
            "ScanIndexForward": True,
            "Limit": limit,
        }
        if next_key:
            request['ExclusiveStartKey'] = next_key

        _schema["createdAt"] = ""
        _schema["updatedAt"] = ""
        if self.debug:
            print(request)
        response = self.client.query(**request)
        if len(response['Items']) > 0:
            r = []
            for idx, item in enumerate(response['Items']):
                r.append({k: v for k, v in item.items() if k in _schema.keys()})
            return r

        return []

    def delete_by_keys(self, query: dict):
        pk = self.schema['indexes']['primary']['hash']
        sk = self.schema['indexes']['primary']['sort']
        self.client.delete_item(
            Key={
                pk: query[self.pk_key],
                sk: query[self.sk_key],
            }
        )
