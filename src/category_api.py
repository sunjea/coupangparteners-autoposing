

def getProductBestCategories() :
    # 카테고리
    category_url = "/v2/providers/affiliate_open_api/apis/openapi/v1/products/bestcategories/"
    # 카테고리별 고유 코드
    category = 1001
    
    url = "{}{}?subId={}".format(category_url, category, CHANNAL_ID)
    response = requestGetData(API_BEST_CATEGORY, url)
    categoriesIdList = parseCategoryData(response)
    return categoriesIdList

def parseCategoryData(rsp):
    rspDump = json.dumps(rsp['data'])
    items = json.loads(rspDump)
    product_list = []

    for data in items :
        product_list.append("https://www.coupang.com/vp/products/" + str(data['productId']))

    return product_list