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

    # Create crawling rules
    def create_crawling_rules(self, crawling_rules):
        pass

    # Create shops: Return error code
    def create_shops(self, shops_to_create):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shops_to_create is None or len(shops_to_create) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to create were empty' % shops_to_create}

        # Create one by one
        number_created = 0
        all_existing = True
        with self.db_connector.cursor() as cursor:
            # Get maximum shopid
            max_shop_id = 0
            sql = 'SELECT MAX(ShopID) AS MaxShopID FROM tShops'
            cursor.execute(sql)
            result_rows = cursor.fetchall()
            for result_row in result_rows:
                max_shop_id = int(result_row['MaxShopID'])
                break

            # Create one by one
            for shop in shops_to_create:
                # Check request shop
                shop_type = int(shop.get('shop_type', 0))
                shop_name = shop.get('shop_name', None)
                shop_url = shop.get('shop_url', None)
                if shop_type is None or shop_type <= 0 or shop_name is None or len(shop_name) <= 0 or shop_url is None or len(shop_url) <= 0:
                    return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to create were error format' % shops_to_create}

                # Check if existing
                shop_existing = False
                sql = 'SELECT ShopID FROM tShops WHERE ShopType=%d AND (ShopName=\'%s\' OR ShopURL=\'%s\');' % (shop_type, shop_name, shop_url)
                cursor.execute(sql)
                result_rows = cursor.fetchall()
                for result_row in result_rows:
                    if result_row['ShopID'] is not None and int(result_row['ShopID']) > 0:
                        shop_existing = True
                        break

                # Create is not found
                if shop_existing is not True:
                    max_shop_id = max_shop_id + 1
                    number_created = number_created + 1
                    all_existing = False
                    sql = ('REPLACE INTO tShops('
                           'ShopID,ShopType,ShopName,ShopURL,CrawlingFrequency,CrawlingState,FirstCrawlingTime,LastCrawlingTime,CrawlingCounter) '
                           'VALUES('
                           '%s,%s,%s,%s,%s,0,CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP(),0);')
                    cursor.execute(
                        sql, 
                        (
                        str(max_shop_id), 
                        str(shop_type), 
                        str(shop_name), 
                        str(shop_url), 
                        str(shop.get('crawling_freq', 3600))
                        )
                        )
                    self.db_connector.commit()
                # Update if not found
                else:
                    shop_id = int(shop.get('shop_id', 0))
                    if shop_id is not None and shop_id > 0:
                        sql = ('UPDATE tShops '
                               'SET ShopType=%s,ShopName=%s,ShopURL=%s,CrawlingFrequency=%s '
                               'WHERE ShopID=%s;')
                        cursor.execute(
                            sql, 
                            (
                            str(shop_type), 
                            str(shop_name), 
                            str(shop_url), 
                            str(shop.get('crawling_freq', 3600)),
                            str(shop_id)
                            )
                            )
                        self.db_connector.commit()

                # Update/Create rules
                crawling_rules = shop.get('crawling_rules', None)
                if crawling_rules is not None and len(crawling_rules) > 0:
                    self.create_crawling_rules(crawling_rules)

        # Return
        if number_created > 0:
            return {'errcode': StatusCode.CREATED.value, 'errmsg': '%d shops were created' % number_created}
        else:
            if all_existing is True:
                return {'errcode': StatusCode.CREATED.value, 'errmsg': 'shops(%s) to create were existing' % shops_to_create}
            else:
                return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to create were error format' % shops_to_create}

    # Read shops: Return error code
    def read_shops(self, shop_ids_to_read, shops_read):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
         
        # Get recordset
        with self.db_connector.cursor() as cursor:
            # Encode sql
            sql = ('SELECT ShopID,ShopType,ShopName,ShopURL,CrawlingFrequency,CrawlingState,'
                   'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime '
                   'FROM tShops '
                   'ORDER BY ShopID ASC;')
            if shop_ids_to_read is not None and len(shop_ids_to_read) > 0:
                sql = ('SELECT ShopID,ShopType,ShopName,ShopURL,CrawlingFrequency,CrawlingState,'
                       'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime '
                       'FROM tShops '
                       'WHERE ShopID IN (%s) '
                       'ORDER BY ShopID ASC;' % ','.join([str(shop_id) for shop_id in shop_ids_to_read]))
            cursor.execute(sql)
            result_rows = cursor.fetchall()
            for result_row in result_rows:
                shop = {
                    'shop_id':int(result_row['ShopID']),
                    'shop_type':int(result_row['ShopType']),
                    'shop_name':result_row['ShopName'],
                    'shop_url':result_row['ShopURL'],
                    'crawling_freq':int(result_row['CrawlingFrequency']),
                    'crawling_state':int(result_row['CrawlingState']),
                    'first_crawling':int(result_row['FirstCrawlingTime']),
                    'last_crawling':int(result_row['LastCrawlingTime']),
                }
                shops_read.append(shop)

        # Return
        if len(shops_read) > 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d shops were read' % len(shops_read)}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'shop(s) were not found'}

    # Update shops: Return error code
    def update_shops(self, shop_ids_to_update, shops_to_update):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shops_to_update is None or len(shops_to_update) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to update were empty' % shops_to_update}

        # Update one by one
        number_updated = 0
        with self.db_connector.cursor() as cursor:
            for shop in shops_to_update:
                # Check input shop
                need_update = False
                shop_type = int(shop.get('shop_type', 0))
                shop_name = shop.get('shop_name', None)
                shop_url = shop.get('shop_url', None)
                if shop_type is None or shop_type <= 0 or shop_name is None or len(shop_name) <= 0 or shop_url is None or len(shop_url) <= 0:
                    return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to update were error format' % shops_to_update}
                req_shop_id = int(shop.get('shop_id', 0))
                if shop_ids_to_update is None or len(shop_ids_to_update) <= 0:
                    if req_shop_id <= 0:
                        return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to update were error format' % shops_to_update}
                    else:
                        need_update = True
                else:     
                    for shop_id in shop_ids_to_update:
                        if req_shop_id == int(shop_id):
                            req_shop_id = int(shop_id)
                            need_update = True
                            break
                if need_update is not True:
                    continue

                # Encode sql
                with self.db_connector.cursor() as cursor:
                    number_updated = number_updated + 1
                    sql = ('UPDATE tShops '
                           'SET ShopType=%s,ShopName=%s,ShopURL=%s,CrawlingFrequency=%s '
                           'WHERE ShopID=%s;')
                    cursor.execute(
                        sql, 
                        (
                        str(shop_type), 
                        str(shop_name), 
                        str(shop_url), 
                        str(shop.get('crawling_freq', 3600)),
                        str(shop_id)
                        )
                        )
                    self.db_connector.commit()

                # Update/Create rules
                crawling_rules = shop.get('crawling_rules', None)
                if crawling_rules is not None and len(crawling_rules) > 0:
                    self.create_crawling_rules(crawling_rules)

        # Return
        if number_updated >= 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d shops were updated' % number_updated}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'shops(%s) were not created' % shops_to_update}

    # Delete shops: Return error code
    def delete_shops(self, shop_ids_to_delete, shops_deleted):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_ids_to_delete is None or len(shop_ids_to_delete) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shops(%s) to delete were invalid' % shop_ids_to_delete}

        # Get/Set into database
        with self.db_connector.cursor() as cursor:
            # Encode condition
            shop_ids_condition = ','.join([str(shop_id) for shop_id in shop_ids_to_delete])

            # Get shops to deleted
            sql = ('SELECT ShopID,ShopType,ShopName,ShopURL,CrawlingFrequency,CrawlingState,'
                   'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime '
                   'FROM tShops '
                   'WHERE ShopID IN (%s) '
                   'ORDER BY ShopID ASC;' % shop_ids_condition)
            cursor.execute(sql)
            result_rows = cursor.fetchall()
            for result_row in result_rows:
                shop = {
                    'shop_id':int(result_row['ShopID']),
                    'shop_type':int(result_row['ShopType']),
                    'shop_name':result_row['ShopName'],
                    'shop_url':result_row['ShopURL'],
                    'crawling_freq':int(result_row['CrawlingFrequency']),
                    'crawling_state':int(result_row['CrawlingState']),
                    'first_crawling':int(result_row['FirstCrawlingTime']),
                    'last_crawling':int(result_row['LastCrawlingTime']),
                }
                shops_deleted.append(shop)

            # Delete selected shop
            sql = 'DELETE FROM tShops WHERE ShopID IN (%s);' % shop_ids_condition
            cursor.execute(sql)
            self.db_connector.commit()

        # Return
        if len(shops_deleted) > 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d shops were deleted' % len(shops_deleted)}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'shops(%d) were not found' % int(shop_id)}

    # Read products: Return error code
    def read_products(self, shop_id, product_ids_to_read, products_read):
         # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or int(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%s) for product was invalid' % int(shop_id)}
        if product_ids_to_read is not None and len(product_ids_to_read) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to read were invalid' % product_ids_to_read}
        
        # Get recordset
        with self.db_connector.cursor() as cursor:
            # Encode sql
            sql = ('SELECT ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
                   'VariantID,Variant,SKU,Brand,HotSale,'
                   'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,'
                   'UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime,'
                   'CrawlingCounter '
                   'FROM tProducts '
                   'WHERE ShopID=%d '
                   'ORDER BY ProductID ASC;' % int(shop_id))
            if product_ids_to_read is not None and len(product_ids_to_read) > 0:
                sql = ('SELECT ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
                       'VariantID,Variant,SKU,Brand,HotSale,'
                       'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,'
                       'UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime,'
                       'CrawlingCounter '
                       'FROM tProducts '
                       'WHERE ShopID=%d AND ProductID IN (%s) '
                       'ORDER BY ProductID ASC;' % (int(shop_id), ','.join([str(product_id) for product_id in product_ids_to_read])))

            # Execute and get recordset
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
                    'hot_sale':int(result_row['HotSale']),
                    'first_crawling':int(result_row['FirstCrawlingTime']),
                    'last_crawling':int(result_row['LastCrawlingTime']),
                    'crawling_counter':int(result_row['CrawlingCounter'])
                }
                products_read.append(product)

        # Return
        if len(products_read) > 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d products were read' % len(products_read)}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'product(s) were not found'}

    # Update products: Return error code
    def update_products(self, shop_id, product_ids_to_update, products_to_update):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or int(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%d) for product was invalid' % int(shop_id)}
        if products_to_update is None or len(products_to_update) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to update were empty' % products_to_update}

        # Update one by one
        number_updated = 0
        with self.db_connector.cursor() as cursor:
            for product in products_to_update:
                # Check input product
                need_update = False
                req_product_id = product.get('product_id', None)
                product_name = product.get('product_name', None)
                if req_product_id is None or len(req_product_id) <= 0 or product_name is None or len(product_name) <= 0:
                    return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to update were error format' % products_to_update}
                if product_ids_to_update is None or len(product_ids_to_update) <= 0:
                    if req_product_id <= 0:
                        return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to update were error format' % products_to_update}
                    else:
                        need_update = True
                else:     
                    for product_id in product_ids_to_update:
                        if req_product_id == product_id:
                            req_product_id = product_id
                            need_update = True
                            break
                if need_update is not True:
                    continue
                catalog_name = product.get('catalog_name', '')
                product_price = product.get('product_price', '')
                compare_price = product.get('compare_price', '')
                product_link = product.get('product_link', '')
                product_details = product.get('product_details', '')
                variant_id = product.get('variant_id', '')
                variant = product.get('variant', '')
                sku = product.get('sku', '')
                brand = product.get('brand', '')
                hot_sale = int(product.get('hot_sale', 0))

                # Encode sql
                with self.db_connector.cursor() as cursor:
                    number_updated = number_updated + 1
                    sql = ('UPDATE tProducts '
                           'SET ProductName=%s,CatalogName=%s,ProductPrice=%s,ComparePrice=%s,ProductLink=%s,ProductDescription=%s,VariantID=%s,Variant=%s,SKU=%s,Brand=%s,HotSale=%s '
                           'WHERE ShopID=%s AND ProductID=%s;')
                    cursor.execute(
                        sql, 
                        (
                        str(product_name), 
                        str(catalog_name), 
                        str(product_price), 
                        str(compare_price),
                        str(product_link),
                        str(product_details),
                        str(variant_id),
                        str(variant),
                        str(sku),
                        str(brand),
                        str(hot_sale),
                        str(shop_id),
                        str(req_product_id)
                        )
                        )
                    self.db_connector.commit()

        # Return
        if number_updated >= 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d products were updated' % number_updated}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'products(%s) were not created' % products_to_update}

    # Delete products: Return error code
    def delete_products(self, shop_id, product_ids_to_delete, products_deleted):
        # Check database connector
        if self.db_connector is None:
            return {'errcode': StatusCode.INTERNAL_SERVER_ERROR.value, 'errmsg': 'database connector was null'}
        # Check requests and inputs
        if shop_id is None or int(shop_id) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'shop(%d) for product was invalid' % int(shop_id)}
        if product_ids_to_delete is None or len(product_ids_to_delete) <= 0:
            return {'errcode': StatusCode.BAD_REQUEST.value, 'errmsg': 'products(%s) to delete were invalid' % product_ids_to_delete}

        # Get/Set into database
        with self.db_connector.cursor() as cursor:
            # Get products to deleted
            sql = ('SELECT ProductID,ProductName,CatalogName,ProductPrice,ComparePrice,ProductLink,ProductDescription,'
                   'VariantID,Variant,SKU,Brand,HotSale,'
                   'UNIX_TIMESTAMP(IFNULL(FirstCrawlingTime,\'2000-01-01 00:00:00\')) AS FirstCrawlingTime,'
                   'UNIX_TIMESTAMP(IFNULL(LastCrawlingTime,\'2000-01-01 00:00:00\')) AS LastCrawlingTime,'
                   'CrawlingCounter '
                   'FROM tProducts '
                   'WHERE ShopID=%d AND ProductID IN (%s) '
                   'ORDER BY ProductID ASC;' % (int(shop_id), ','.join([str(product_id) for product_id in product_ids_to_delete])))

            # Execute and get recordset
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
                    'hot_sale':int(result_row['HotSale']),
                    'first_crawling':int(result_row['FirstCrawlingTime']),
                    'last_crawling':int(result_row['LastCrawlingTime']),
                    'crawling_counter':int(result_row['CrawlingCounter'])
                }
                products_deleted.append(product)

            # Delete selected products
            sql = 'DELETE FROM tProducts WHERE ShopID=%d AND ProductID IN (%s);' % (int(shop_id), ','.join([str(product_id) for product_id in product_ids_to_delete]))
            cursor.execute(sql)
            self.db_connector.commit()

        # Return
        if len(products_deleted) > 0:
            return {'errcode': StatusCode.OK.value, 'errmsg': '%d products of shop(%d) were deleted' % (len(products_deleted), int(shop_id))}
        else:
            return {'errcode': StatusCode.NOT_FOUND.value, 'errmsg': 'products(%s) of shop(%d) were not found' % (product_ids_to_delete, int(shop_id))}

    
