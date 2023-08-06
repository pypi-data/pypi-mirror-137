import re
import pandas as pd
import urllib.parse as urlParse
import LibHanger.Library.uwLogger as Logger
from pandas.core.frame import DataFrame
from bs4 import BeautifulSoup
from LibHanger.Models.recset import recset
from Scrapinger.Library.browserContainer import browserContainer
from sqlalchemy.sql.elements import Null
from parroter.Library.kojima.lastNameListController import lastNameListController
from parroter.Library.kojima.kojimaConfig import kojimaConfig
from parroter.Library.kojima.kojimaGlobals import *
from parroter.Models.trn_last_name import trn_last_name

class gettr_lastNameList(lastNameListController):
    
    """
    全国苗字ランキング取得クラス
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        super().__init__()
        
        self.dfLastNameInfo:DataFrame = recset(trn_last_name).getDataFrame()
        """ 全国苗字情報DataFrame """  
    
    def getAllData(self, *args, **kwargs):
        
        for page in range(kwargs.get('FromPage') , int(kwargs.get('ToPage')) + 1, 1):
            dfLastNameInfoTemp = self.getData(pageNo=page)
            if len(dfLastNameInfoTemp) == 0:
                continue
            else:
                self.dfLastNameInfo = pd.concat([self.dfLastNameInfo, dfLastNameInfoTemp])
                
        return self.dfLastNameInfo
    
    @Logger.loggerDecorator("getData",['pageNo'])
    def getData(self, *args, **kwargs):
        
        """
        全国苗字情報取得
        
        Parameters
        ----------
        kwargs : dict
            @pageNo
                ページ番号
        """
        
        # 全国苗字情報をDataFrameで取得
        dfLastNameInfo = self.getLastNameInfoDataFrame(**kwargs)

        return dfLastNameInfo
    
    @Logger.loggerDecorator("getLastNameInfoDataFrame")
    def getLastNameInfoDataFrame(self, *args, **kwargs):

        """
        全国苗字情報取得
        
        Parameters
        ----------
        kwargs : dict
            @pageNo
                ページ番号
        """
        
        # 検索url(ルート)
        rootUrl = gv.kojimaConfig.myoji_yurai_URL
        # 検索url(ページ番号指定)
        lastNameInfoUrl = rootUrl.format(kwargs.get('pageNo'))

        # スクレイピング準備
        self.wdc.settingScrape()

        # ページロード
        self.wdc.browserCtl.loadPage(lastNameInfoUrl)

        # pandasデータを返却する
        return self.wdc.browserCtl.createSearchResultDataFrame(**kwargs)

    class beautifulSoup(browserContainer.beautifulSoup):
        
        """
        ブラウザコンテナ:beautifulSoup
        """

        def __init__(self, _config: kojimaConfig):
            
            """
            コンストラクタ
            
            Parameters
            ----------
                _config : kojimaConfig
                    共通設定
            """

            super().__init__(_config)
            
            self.config = _config
            self.bc = gettr_lastNameList
            self.cbCreateSearchResultDataFrameByBeutifulSoup = self.createSearchResultDataFrameByBeutifulSoup
                            
        def createSearchResultDataFrameByBeutifulSoup(self, soup:BeautifulSoup, *args, **kwargs) -> DataFrame:
            
            """
            全国苗字ランキングをDataFrameで返す(By BeutifulSoup)
            
            Parameters
            ----------
            soup : BeautifulSoup
                BeautifulSoupオブジェクト
            
            """

            # スクレイピング結果から改行ｺｰﾄﾞを除去
            [tag.extract() for tag in soup(string='\n')]
            
            # class取得
            tables = soup.find_all(class_="simple")

            if tables:
                
                # 全国苗字情報model用意            
                lastNameInfo = recset(trn_last_name)
                
                for index in range(len(tables)):
                    try:
                        last_name_list = tables[index].find_all(class_="odd")
                        if len(last_name_list) > 5 and tables[index].attrs['width'] == '98%':
                            for index in range(len(last_name_list)):
                                
                                last_name_row = last_name_list[index].find_all('td')
                                # 順位
                                ranking = last_name_row[0].text.replace('位','')
                                # 苗字
                                last_name = last_name_row[1].text
                                # 人数
                                numPeple = last_name_row[2].text.replace('およそ','').replace('人','').replace(',','')
                                
                                # Modelに追加
                                lastNameInfoRow:trn_last_name = lastNameInfo.newRow()
                                lastNameInfoRow.ranking = ranking
                                lastNameInfoRow.last_name = last_name
                                lastNameInfoRow.numPeple = numPeple
                                lastNameInfo.addRow(lastNameInfoRow)

                                # コンソール出力
                                print('順位={0}位'.format(ranking))
                                print('苗字={0}'.format(last_name))
                        
                    except Exception as e: # その他例外
                        Logger.logging.error('Other Exception')
                        Logger.logging.error(str(e))
                
                return lastNameInfo.getDataFrame()
        
