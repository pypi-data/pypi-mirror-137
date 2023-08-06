import os
import sys
import math
import LibHanger.Library.uwLogger as Logger
from twython import Twython, TwythonError
from LibHanger.Library.uwConfig import cmnConfig
from parroter.Library.parroterConfig import parroterConfig

class parroterBase():
    
    """
    parroter基底クラス
    """
    
    def __init__(self, rootPath) -> None:
        
        """
        コンストラクタ
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        """
        
        # LibHanger.ini
        dc = cmnConfig()
        dc.getConfig(rootPath)
        
        # ロガー設定
        Logger.setting(dc)

        # 共通設定
        self.config = dc
        self.parroterConfig:parroterConfig = None
        
        # キートークン初期化
        self.twitter = None
        
        # ルートパス
        self.rootPathFull = rootPath
        self.rootPath = os.path.dirname(rootPath)
    
    @property
    def appName(self):
        
        """
        アプリ名
        """

        return ''
    
    def settingConfig(self):
        
        """
        parroter共通設定(派生側でオーバーライドする)
        """
        
        pass
    
    def setKeyToken(self):
        
        """
        キートークンを設定する
        """
        
        # キートークン設定
        self.twitter = Twython(
                         self.parroterConfig.consumer_key
                        ,self.parroterConfig.consumer_secret
                        ,self.parroterConfig.access_token
                        ,self.parroterConfig.access_token_secret
                        )
    
    def tweetHello(self):
        
        """
        挨拶をツイートする
        """
        
        # 挨拶ツイート内容の設定
        helloTweetText = self.getHelloTweetText()

        # ツイートに含める画像の設定
        helloTweetImage = self.getHelloTweetImage()
                
        # 挨拶をツイートする
        response, result = self.tweet(helloTweetText, helloTweetImage)
        if result:
            
            try:
                
                # ログ出力先ディレクトリを作成
                hello_id_dir, reply_log_dir = self.createLogOutputDir()
                
                # ログ出力先取得
                hello_id_path, reply_log_path = self.getLogOutputPath(hello_id_dir, reply_log_dir)
                
                # 挨拶ツイートログ出力
                self.createHelloTweetLog(response, hello_id_path)
                
                # 返信ツイートログ初期化
                self.createReplyTweetLog(response, reply_log_path)
                
            except Exception as e:                
                # エラーロギング
                Logger.logging.error(e.msg)
                # 処理を停止
                sys.exit()

        else:
            # 処理を停止
            sys.exit()
        
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        return ''
    
    def getHelloTweetImage(self):
        
        """
        挨拶ツイートに含める画像を取得する
        """
        
        return ''
    
    def getAdjustInsertPointY(self, insertText, indentYPoint, txtHeight, maxIndentCount):

        """
        テキスト挿入位置調整

        Parameters
        ----------
        insertText : str
            挿入文字列
        indentYPoint : int
            1行あたり文字数
        txtHeight : int
            文字高さ
        maxIndentCount : int
            最大字下げ数            
        """
                
        insertTextLen = len(insertText)
        if insertTextLen <= indentYPoint:
            adjInsertPointY = 0
        else:
            baseLength = indentYPoint * maxIndentCount
            indentCount = math.floor(baseLength / insertTextLen) if insertTextLen < baseLength else maxIndentCount
            adjInsertPointY = -1 * (txtHeight * indentCount)
        
        return adjInsertPointY
    
    def tweet(self, tweetText, fileName = ''):
        
        """
        ツイートする
        
        Parameters
        ----------
        tweetText : str
            ツイート文
        fileName : str
            ツイート画像ファイルパス
        """
        
        response = None
        try:
            # 挨拶ツイート
            if fileName == '': # テキストのみ
                response = self.twitter.update_status(status=tweetText)
            else: # 画像付き
                if os.path.exists(fileName):                    
                    image=open(fileName,'rb')
                    image_upl_inf = self.twitter.upload_media(media=image)
                    media_id = image_upl_inf['media_id']                    
                    response = self.twitter.update_status(status=tweetText, media_ids=[media_id])
                else:
                    response = self.twitter.update_status(status=tweetText)
        except TwythonError as e:
            # エラーロギング
            Logger.logging.error(e.msg)
            # Falseを返す
            return response, False
        else:
            return response, True
        
    def getLogOutputPath(self, hello_id_dir, reply_log_dir):
        
        """
        ログ出力先を返す

        Parameters
        ----------
        hello_id_dir : str
            挨拶ツイートIDログ出力先
        reply_log_dir : str
            返信ツイートIDログ出力先
        """
        
        # ログ出力先
        hello_id_path = os.path.join(hello_id_dir, 
                                     self.parroterConfig.hello_id_filename)
        reply_log_path = os.path.join(reply_log_dir, 
                                      self.parroterConfig.reply_log_filename)
        
        # ログ出力先を返す
        return hello_id_path, reply_log_path
    
    def createLogOutputDir(self):
        
        """
        ログ出力先ディレクトリ作成
        """

        # ログ出力先ディレクトリ
        hello_id_dir = os.path.join(self.rootPath, 
                                    self.parroterConfig.hello_id_folder)
        reply_log_dir = os.path.join(self.rootPath, 
                                     self.parroterConfig.reply_log_folder)
        
        # ログ出力先ディレクトリを作成
        os.makedirs(hello_id_dir, exist_ok=True)
        os.makedirs(reply_log_dir, exist_ok=True)
        
        # 作成したディレクトリパスを返す
        return hello_id_dir, reply_log_dir

    def createHelloTweetLog(self, response, hello_id_path):
        
        """
        挨拶ツイートログ出力

        Parameters
        ----------
        response : any
            tweet-response
        hello_id_path : str
            挨拶ツイートIDログ出力先        
        """
        
        # 挨拶ツイートログ出力
        with open(hello_id_path, mode='w') as f:
            f.write(response['id_str'])
            
    def createReplyTweetLog(self, response, reply_log_path):
        
        """
        返信ツイートログ出力
        
        Parameters
        ----------
        response : any
            tweet-response
        reply_log_path : str
            返信ツイートIDログ出力先  
        """
        
        # 返信ツイートログ出力
        with open(reply_log_path, mode='w') as f:
            pass
