'''
Created on 3/09/2015

@author: Finn Colman
'''
import unittest
import urllib2
from runthered.http_gateway import HttpGatewayApi
from runthered.http_gateway import HttpGatewayException
import code

class TestRtrHttpGatewayWrapper(unittest.TestCase):
    
    class UrlResponse():
        def __init__(self, code, response):
            self.code = code
            if self.code == 401:
                raise urllib2.HTTPError('', 401, "Not Authorised", '', None)
            elif self.code == 400:
                raise urllib2.HTTPError('', 400, "Bad Request", '', None)
            elif self.code == 404:
                raise urllib2.HTTPError('', 404, "Not found", '', None)            
            self.response = response
                
        def getcode(self):
            return self.code
                
        def read(self):
            return self.response
        
        def close(self):
            pass
           
    def test_rtr_http_gateway_success(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        message = 'bob the builder'
                            
        msg_id = "515cabc3464af599972c65bc"
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(200, msg_id)              
                               
        response = http_gateway_api.push_message(message, to, from_number)
    
        self.assertEqual(response, "515cabc3464af599972c65bc")
        
    def test_rtr_http_gateway_dlr_success(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
                            
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"id": "%s", "status": "DELIVRD", "reason": "000"}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(200, json_string)              
                               
        response = http_gateway_api.query_dlr(msg_id)
    
        self.assertEqual(response.status, "DELIVRD")
        self.assertEqual(response.reason_code, "000")
        self.assertEqual(response.id, msg_id)
        
    def test_rtr_http_gateway_unauthorised(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        message = 'bob the builder'
                            
        msg_id = "515cabc3464af599972c65bc"
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(401, msg_id)              
            
        self.assertRaises(HttpGatewayException, http_gateway_api.push_message, message, to, from_number)
        
    def test_rtr_http_gateway_dlr_unauthorised(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        message = 'bob the builder'
                            
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"id": "%s", "status": "DELIVRD", "reason": "000"}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(401, json_string)              
            
        self.assertRaises(HttpGatewayException, http_gateway_api.query_dlr, msg_id)
        
    def test_rtr_http_gateway_error(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
        
        to = ''
        from_number = '8222'
        message = 'bob the builder'
                            
        msg_id = "515cabc3464af599972c65bc"
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(400, msg_id)              
            
        self.assertRaises(HttpGatewayException, http_gateway_api.push_message, message, to, from_number)
        
    def test_rtr_http_gateway_dlr_error(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        http_gateway_api = HttpGatewayApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        message = 'bob the builder'
                            
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"id": "%s", "status": "DELIVRD", "reason": "000"}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrHttpGatewayWrapper.UrlResponse(404, json_string)              
            
        self.assertRaises(HttpGatewayException, http_gateway_api.query_dlr, msg_id)
        
        