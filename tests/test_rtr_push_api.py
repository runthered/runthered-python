'''
Created on 27/08/2015

@author: Finn Colman
'''
import unittest
import urllib2
from runthered.push_api import PushApi
from runthered.push_api import PushApiException
import code

class TestRtrPushApiWrapper(unittest.TestCase):
    
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
           
    def test_rtr_push_api_success(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "result": {"status": "Accepted", "msg_id": "%s"}}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(200, json_string)              
                               
        response = push_api.push_message(body, to, from_number, push_id)
    
        self.assertEqual(response.msg_id, "515cabc3464af599972c65bc")
        self.assertEqual(response.status, "Accepted")
        self.assertEqual(response.id, 12345)
        
    def test_rtr_push_api_dlr_success(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "result": {"status": "DELIVRD", "reason": "000", "msg_id": "%s"}}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(200, json_string)              
                               
        response = push_api.query_dlr(msg_id, push_id)
    
        self.assertEqual(response.status, "DELIVRD")
        self.assertEqual(response.reason_code, "000")
        self.assertEqual(response.id, 12345)
        
    def test_rtr_push_api_unauthorised(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "result": {"status": "Accepted", "msg_id": "%s"}}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(401, json_string)              
            
        self.assertRaises(PushApiException, push_api.push_message, body, to, from_number, push_id)
        
    def test_rtr_push_api_dlr_unauthorised(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "result": {"status": "Accepted", "msg_id": "%s"}}'%msg_id
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(401, json_string)              
            
        self.assertRaises(PushApiException, push_api.query_dlr, msg_id, push_id)
        
    def test_rtr_push_api_error(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "error": {"message": "Invalid shortcode.", "code": -1}}'
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(200, json_string)              
            
        self.assertRaises(PushApiException, push_api.push_message, body, to, from_number, push_id)
        
    def test_rtr_push_api_dlr_error(self):
        username = 'fred'
        password = 'fred'
        service_key = 'bob12'
        push_api = PushApi(username, password, service_key)
        
        to = '64212431234'
        from_number = '8222'
        body = 'bob the builder'
        push_id = 4
                    
        msg_id = "515cabc3464af599972c65bc"
        json_string = '{"jsonrpc": "2.0", "id": 12345, "error": {"message": "Unknown Message Id.", "code": -11}}'
        # dummy out urllib2.urlopen(req)
        urllib2.urlopen = lambda req: TestRtrPushApiWrapper.UrlResponse(200, json_string)              
            
        self.assertRaises(PushApiException, push_api.query_dlr, msg_id, push_id)
    