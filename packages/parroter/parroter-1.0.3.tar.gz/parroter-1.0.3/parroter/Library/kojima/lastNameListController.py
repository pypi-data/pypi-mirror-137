from Scrapinger.Library.browserContainer import browserContainer
from Scrapinger.Library.webDriverController import webDriverController
from parroter.Library.kojima.kojimaGlobals  import *

class lastNameListController(browserContainer):
    
    """
    苗字リスト取得コントローラー
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()
                
        # WebDriverController
        self.wdc = webDriverController(gv.kojimaConfig, self)
        