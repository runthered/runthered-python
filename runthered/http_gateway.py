import urllib
import urllib2
import json
import base64

class DlrQueryResponse:
    def __init__(self, status, reason_code, push_id):
        self.status = status
        self.reason_code = reason_code
        self.id = push_id

class HttpGatewayException(Exception):
    pass

class HttpGatewayApi:
    def __init__(self, username, password, service_key, url='https://connect.runthered.com:14004/public_api/sms/gateway/', dlr_url='https://connect.runthered.com:14004/public_api/sms/dlr/'):
        self.url = url
        self.dlr_url = dlr_url
        self.username = username
        self.password = password
        self.service_key = service_key	
        			
    def do_request(self, values, url, method='POST'):
        try:
            data = urllib.urlencode(values)
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            headers = {'Authorization': "Basic %s" % base64string}
            if method == 'POST':
                req = urllib2.Request(url, data, headers=headers)
            else:
                req = urllib2.Request(url + '?' + data, data=None, headers=headers)
            f = urllib2.urlopen(req)
            output = f.read()
            f.close()
            return output
        except urllib2.HTTPError as e:
            raise HttpGatewayException(e.reason, e.code)
                  
    def push_message(self, message, to, from_number=None, billing_code=None, partner_reference=None):
        values = {"message":message, "to": to}
        if from_number:
            values["from"] = from_number
        if billing_code:
            values["billingCode"] = billing_code
        if partner_reference:
            values["partnerReference"] = partner_reference
        data = self.do_request(values, self.url + self.service_key, method='POST')
        return data   

    def query_dlr(self, msg_id):
        values = {"id":msg_id}
        output = self.do_request(values, self.dlr_url + self.service_key, method='GET')
        data = json.loads(output)
        msg_id = data['id']
        status = data['status']
        reason_code = data['reason']
        return DlrQueryResponse(status, reason_code, msg_id)

