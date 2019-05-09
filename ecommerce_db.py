# -*- coding: utf-8 -*-

import sys, os, platform
import json
import pymysql.cursors
from enum import Enum, unique

reload(sys) 
sys.setdefaultencoding('utf8')

# Status code
@unique
class StatusCode(Enum):
    OK = 200 # 一般来说，这是客户端希望看到的响应代码。它表示服务器成功执行了客户端所请求的动作，并且在2XX系列里没有其他更适合的响应代码了。# GET: 200 OK/PUT: 200 OK
    CREATED = 201 # 当服务器依照客户端的请求创建了一个新资源时，发送此响应代码。# POST: 201 Created
    ACCEPTED = 202 # 客户端的请求无法或将不被实时处理。
    NON_AUTHORITATIVE_INFORMATION = 203 # 这个响应代码跟200一样，只不过服务器想让客户端知道，有些响应报头并非来自该服务器--他们可能是从客户端先前发送的一个请求里复制的，或者从第三方得到的。
    NO_CONTENT = 204 # 若服务器拒绝对PUT、POST或者DELETE请求返回任何状态信息或表示，那么通常采用此响应代码。# DELETE: 204 No Content
    RESET_CONTENT = 205 # 它表明客户端应重置数据源的视图或数据结构。
    PARITIAL_CONTENT = 206 # 对于支持部分GET（partial GET）的服务而言“非常高”，其他情况下“低”。
    BAD_REQUEST = 400 # 服务器不理解客户端的请求，未做任何处理。
    UNAUTHORIZED = 401 # 用户未提供身份验证凭据，或者没有通过身份验证。
    PAYMENT_REQUIRED = 402 # 目前还没有用于HTTP的微支付系统，所以它被留作将来使用
    FORBIDDEN = 403 # 用户通过了身份验证，但是不具有访问资源所需的权限。
    NOT_FOUND = 404 # 所请求的资源不存在，或不可用。
    METHOD_NOT_ALLOWED = 405 # 用户已经通过身份验证，但是所用的 HTTP 方法不在他的权限之内。
    NOT_ACCEPTABLE = 406 # 例如：客户端通过Accept头指定媒体类型为application/json+hic，但是服务器只支持application/json。
    PROXY_AUTHENTICATION_REQUIRED = 407 # 可能是因为客户端没有提供证书，也可能是客户端提供的证书不正确或不充分。
    REQUEST_TIMEOUT = 408 # 假如HTTP客户端与服务器建立链接后，却不发送任何请求（或从不发送表明请求结束的空白行），那么服务器最终应该发送一个408响应代码，并关闭此连接
    CONFLICT = 409 # 你请求的操作会导致服务器的资源处于一种不可能或不一致的状态。
    GONE = 410 # 所请求的资源已从这个地址转移，不再可用。
    LENGTH_REQUIRED = 411 # 若HTTP请求包含表示，它应该把Content-Length请求报头的值设为该表示的长度（以字节为单位）。
    PRECONDITION_FAILED = 412 # 客户端在请求报头里指定一些前提条件，并要求服务器只有在满足一定条件的情况下才能处理本请求。
    REQUEST_ENTITY_TOO_LARGE = 413 # 这个响应代码跟411类似，服务器可以用它来中断客户端的请求并关闭连接，而不需要等待请求完成。
    REQUEST_URI_TOO_LONG = 414 # HTTP标准并没有对URI长度作出官方限制，但大部分现有的web服务器都对URI长度有一个上限
    UNSUPPORTED_MEDIA_TYPE = 415 # 客户端要求的返回格式不支持。比如，API 只能返回 JSON 格式，但是客户端要求返回 XML 格式。
    REQUESTED_RANGE_NOT_SATISFIABLE = 416 # 当客户端所请求的字节范围超出表示的实际大小时，服务器发送此响应代码。
    EXPECTATION_FAILED = 417 # 当你用LBYL请求来考察服务器是否会接受你的表示时，如果服务器确认会接受你的表示，那么你将获得响应代码100，否则你将获得417。
    UNPROCESSABLE_ENTITY = 422 # 客户端上传的附件无法处理，导致请求失败。
    TOO_MANY_REQUESTS = 429 # 客户端的请求次数超过限额。
    INTERNAL_SERVER_ERROR = 500 # 客户端请求有效，服务器处理时发生了意外。
    NOT_IMPLEMENTED = 501 # 客户端试图做一个采用了拓展HTTP方法的请求，而普通web服务器不支持此请求。
    BAD_GATEWAY = 502 # 它表明代理方面出现问题，或者代理与上行服务器之间出现问题，而不是上行服务器本身有问题
    SERVICE_UNAVAILABLE = 503 # 服务器无法处理请求，一般用于网站维护状态。
    GATEWAY_TIMEOUT = 504 # 此响应代码表明代理无法连接上行服务器。
    HTTP_VERSION_NOT_SUPPORTED = 505 # 当服务器不支持客户端试图使用的HTTP版本时发送此响应代码。
    

