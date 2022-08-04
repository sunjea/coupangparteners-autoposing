import hmac
import os
import hashlib
import requests
import json

from time import gmtime, strftime, localtime, time
import logging
import config 

logger = logging.getLogger(__name__)

def requestGetData(api_type, url) :
    authorization = generateHmac("GET", url, config.SECRET_KEY, config.ACCESS_KEY)
    url = "{}{}".format(config.DOMAIN, url)
    logger.info(" == Request GetData URL : {} ".format(url))
    response = requests.get(url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            }
                            )
    return response.json()

def requestPostData(api_type, url, body_data) :
    authorization = generateHmac("POST", url, config.SECRET_KEY, config.ACCESS_KEY)
    url = "{}{}".format(config.DOMAIN, url)
    response = requests.post(url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            },
                            data=json.dumps(body_data)
                            )
    return response.json()

def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)


def writeJsonData(items):
    filePath = "%s/%s" % (config.JSON_PATH, config.JSON_FILE_NAME)
    logger.info(" == Write Json Data : {} ".format(filePath))
    with open(filePath, 'w', encoding='utf-8') as outfile:
        json.dump(items, outfile, indent="\t", ensure_ascii=False)

def readJsonToDict():
    filePath = "%s/%s" % (config.JSON_PATH, config.JSON_FILE_NAME)
    logger.info(" == Read Json Data : {} ".format(filePath))
    with open(filePath, "r", encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        # print(json_data)
    return json_data

def checkAlreadySearch():
    config.JSON_FILE_NAME 
    config.JSON_FILE_NAME = "%s%s" % (strftime('%Y_%m_%d', localtime(time())), ".json")
    filepath = findfile(config.JSON_FILE_NAME, config.JSON_PATH)
    logger.info(" == JSON_FILE_NAME : {} ".format(config.JSON_FILE_NAME))
    # 파일이 존재할 경우
    if filepath != None :
        logger.info(" >>> Already File {} ".format(filepath))
        return True
    else :
        # logger.info(" >>> File Not Found !! ")
        return False
    
def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)