# -*- coding: utf-8 -*-

import sys, os, platform
import json
from ecommerce_db import ECommerceDBHelper
from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource
from flask_cors import *

reload(sys) 
sys.setdefaultencoding('utf8')

app = Flask(__name__)
CORS(app, supports_credentials=True);
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('Content-Type', location='headers')
parser.add_argument('Accept', location='headers')

# Abort if not authorized
def abort_if_not_authorized():
    pass

# Shop
class Shop(Resource):
    # Read shop ==> GET /shops/<shop_id>
    def get(self, shop_id):
        abort_if_not_authorized()
        shop_ids_to_read = []
        shop_ids_to_read.append(shop_id)
        shops_read = []
        result = ECommerceDBHelper().read_shops(shop_ids_to_read, shops_read)
        return {'type': 'GET', 'result': result, 'data': shops_to_create}, result['errcode']

    # Update shop ==> PUT /shops/<shop_id>
    def put(self, shop_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        shop_ids_to_update = []
        shop_ids_to_update.append(shop_id)
        shops_to_update = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            shop = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            shop = request.json
        else:
            shop = request.json
        if isinstance(shop, list) is True:
            shops_to_update = shop
        elif isinstance(shop, dict) is True:
            shops_to_update.append(shop)
        result = ECommerceDBHelper().update_shops(shop_ids_to_update, shops_to_update)
        return {'type': 'PUT', 'result': result, 'data': shops_to_update}, result['errcode']

    # Delete shop ==> DELETE /shops/<shop_id>
    def delete(self, shop_id):
        abort_if_not_authorized()
        shop_ids_to_delete = []
        shop_ids_to_delete.append(shop_id)
        shops_deleted = []
        result = ECommerceDBHelper().delete_shops(shop_ids_to_delete, shops_deleted)
        return {'type': 'DELETE', 'result': result, 'data': shops_deleted}, result['errcode']

# Shops
class Shops(Resource):
    # Read shops ==> GET /shops
    def get(self):
        abort_if_not_authorized()
        shops_read = []
        result = ECommerceDBHelper().read_shops(None, shops_read)
        return {'type': 'GET', 'result': result, 'data': shops_read}, result['errcode']

    # Create shops ==> POST /shops
    def post(self):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        shops_to_create = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            shops = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            shops = request.json
        else:
            shops = request.json
        if isinstance(shops, list) is True:
            shops_to_create = shops
        elif isinstance(shops, dict) is True:
            shops_to_create.append(shops)
        result = ECommerceDBHelper().create_shops(shops_to_create)
        return {'type': 'POST', 'result': result, 'data': shops_to_create}, result['errcode']

    # Update shops ==> PUT /shops
    def put(self):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        shops_to_update = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            shops = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            shops = request.json
        else:
            shops = request.json
        if isinstance(shops, list) is True:
            shops_to_update = shops
        elif isinstance(shops, dict) is True:
            shops_to_update.append(shops)
        result = ECommerceDBHelper().update_shops(None, shops_to_update)
        return {'type': 'PUT', 'result': result, 'data': shops_to_create}, result['errcode']

    # Delete shops ==> DELETE /shops
    def delete(self):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        shop_ids_to_delete = []
        shops_deleted = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            shop_ids = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            shop_ids = request.json
        else:
            shop_ids = request.json
        if isinstance(shop_ids, list) is True:
            shop_ids_to_delete = shop_ids
        elif isinstance(shop_ids, dict) is True:
            shop_ids_to_delete.append(shop_ids)
        result = ECommerceDBHelper().delete_shops(shop_ids_to_delete, shops_deleted)
        return {'type': 'DELETE', 'result': result, 'data': shops_deleted}, result['errcode']

# Product
class Product(Resource):
    # Read product ==> GET /shops/<shop_id>/products/<product_id>
    def get(self, shop_id, product_id):
        abort_if_not_authorized()
        product_ids_to_read = []
        product_ids_to_read.append(product_id)
        products_read = []
        result = ECommerceDBHelper().read_products(shop_id, product_ids_to_read, products_read)
        return {'type': 'GET', 'result': result, 'data': products_read}, result['errcode']

    # Update product ==> PUT /shops/<shop_id>/products/<product_id>
    def put(self, shop_id, product_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        product_ids_to_update = []
        product_ids_to_update.append(product_id)
        products_to_update = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            product = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            product = request.json
        else:
            product = request.json
        if isinstance(product, list) is True:
            products_to_update = product
        elif isinstance(product, dict) is True:
            products_to_update.append(product)
        result = ECommerceDBHelper().update_products(shop_id, product_ids_to_update, products_to_update)
        return {'type': 'PUT', 'result': result, 'data': products_to_update}, result['errcode']

    # Delete product ==> DELETE /shops/<shop_id>/products/<product_id>
    def delete(self, shop_id, product_id):
        abort_if_not_authorized()
        product_ids_to_delete = []
        product_ids_to_delete.append(product_id)
        products_deleted = []
        result = ECommerceDBHelper().delete_products(shop_id, product_ids_to_delete, products_deleted)
        return {'type': 'DELETE', 'result': result, 'data': products_deleted}, result['errcode']

# Products
class Products(Resource):
    # Read products ==> GET /shops/<shop_id>/products
    def get(self, shop_id):
        abort_if_not_authorized()
        products_read = []
        result = ECommerceDBHelper().read_products(shop_id, None, products_read)
        return {'type': 'GET', 'result': result, 'data': products_read}, result['errcode']

    # Create products ==> POST /shops/<shop_id>/products
    def post(self, shop_id):
        abort_if_not_authorized()
        return {'type': 'POST', 'result': {'errcode': StatusCode.FORBIDDEN.value, 'errmsg': 'you are forbidden to create product(s)'}, 'data': null}, StatusCode.FORBIDDEN.value

    # Update products ==> PUT /shops/<shop_id>/products
    def put(self, shop_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        products_to_update = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            products = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            products = request.json
        else:
            products = request.json
        if isinstance(products, list) is True:
            products_to_update = products
        elif isinstance(products, dict) is True:
            products_to_update.append(products)
        result = ECommerceDBHelper().update_products(shop_id, None, products_to_update)
        return {'type': 'PUT', 'result': result, 'data': products_to_update}, result['errcode']

    # Delete products ==> DELETE /shops/<shop_id>/products
    def delete(self, shop_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        product_ids_to_delete = []
        products_deleted = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            product_ids = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            product_ids = request.json
        else:
            product_ids = request.json
        if isinstance(product_ids, list) is True:
            product_ids_to_delete = product_ids
        elif isinstance(product_ids, dict) is True:
            product_ids_to_delete.append(product_ids)
        result = ECommerceDBHelper().delete_products(shop_id, product_ids_to_delete, products_deleted)
        return {'type': 'DELETE', 'result': result, 'data': products_deleted}, result['errcode']

# Actually setup the Api resource routing here
api.add_resource(Shops,     '/ecapi/v1/shops')
api.add_resource(Shop,      '/ecapi/v1/shops/<shop_id>')
api.add_resource(Products,  '/ecapi/v1/shops/<shop_id>/products')
api.add_resource(Product,   '/ecapi/v1/shops/<shop_id>/products/<product_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
