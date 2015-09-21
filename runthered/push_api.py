import json
import urllib2
import base64

class PushApiResponse:
    def __init__(self, status, msg_id, push_id):
        self.status = status
        self.msg_id = msg_id
        self.id = push_id

class DlrQueryResponse:
    def __init__(self, status, reason_code, push_id):
        self.status = status
        self.reason_code = reason_code
        self.id = push_id

class PushApiException(Exception):
    pass

class PushApi:
    def __init__(self, username, password, service_key, url='https://connect.runthered.com:10443/public_api/service'):
        self.url = url
        self.username = username
        self.password = password
        self.service_key = service_key		
		
    def do_json_request(self, data):
        try:
            data_string = json.dumps(data)    
            headers = {'Content-Type': 'application/json'}
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            headers['Authorization'] = "Basic %s" % base64string
            req = urllib2.Request(self.url, data_string, headers)
            f = urllib2.urlopen(req)
            http_code = f.getcode()
            output = f.read()
            f.close()
            data = json.loads(output)
            if 'result' not in data:
                error = data['error']
                message = error['message']
                code = error['code']
                raise PushApiException(message)
            return data
        except urllib2.HTTPError as e:
            raise PushApiException(e.reason, e.code)
              
    def push_message(self, body, to, from_number=None, push_id=1):
        json_data = {"jsonrpc":"2.0", "method":"sendsms", "params":{"service_key":self.service_key, "to":to, "body":body}, "id":push_id} 
        if from_number:
            json_data["params"]["frm"] = from_number
        data = self.do_json_request(json_data)
        push_id = data['id']
        result = data['result']
        status = result['status']
        msg_id = result['msg_id']
        return PushApiResponse(status, msg_id, push_id)   

    def query_dlr(self, msg_id, push_id=1):
        json_data = {"jsonrpc":"2.0", "method":"querydlr", "params":{"service_key":self.service_key, "msg_id": msg_id}, "id":push_id}
        data = self.do_json_request(json_data)
        push_id = data['id']
        result = data['result']
        status = result['status']
        reason_code = result['reason']
        msg_id = result['msg_id']
        return DlrQueryResponse(status, reason_code, push_id)

