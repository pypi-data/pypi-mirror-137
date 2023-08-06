from ipaddress import v4_int_to_packed
import os
import random
from LibHanger.Library.uwImport import JsonImporter
from LibHanger.Library.uwImage import uwImage
from parroter.Library.parroterBase import parroterBase
from parroter.Library.kojima.kojimaConfig import kojimaConfig
from parroter.Library.kojima.kojimaGlobals import *
from parroter.Library.kojima.Getter.lastNameList import gettr_lastNameList

class kojimaBot(parroterBase):
    
    """
    児嶋Botクラス
    """
    
    class botLang():
        
        """
        言語設定
        """
        
        jp = 'Jp'
        """ 日本語 """

        en = 'En'
        """ 英語 """
        
    def __init__(self, rootPath, lang:str = botLang.jp) -> None:
        
        """
        コンストラクタ

        Parameters
        ----------
        rootPath : str
            ルートパス
        lang : str
            言語
        """
        
        # 基底側コンストラクタ
        super().__init__(rootPath)
        
        # 言語設定
        self._lang = lang
        
        # gvに設定情報をセット
        gv.config = self.config
        gv.kojimaConfig = self.settingConfig(rootPath)
        
        # kojima共通設定をメンバ変数にセット
        self.parroterConfig = gv.kojimaConfig
        
        # キートークン設定
        self.setKeyToken()
    
    def appName(self):
        
        """
        アプリ名
        """

        return 'kojima'
    
    def settingConfig(self, rootPath):
        
        """
        parroter共通設定
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        """
        
        # kojima.ini
        kc = kojimaConfig()
        kc.getConfig(rootPath, os.path.join(self.config.startupCfg.configFolderPath, self.appName()))

        return kc
    
    def getLastName(self, *args, **kwargs):
        
        """
        苗字リストを取得してDataFrameとして返す
        """
        
        getter = gettr_lastNameList()
        return getter.getAllData(**kwargs)
    
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        # 挨拶文の定型テキスト文取得
        helloTemplateText = self.getHelloTweetTemplateText()
                
        return helloTemplateText
    
    def getHelloTweetImage(self):
        
        """
        名言ツイート画像を生成する
        """
        
        # 名言ツイート画像を生成する
        return self.generateTweetImage()
    
    def getHelloTweetTemplateText(self):

        """
        挨拶定型文を取得する
        """
        
        with open(os.path.join(self.rootPath, 
                               self.parroterConfig.appListDir, 
                               self.parroterConfig.appHelloTextFileName),'r',encoding='utf-8') as f:
            helloTemplateText= f.read()
        
        return helloTemplateText
            
    def getWiseSayingTweetData(self):
        
        """
        名言ツイート文を取得する
        """
                
        # 名言ツイートjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfWiseSaying = ji.convertToDataFrame(gv.kojimaConfig.wiseSayingJsonDir, gv.kojimaConfig.wiseSayingJsonFileName)
        targetTweetNo = []
        if len(dfWiseSaying) > 0:
            targetTweetNo = range(1, len(dfWiseSaying) + 1)
        else:
            return []

        # 名言ツイートNoログ取得
        wiseSayingTweetNoLogFilePath = os.path.join(self.rootPath, 
                                                    gv.kojimaConfig.wiseSayingTweetNoLogDir, 
                                                    gv.kojimaConfig.wiseSayingTweetNoLogFileName)
        
        # 名言ツイートNoログ出力先ディレクトリ作成
        wiseSayingTweetNoLogFolderDir = os.path.dirname(wiseSayingTweetNoLogFilePath)
        if not os.path.exists(wiseSayingTweetNoLogFolderDir):
            os.makedirs(wiseSayingTweetNoLogFolderDir, exist_ok=True)
            
        wiseSayingTweetNoLog = []
        if os.path.exists(wiseSayingTweetNoLogFilePath):
            
            # 名言ツイートログ読込
            with open(wiseSayingTweetNoLogFilePath,'r',encoding='utf-8') as f:
                wiseSayingTweetNoLog = f.read().split('\n')
        
        # 対象ツイートNo絞り込み   
        if len(wiseSayingTweetNoLog) > 0:
            
            # ツイート済NoはtargetTweetNoから除外する
            targetTweetNo = [tweetNo for tweetNo in targetTweetNo if not tweetNo in wiseSayingTweetNoLog]

            # 対象ツイートNoが取得できなかった場合は名言ツイートログファイルを初期化する
            if len(targetTweetNo) == 0:
                
                with open(wiseSayingTweetNoLogFilePath, mode='w') as f:
                    targetTweetNo = range(1, len(dfWiseSaying) + 1)
                    
        # ツイートNoをランダム選択
        tweetNo = random.choice(targetTweetNo)

        # ツイートNoを名言ツイートログに書込
        with open(wiseSayingTweetNoLogFilePath, mode='a') as f:
            f.write(str(tweetNo))
            f.write('\n')
        
        # dfWiseSayingから対象となるツイートを取得する
        return dfWiseSaying[dfWiseSaying['no'] == tweetNo]
    
    def getWiseSayingPtrnData(self, wiseSayingTweetPattern):
        
        """
        名言ツイートパターンリストを取得する
        
        Parameters
        ----------
        wiseSayingTweetPattern : str
            名言ツイートパターンNo

        """
        
        # 名言ツイートパターンリストjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfWiseSayingPtrn = ji.convertToDataFrame(gv.kojimaConfig.wiseSayingJsonDir, gv.kojimaConfig.wiseSayingPtrnJsonFileName)
        
        # 該当する名言パターンを取得
        srWiseSayingPtrn = dfWiseSayingPtrn[dfWiseSayingPtrn['pattern'] == wiseSayingTweetPattern].iloc[0]
        
        # 名言パターンリストクラスへ値セット
        gv.kojimaConfig.wiseSayingPattern.pattern = wiseSayingTweetPattern
        gv.kojimaConfig.wiseSayingPattern.font_name = srWiseSayingPtrn['font_name']
        gv.kojimaConfig.wiseSayingPattern.say_ipX = srWiseSayingPtrn['say{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_ipY = srWiseSayingPtrn['say{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_fontSize = srWiseSayingPtrn['say{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_indentYPoint = srWiseSayingPtrn['say{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_txtHeight = srWiseSayingPtrn['say{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_ipX = srWiseSayingPtrn['category{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_ipY = srWiseSayingPtrn['category{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_fontSize = srWiseSayingPtrn['category{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_indentYPoint = srWiseSayingPtrn['category{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_txtHeight = srWiseSayingPtrn['category{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_ipX = srWiseSayingPtrn['speaker{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_ipY = srWiseSayingPtrn['speaker{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_fontSize = srWiseSayingPtrn['speaker{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_indentYPoint = srWiseSayingPtrn['speaker{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_txtHeight = srWiseSayingPtrn['speaker{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_label = '出典:{}' if self._lang == self.botLang.jp else 'source:{}'

    def generateTweetImage(self):
        
        """
        名言ツイート画像生成
        """
        
        # 名言ツイートDataFrame取得
        dfWiseSaying = self.getWiseSayingTweetData()        
        if len(dfWiseSaying):
            srWiseSayingTweet = dfWiseSaying.iloc[0]
        else:
            return ''

        # 名言ツイートパターンリストDataFrame取得
        self.getWiseSayingPtrnData(srWiseSayingTweet['pattern'])
        wsp = gv.kojimaConfig.wiseSayingPattern
        
        # イメージクラスインスタンス
        imageFileName = srWiseSayingTweet['file_name']
        orgFolderDir = gv.kojimaConfig.orgImageFolderDir
        genFolderDir = gv.kojimaConfig.genImageFolderDir
        uwi = uwImage(self.rootPathFull, imageFileName, orgFolderDir, genFolderDir)

        # フォントファイル名取得
        fontFileName = wsp.font_name
        fontFilePath = os.path.join(gv.kojimaConfig.fontFolderDir, fontFileName)

        # テキストの文字数に応じて挿入開始位置を調整
        adjInsertPointY = self.getAdjustInsertPointY(srWiseSayingTweet['wise_saying_{}'.format(self._lang)], 
                                                     wsp.say_indentYPoint, 
                                                     wsp.say_txtHeight, 
                                                     4)
        
        # テキスト挿入(本文)
        uwi.setFont(fontFilePath, wsp.say_fontSize)
        uwi.insertText(srWiseSayingTweet['wise_saying_{}'.format(self._lang)], 
                       insertPoint=(wsp.say_ipX,adjInsertPointY + wsp.say_ipY), 
                       indentationYPoint=wsp.say_indentYPoint, 
                       textHeight=wsp.say_txtHeight)

        # テキスト挿入(category)
        if srWiseSayingTweet['category_{}'.format(self._lang)] != '':
            uwi.setFont(fontFilePath, wsp.category_fontSize)
            uwi.insertText(wsp.category_label.format(srWiseSayingTweet['category_{}'.format(self._lang)]), 
                           insertPoint=(wsp.category_ipX,wsp.category_ipY), 
                           indentationYPoint=wsp.category_indentYPoint, 
                           textHeight=wsp.category_txtHeight)

        # テキスト挿入(speaker)
        if srWiseSayingTweet['speaker_{}'.format(self._lang)] != '':
            uwi.setFont(fontFilePath, wsp.speaker_fontSize)
            uwi.insertText('@{}'.format(srWiseSayingTweet['speaker_{}'.format(self._lang)]), 
                           insertPoint=(wsp.speaker_ipX,wsp.speaker_ipY), 
                           indentationYPoint=wsp.speaker_indentYPoint, 
                           textHeight=wsp.speaker_txtHeight)

        # イメージを保存する
        return uwi.saveImage()
        