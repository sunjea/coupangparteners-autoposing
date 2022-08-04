import logging
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic 
from PyQt5.QtCore import *

from util import checkAlreadySearch, writeJsonData, readJsonToDict
from productsearch_api import getProductSearch, parseSearchData
from make_html import makePostingItems
import config

#UI파일 연결 #단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다. 
form_class = uic.loadUiType("ui/coupang_posting.ui")[0] 

class WindowClass(QMainWindow, form_class) : 
    def __init__(self) : 
        super().__init__() 
        self.setupUi(self) 
        
        self.setFixedSize(340,60)
        #각 버튼에 대한 함수 연결 
        self.pushButton.clicked.connect(self.func_start)
        self.searchThr = SearchThread(parent=self)
        self.statusBar.showMessage('준비')

    def func_start(self) :
        self.pushButton.setDisabled(True)
        self.searchThr.start()
        
class SearchThread(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent 
    
    def run(self): 
        logger.info(" == Searching Start .. ")
        self.parent.statusBar.showMessage('동작중..')
        if checkAlreadySearch() == False :      ## 파일이 없을 경우 생성
            # choose = input("검색할 키워드를 입력 하세요. : ")
            config.KEY_WORD = self.parent.plainTextEdit.toPlainText().lstrip()
            rspSearchItems = getProductSearch()
            items = parseSearchData(rspSearchItems)
            writeJsonData(items)
        else :
            self.parent.statusBar.showMessage('이전 동일 날짜 동작 파일(.json) 존재..')
            return 
        jsonData = readJsonToDict()
        makePostingItems(jsonData)
        logger.info(" == Searching End .. : {} ".format(config.KEY_WORD))
        self.parent.statusBar.showMessage('완료')
        self.parent.pushButton.setEnabled(True)
 
if __name__ == "__main__" :

    # 로그 생성
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)
    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log를 파일에 출력
    file_handler = logging.FileHandler(config.LOG_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(" === START COUPANG-API PROGRAM === ")

    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show() 
    app.exec_()
    
    logger.info(" === END COUPANG-API PROGRAM === ")
    
    