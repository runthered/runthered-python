from runthered.http_gateway import HttpGatewayApi
from runthered.http_gateway import HttpGatewayException

try:
    username = 'snoop7'
    password = 'snoop7'
    service_key = 'snop7'
    http_gateway_api = HttpGatewayApi(username, password, service_key)

    to = '6421859582'
    from_number = '2059'
    message = 'Hello World!'
    response = http_gateway_api.push_message(message, to, from_number)
    print "The msg_id is %s"%response
        
    msg_id = '55f8ad98e13823069edbdfd6'
    dlr_response = http_gateway_api.query_dlr(msg_id)
    print "The status is %s"%dlr_response.status
    print "The reason is %s"%dlr_response.reason_code
    print "The dlr id is %s"%dlr_response.id
except HttpGatewayException as e:
    print "Caught exception: %s"%e



