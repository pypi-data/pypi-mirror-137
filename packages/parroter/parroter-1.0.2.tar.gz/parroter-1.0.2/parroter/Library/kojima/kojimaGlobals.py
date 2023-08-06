from parroter.Library.parroterGlobals import parroterGlobal
from parroter.Library.kojima.kojimaConfig import kojimaConfig

class kojimaGlobal(parroterGlobal):
    
    """
    児嶋botグローバル設定クラス
    """
    
    def __init__(self):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ呼び出し
        super().__init__()
        
        self.kojimaConfig:kojimaConfig = None
        """ kojima共通設定 """

# インスタンス生成(import時に実行される)
gv = kojimaGlobal()