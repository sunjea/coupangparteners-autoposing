

def getDeepLink(req_list):
    deep_url = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    deeplink_req = dict()
    deeplink_req['coupangUrls'] = req_list
    deeplink_req['subId'] = CHANNAL_ID

    response = requestPostData(API_DEEPLINK, deep_url, deeplink_req)
    return parseDeepLink(response)

def parseDeepLink(rsp):
    rspDump = json.dumps(rsp['data'])
    items = json.loads(rspDump)
    shortUrlList = []
    for data in items :
        shortUrlList.append(data['shortenUrl'])
    
    return shortUrlList
