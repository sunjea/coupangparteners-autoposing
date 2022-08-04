import pyshorteners as ps
import urllib.request
import json
import config
from util import requestGetData
import logging
logger = logging.getLogger(__name__)

def getProductSearch() :
    # 상품검색
    search_url = "/v2/providers/affiliate_open_api/apis/openapi/v1/products/search?keyword="
    query = config.KEY_WORD
    url = "{}{}".format(search_url, urllib.parse.quote(query))
    logger.info(" == Product Searh Query : {} KEY_WORD : {} ".format(url, config.KEY_WORD))
    return requestGetData(config.API_SEARCH, url)

def parseSearchData(rsp):
    rspDump = json.dumps(rsp['data'])
    rspDict = json.loads(rspDump)
    items = rspDict['productData']
    logger.info(" == parseSearchData Start ")
    # for data in items :
    #     sh = ps.Shortener()
    #     short_url = (sh.tinyurl.short(data['productUrl']))
    #     logger.info(" == parseSearchData :  productUrl -> short_url ..")
    #     data['productUrl'] = short_url
        # logger.info(" == short_url {} ", str(short_url))
        
    logger.info(" == parseSearchData End ")
    return items