# -*- coding: utf-8 -*-

import sys, os, platform
import json
from ecommerce_db import ECommerceDBHelper
from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource

reload(sys) 
sys.setdefaultencoding('utf8')

app = Flask(__name__)
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
        shops_read = []
        result = ECommerceDBHelper().read_shops(shop_id, shops_read)
        return {'type': 'GET', 'result': result, 'data': shops_to_create}, result['errcode']

    # Update shop ==> PUT /shops/<shop_id>
    def put(self, shop_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
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
        result = ECommerceDBHelper().update_shops(shop_id, shops_to_update)
        return {'type': 'PUT', 'result': result, 'data': shops_to_update}, result['errcode']

    # Delete shop ==> DELETE /shops/<shop_id>
    def delete(self, shop_id):
        abort_if_not_authorized()
        shops_deleted = []
        result = ECommerceDBHelper().delete_shops(shop_id, shops_deleted)
        return {'type': 'DELETE', 'result': result, 'data': shops_deleted}, result['errcode']

# Shops
class Shops(Resource):
    # Read shops ==> GET /shops
    def get(self):
        abort_if_not_authorized()
        shops_read = []
        result = ECommerceDBHelper().read_shops(None, shops_read)
        return {'type': 'GET', 'result': result, 'data': shops_read}, result['errcode']

    # Create shop ==> POST /shops
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
            shop_to_update = shops
        elif isinstance(shops, dict) is True:
            shop_to_update.append(shops)
        result = ECommerceDBHelper().create_shops(shops_to_create)
        return {'type': 'POST', 'result': result, 'data': shops_to_create}, result['errcode']

# Product
class Product(Resource):
    # Read product ==> GET /shops/<shop_id>/products/<product_id>
    def get(self, shop_id, product_id):
        abort_if_not_authorized()
        products_read = []
        result = ECommerceDBHelper().read_products(shop_id, product_id, products_read)
        return {'type': 'GET', 'result': result, 'data': products_read}, result['errcode']

    # Update product ==> PUT /shops/<shop_id>/products/<product_id>
    def put(self, shop_id, product_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
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
        result = ECommerceDBHelper().update_products(shop_id, product_id, products_to_update)
        return {'type': 'PUT', 'result': result, 'data': products_to_update}, result['errcode']

    # Delete product ==> DELETE /shops/<shop_id>/products/<product_id>
    def delete(self, shop_id, product_id):
        abort_if_not_authorized()
        products_deleted = []
        result = ECommerceDBHelper().delete_products(shop_id, product_id, products_deleted)
        return {'type': 'DELETE', 'result': result, 'data': products_deleted}, result['errcode']

# Products
class Products(Resource):
    # Read products ==> GET /shops/<shop_id>/products
    def get(self, shop_id):
        abort_if_not_authorized()
        products_read = []
        result = ECommerceDBHelper().read_products(shop_id, None, products_read)
        return {'type': 'GET', 'result': result, 'data': products_read}, result['errcode']

    # Create product ==> POST /shops/<shop_id>/products
    def post(self, shop_id):
        abort_if_not_authorized()
        args = parser.parse_args()
        content_type = args.get('Content-Type', 'application/json')
        accept_type = args.get('Accept', 'application/json')
        products_to_create = []
        if 'application/x-www-form-urlencoded' in content_type or 'application/x-www-form-urlencoded' in accept_type:
            products = request.form
        elif 'application/json' in content_type or 'application/json' in accept_type:
            products = request.json
        else:
            products = request.json
        if isinstance(products, list) is True:
            products_to_create = products
        elif isinstance(products, dict) is True:
            products_to_create.append(products)
        result = ECommerceDBHelper().create_products(shop_id, products_to_create)
        return {'type': 'POST', 'result': result, 'data': products_to_create}, result['errcode']

# Actually setup the Api resource routing here
api.add_resource(Shops, '/ecapi/v1/shops')
api.add_resource(Shop, '/ecapi/v1/shops/<shop_id>')
api.add_resource(Products, '/ecapi/v1/shops/<shop_id>/products')
api.add_resource(Product, '/ecapi/v1/shops/<shop_id>/products/<product_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
