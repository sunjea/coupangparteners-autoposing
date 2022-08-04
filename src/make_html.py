import dominate
from dominate.tags import *
from time import strftime, localtime, time
import config
import logging

logger = logging.getLogger(__name__)

def makePostingItems(items):
    doc = dominate.document(title='coupang-list')
    with doc.head:
        meta(charset='utf-8')
        meta(name='viewport', content='width=device-width, initial-scale=1')
        link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css', integrity='sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor', crossorigin='anonymous')

    with doc:
        with div(cls='m-5'):
            
            h1("{}년 {}월 {} 인기 순위 TOP10 ".format(strftime('%Y', localtime(time())), strftime('%m', localtime(time())), config.KEY_WORD))
            for i in items:
                with div(cls='card mb-3', style='max-with: 540px'):
                    with div(cls='row g-0 '):
                        with div(cls='col-md-4 text-center"'):
                            with a(href='%s' % i['productUrl'], target='_blank'):
                                img(cls='rounded p-2', width='250px', src='%s' % i['productImage'])
                        with div(cls='col-md-8'):
                            with div(cls='card-body'):
                                p("{}위) {}".format(i['rank'], i['productName']), cls='card-title h4 border-bottom pb-2')
                                p("%s 원" % format(i['productPrice'],','), cls='card-text text-danger h5 pb-1')
                                if i['isFreeShipping'] == True :
                                    p("무료배송", cls='card-text h6 pb-2')
                                # if i['isRocket'] == True :
                                #     with span() :
                                #         img(width='70px', src='https://image10.coupangcdn.com/image/badges/rocket/rocket_logo.png')
                                a("구매후기 보러가기" , href='%s' % i['productUrl'], target='_blank', cls='card-text btn btn-primary')
        
        # script(src='https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js', integrity='sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2', crossorigin='anonymous')
        with figure(cls='text-center'):
            figcaption("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.", cls='blockquote-footer')
        
    # Write HTML File...
    filePath = "%s/%s%s" % (config.HTML_PATH, strftime('%Y_%m_%d', localtime(time())), ".html")
    logger.info(" == Write HTML_File : {} ".format(config.JSON_FILE_NAME))
    doc_str = str(doc)
    with open(filePath, "w", encoding='utf-8') as out_doc:
        out_doc.write(doc_str)
