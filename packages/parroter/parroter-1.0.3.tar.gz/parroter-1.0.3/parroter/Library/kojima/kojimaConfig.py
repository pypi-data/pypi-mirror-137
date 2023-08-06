from parroter.Library.parroterConfig import parroterConfig

class kojimaConfig(parroterConfig):
    
    """
    児嶋共通設定クラス(kojimaConfig)
    """ 
    
    class wise_saying_pattern():
        
        """
        名言パターンリスト
        """
        
        def __init__(self):
            
            """
            コンストラクタ
            """
            
            self.pattern = ''
            self.font_name = ''
            self.say_ipX = 0
            self.say_ipY = 0
            self.say_fontSize = 0
            self.say_indentYPoint = 0
            self.say_txtHeight = 0
            self.category_ipX = 0
            self.category_ipY = 0
            self.category_fontSize = 0
            self.category_indentYPoint = 0
            self.category_txtHeight = 0
            self.speaker_ipX = 0
            self.speaker_ipY = 0
            self.speaker_fontSize = 0
            self.speaker_indentYPoint = 0
            self.speaker_txtHeight = 0
            self.category_label = ''

    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        self.wiseSayingJsonDir = ''
        """ 名言json格納先ディレクトリ """

        self.wiseSayingTweetNoLogDir = ''
        """ 名言TweetNoログ格納先ディレクトリ """

        self.wiseSayingJsonFileName = ''
        """ 名言jsonファイル名 """

        self.wiseSayingPtrnJsonFileName = ''
        """ 名言パターンリストjsonファイル名 """

        self.wiseSayingTweetNoLogFileName = ''
        """ 名言TweetNoログファイル名 """

        self.wiseSayingPattern = self.wise_saying_pattern()
        """ 名言パターンリスト """
        
    def getConfigFileName(self):
        
        """ 
        設定ファイル名 
        """

        return 'kojima.ini'
    
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # 基底側実行
        super().setInstanceMemberValues()

        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingJsonDir',self.config_ini,'DIR','WISE_SAYING_JSON_DIR',str)

        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingTweetNoLogDir',self.config_ini,'DIR','WISE_SAYING_LOG_DIR',str)
        
        # wise_saying - json - FileName
        super().setConfigValue('wiseSayingJsonFileName',self.config_ini,'FILE','WISE_SAYING_JSON_FILENAME',str)

        # wise_saying_pattern - json - FileName
        super().setConfigValue('wiseSayingPtrnJsonFileName',self.config_ini,'FILE','WISE_SAYING_PATTERN_JSON_FILENAME',str)

        # wise_saying - log - FileName
        super().setConfigValue('wiseSayingTweetNoLogFileName',self.config_ini,'FILE','WISE_SAYING_LOG_FILENAME',str)
