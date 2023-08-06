from Scrapinger.Library.scrapingConfig import scrapingConfig

class parroterConfig(scrapingConfig):
    
    """
    parotter共通設定クラス(parotterConfig)
    """ 
                    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        self.consumer_key = ''
        """ コンシューマキー """

        self.consumer_secret = ''
        """ コンシューマキー(秘密) """
        
        self.access_token = ''
        """ アクセストークン """

        self.access_token_secret = ''
        """ アクセストークン(秘密) """

        self.hello_id_folder = ''
        """ 挨拶ツイートのIDログ格納先フォルダ """
        
        self.hello_id_filename = ''
        """ 挨拶ツイートのIDログファイル名 """
        
        self.reply_log_folder = ''
        """ 返信ツイートのIDログ格納先フォルダ """

        self.reply_log_filename = ''
        """ 返信ツイートのIDログファイル名 """
        
        self.appListDir = ''
        """ アプリリストフォルダパス """
        
        self.appHelloTextFileName = ''
        """ アプリ挨拶文テキストファイル名 """

        self.myoji_yurai_URL = 'https://myoji-yurai.net/prefectureRanking.htm?prefecture=%E5%85%A8%E5%9B%BD&page={}'
        """ myoji-yurai URL """
        
        self.orgImageFolderDir = ''
        """ オリジナルイメージ格納先フォルダ """

        self.genImageFolderDir = ''
        """ 生成イメージ格納先フォルダ """

        self.fontFolderDir = ''
        """ フォントファイル格納先フォルダ """
        
    def getConfigFileName(self):
        
        """ 
        設定ファイル名 
        """

        return 'parroter.ini'
    
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # 基底側実行
        super().setInstanceMemberValues()
        
        # consumer_key
        super().setConfigValue('consumer_key',self.config_ini,'KEYTOKEN','CONSUMER_KEY',str)

        # consumer_secret
        super().setConfigValue('consumer_secret',self.config_ini,'KEYTOKEN','CONSUMER_SECRET',str)

        # access_token
        super().setConfigValue('access_token',self.config_ini,'KEYTOKEN','ACCESS_TOKEN',str)

        # access_token_secret
        super().setConfigValue('access_token_secret',self.config_ini,'KEYTOKEN','ACCESS_TOKEN_SECRET',str)

        # hello-id Folder
        super().setConfigValue('hello_id_folder',self.config_ini,'LOG','HELLO_ID_FOLDER',str)

        # hello-id FileName
        super().setConfigValue('hello_id_filename',self.config_ini,'LOG','HELLO_ID_FILENAME',str)

        # reply-log Folder
        super().setConfigValue('reply_log_folder',self.config_ini,'LOG','REPLY_LOG_FOLDER',str)

        # reply-log FileName
        super().setConfigValue('reply_log_filename',self.config_ini,'LOG','REPLY_LOG_FILENAME',str)

        # App - ListDir
        super().setConfigValue('appListDir',self.config_ini,'DIR','APP_LIST_DIR',str)

        # App - helloText - FileName
        super().setConfigValue('appHelloTextFileName',self.config_ini,'FILE','APP_HELLO_TEXT_FILENAME',str)

        # myoji-yurai URL
        super().setConfigValue('myoji_yurai_URL',self.config_ini,'SITE','MYOJI_YURAI_URL',str)

        # original image folder path
        super().setConfigValue('orgImageFolderDir',self.config_ini,'DIR','ORG_IMAGE_FOLDER_DIR',str)

        # generate image folder path
        super().setConfigValue('genImageFolderDir',self.config_ini,'DIR','GEN_IMAGE_FOLDER_DIR',str)

        # font file folder path
        super().setConfigValue('fontFolderDir',self.config_ini,'DIR','FONT_FOLDER_DIR',str)