# eCommerce database helper
class ECommerceDBHelper(object):
    # Class construction
    def __init__(self):
        # Create database connector
        self.db_connector = None
        '''
        if 'mysql' == self.config_parameters['database']['type']:
            self.db_connector = pymysql.connect(
                host = str(self.config_parameters['database']['host']),
                port = int(self.config_parameters['database']['port']),
                user = str(self.config_parameters['database']['user']),
                passwd = str(self.config_parameters['database']['password']),
                db = str(self.config_parameters['database']['dbname']),
                charset = str(self.config_parameters['database']['charset']),
                cursorclass = pymysql.cursors.DictCursor)
        '''
        self.db_connector = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '123456',
            db = 'eCommerce',
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor)

    # Class destruction
    def __del__(self):
        # Close database connector
        if self.db_connector is not None:
            self.db_connector.close()

    # Create shops: Return error code
    def create_shops(self, shops_to_create):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shops_to_create is None or len(shops_to_create) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to create were empty' % shops_to_create}

    # Read shops: Return error code
    def read_shops(self, shop_id, shops_read):
        shops_read = []
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is not None and len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) to read was invalid' % shop_id}

    # Update shops: Return error code
    def update_shops(self, shop_id, shops_to_update):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) to update was invalid' % shop_id}
        if shops_to_update is None or len(shops_to_update) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) to update were empty' % shops_to_update}

    # Delete shops: Return error code
    def delete_shops(self, shop_id, shops_deleted):
        shops_deleted = []
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) to delete was invalid' % shop_id}
    
    # Create products: Return error code
    def create_products(self, shop_id, products_to_create):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) for product was invalid' % shop_id}
        if products_to_create is None or len(products_to_create) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to create were empty' % products_to_create}

        # Create one by one
        with self.db_connector.cursor() as cursor:
            for product in products_to_create:
                product_found = False
                # Check if product exiting
                sql = 'SELECT ProductID FROM tProducts WHERE ShopID=%s AND ProductID=%s;'
                cursor.execute(sql, (str(shop_id), str(product.get('product_id', '0'))))
                result_rows = cursor.fetchall()
                for result_row in result_rows:
                    if len(result_row['ProductID']) > 0:
                        product_found = True
                        break;
                # Create if not found
                if product_found is not True:
                    sql = ('REPLACE INTO tProducts('
                        'ShopID,ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
                        'VariantID,Variant,SKU,Brand,HotSale,FirstCrawlingTime,LastCrawlingTime,CrawlingCounter) '
                        'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,'
                        '%s,%s,%s,%s,%s,CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP(),1);')
                    cursor.execute(
                        sql, 
                        (
                        str(shop_id), 
                        str(product.get('product_id', '0')), 
                        str(product.get('product_name', '')), 
                        str(product.get('catalog_name', '')), 
                        str(product.get('product_price', '')), 
                        str(product.get('compare_price', '')), 
                        str(product.get('product_link', '')), 
                        str(product.get('product_details', '')), 
                        str(product.get('variant_id', '0')), 
                        str(product.get('variant', '')), 
                        str(product.get('sku', '')), 
                        str(product.get('brand', '')), 
                        str(product.get('hot_sale', '0'))
                        )
                        )
                    self.db_connector.commit()
                # Update if found
                else:
                    sql = ('UPDATE tProducts '
                        'SET CrawlingCounter=CrawlingCounter+1,LastCrawlingTime=CURRENT_TIMESTAMP() '
                        'WHERE ShopID=%s AND ProductID=%s AND '
                        'ProductName=%s AND CatalogName=%s AND '
                        'ProductPrice=%s AND ComparePrice=%s AND '
                        'ProductLink=%s AND ProductDescription=%s;')
                    cursor.execute(
                        sql, 
                        (
                        str(shop_id), 
                        str(product.get('product_id', '0')), 
                        str(product.get('product_name', '')), 
                        str(product.get('catalog_name', '')), 
                        str(product.get('product_price', '')), 
                        str(product.get('compare_price', '')), 
                        str(product.get('product_link', '')), 
                        str(product.get('product_details', ''))
                        )
                        )
                    self.db_connector.commit()
            

    # Read products: Return error code
    def read_products(self, shop_id, product_id, products_read):
         # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) for product was invalid' % shop_id}
        if product_id is not None and len(product_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'product(%s) to read was invalid' % product_id}
        
        # Encode sql
        sql = ('SELECT ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
               'VariantID,Variant,SKU,Brand,HotSale,UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime,CrawlingCounter '
               'FROM tProducts '
               'WHERE ShopID=%s '
               'ORDER BY ProductID ASC;' % shop_id)
        if product_id is not None and len(product_id) > 0:
            sql = ('SELECT ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
                   'VariantID,Variant,SKU,Brand,HotSale,UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime,CrawlingCounter '
                   'FROM tProducts '
                   'WHERE ShopID=%s AND ProductID=%s '
                   'ORDER BY ProductID ASC;' % (shop_id, product_id))
         
        # Get recordset
        with self.db_connector.cursor() as cursor:
            cursor.execute(sql)
            result_rows = cursor.fetchall()
            for result_row in result_rows:
                product = {
                    'product_id':result_row['ProductID'],
                    'product_name':result_row['ProductName'],
                    'catalog_name':result_row['CatalogName'],
                    'product_price':result_row['ProductPrice'],
                    'compare_price':result_row['ComparePrice'],
                    'product_link':result_row['ProductLink'],
                    'product_details':result_row['ProductDescription'],
                    'variant_id':result_row['VariantID'],
                    'variant':result_row['Variant'],
                    'sku':result_row['SKU'],
                    'brand':result_row['Brand'],
                    'hot_sale':result_row['HotSale'],
                    'first_crawling':result_row['FirstCrawlingTime'],
                    'last_crawling':result_row['LastCrawlingTime'],
                    'crawling_counter':result_row['CrawlingCounter']
                }
                products_read.append(product)

        # Return
        if len(products_read) > 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d products read' % len(products_read)}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'product(s) not found'}

    # Update products: Return error code
    def update_products(self, shop_id, product_id, products_to_update):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) for product was invalid' % shop_id}
        if product_id is None or len(product_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'product(%s) to update was invalid' % product_id}
        if products_to_update is None or len(products_to_update) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'product(%s) to update was empty' % products_to_update}

    # Delete products: Return error code
    def delete_products(self, shop_id, product_id, products_deleted):
        products_deleted = []
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or len(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) for product was invalid' % shop_id}
        if product_id is None or len(product_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'product(%s) to delete was invalid' % product_id}

    
