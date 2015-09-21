from runthered.push_api import PushApi
from runthered.push_api import PushApiException

try:
    username = 'testuser'
    password = 'testuser'
    service_key = '82221'
    push_api = PushApi(username, password, service_key)

    to = '6421859582'
    from_number = '8222'
    body = 'Hello World!'
    push_id = 12345
    response = push_api.push_message(body, to, from_number, push_id)
    print "The msg_id is %s"%response.msg_id
    print "The status is %s"%response.status
    print "The id is %s"%response.id

    msg_id = '55f8ab0be13823069edbdfbe'
    dlr_id = 12346
    dlr_response = push_api.query_dlr(msg_id, dlr_id)
    print "The status is %s"%dlr_response.status
    print "The reason is %s"%dlr_response.reason_code
    print "The dlr id is %s"%dlr_response.id
except PushApiException as e:
    print "Caught exception: %s"%e



